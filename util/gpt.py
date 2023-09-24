from collections import defaultdict
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import openai

from gpt_config import (DEFAULT_MODEL, FREQUENCY_PENALTY, LOG_FOLDER, MAX_GENERATION_TOKENS, MAX_TOKENS_BY_MODEL,
                        PRESENCE_PENALTY, SYSTEM_PROMPT, TEMPERATURE, TOKEN_RATE_LIMIT_BY_MODEL, TOP_P, GPT3, GPT4)
from util.cleanup import cleanup_gpt_output
from util.time import get_date, get_time
from util.tokens import (count_tokens_in_messages,
                         remove_messages_until_token_count_available)

openai.api_key = open("openai-api-key.txt", "r").read().strip()

# (token_count) entries for rate limit issues
# rate limit:
# GPT4: is 200 requests / min and 40.000 tokens / min
# GPT3: is 3.500 requests / min and 180.000 tokens / min
requests = defaultdict(int)


def chat_completion(messages: list[str] | str, system_message: str = SYSTEM_PROMPT, model: str = DEFAULT_MODEL, stream_output: bool = False) -> str:
    if isinstance(messages, str):
        messages = [messages]
    messages = remove_messages_until_token_count_available(
        messages, MAX_GENERATION_TOKENS, model)

    folder_path = f"{LOG_FOLDER}/{get_date()}"

    os.makedirs(folder_path, exist_ok=True)

    file_path = f"{folder_path}/{get_time()}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Request:\n")
        for message in messages:
            f.write(str(message) + "\n\n")

    total_tokens = count_tokens_in_messages(messages + [system_message])
    print(
        f"Fetching response ({total_tokens} tokens in messages) for {len(messages)} messages.")

    requests[model] += total_tokens + MAX_GENERATION_TOKENS

    if stream_output:
        sys.stdout.write("GPT: ")
        sys.stdout.flush()

    while requests[model] > TOKEN_RATE_LIMIT_BY_MODEL[model]:
        print("Rate limit exceeded, sleeping for 1 second...")
        time.sleep(1)

    text = ""
    for res in openai.ChatCompletion.create(
        model=model,
        messages=_messages_to_map(messages, system_message),
        temperature=TEMPERATURE,
        max_tokens=MAX_GENERATION_TOKENS,
        top_p=TOP_P,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
        stream=True
    ):
        content = str(res["choices"][0]["delta"].get("content", ""))
        content = cleanup_gpt_output(content.encode("utf-8")).decode("utf-8")
        if stream_output:
            sys.stdout.write(content)
            sys.stdout.flush()
        text += content

    requests[model] -= total_tokens + MAX_GENERATION_TOKENS

    if stream_output:
        sys.stdout.write("\n\n")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n\nResponse:\n")
        f.write(text)

    return text


def gpt_in_parallel(messages: list[list[str]], system_message: str = SYSTEM_PROMPT, model: str = DEFAULT_MODEL) -> list[str]:
    results = [None] * len(messages)

    def worker(msg_list):
        return chat_completion(msg_list, system_message=system_message, model=model, stream_output=False)

    with ThreadPoolExecutor() as executor:
        future_to_index = {
            executor.submit(worker, msg_list): index
            for index, msg_list in enumerate(messages)
        }

        for future in as_completed(future_to_index):
            index = future_to_index[future]
            results[index] = future.result()

    return results


def create_embedding(input: str) -> list[float]:
    response = openai.Embedding.create(
        input=input,
        model="text-embedding-ada-002"
    )

    return response['data'][0]['embedding']


def _messages_to_map(messages: list[str], system_message: str) -> list[dict[str, str]]:
    prompts = [{"role": "system", "content": system_message}]
    is_user = len(messages) % 2 == 1

    for message in messages:
        role = "user" if is_user else "assistant"
        prompts.append({"role": role, "content": message})
        is_user = not is_user

    return prompts

import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import openai

from gpt_config import (FREQUENCY_PENALTY, LOG_FOLDER, MAX_TOKENS,
                        PRESENCE_PENALTY, TEMPERATURE, TOP_P)
from util.cleanup import cleanup_gpt_output
from util.time import get_date, get_time
from util.tokens import (count_tokens_in_messages,
                         remove_messages_until_token_count_available)

openai.api_key = open("../openai-api-key.txt", "r").read().strip()

SYSTEM_PROMPT = """You are a helpful assistant helping a student."""

GPT3 = "gpt-3.5-turbo-16k"
GPT4 = "gpt-4"

DEFAULT_MODEL = GPT4


def _messages_to_map(messages: list[str], system_message: str) -> list[dict[str, str]]:

    messages = [{"role": "system", "content": system_message}]
    is_user = len(messages) % 2 == 1

    for message in messages:
        role = "user" if is_user else "assistant"
        messages.append({"role": role, "content": message})
        is_user = not is_user

    return messages


def chat_completion(messages: list[str], system_message: str = SYSTEM_PROMPT, model: str = DEFAULT_MODEL, stream_output: bool = False) -> str:
    messages = remove_messages_until_token_count_available(messages, MAX_TOKENS)

    folder_path = f"{LOG_FOLDER}/{get_date()}"

    os.makedirs(folder_path, exist_ok=True)

    file_path = f"{folder_path}/{get_time()}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Request:\n")
        for message in messages:
            f.write(str(message) + "\n\n")

    print(f"Fetching response ({count_tokens_in_messages(messages)} tokens in messages) for {len(messages)} messages.")

    for _ in range(3):
        try:
            if stream_output:
                sys.stdout.write("GPT: ")

            text = ""
            for res in openai.ChatCompletion.create(
                model=model,
                messages=_messages_to_map(messages, system_message),
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
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

            if stream_output:
                sys.stdout.write("\n\n")
            break
        except openai.error.RateLimitError:
            print("Rate limit exceeded, retrying...")
    else:
        raise openai.error.RateLimitError("Rate limit exceeded, please try again later.")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n\nResponse:\n")
        f.write(text)

    return text


def gpt_in_parallel(messages: list[list[str]], system_message: str = SYSTEM_PROMPT, model: str = DEFAULT_MODEL) -> list[str]:
    results = [None] * len(messages)

    def worker(msg_list):
        return chat_completion(msg_list, system_message=system_message, model=model, stream_output=False)

    with ThreadPoolExecutor() as executor:
        future_to_index = {executor.submit(worker, msg_list): index for index, msg_list in enumerate(messages)}

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


import tiktoken

from gpt_config import MAX_TOKENS_BY_MODEL

encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens_in_messages(messages: list[str]) -> int:
    return sum(count_tokens(message) for message in messages)


def count_tokens(text: str) -> int:
    return len(encoding.encode(text))


def chunk_string_by_tokens(s: str, start_words: int = 3000, max_tokens: int = 4000):
    # Split the text into words
    words = s.split()

    word_idx = 0
    while word_idx < len(words):
        # Start with a base of `start_words`
        current_words = ' '.join(words[word_idx: word_idx + start_words])
        word_idx += start_words

        # Keep adding words until token limit is reached
        while word_idx < len(words) and count_tokens_in_messages(current_words) <= max_tokens:
            current_words += ' ' + words[word_idx]
            word_idx += 1

        # When the token limit is reached or we're at the end of the words list,
        # we save the current chunk and move to the next one
        yield current_words


def remove_messages_until_token_count_available(messages: list[str], token_count: int, model: str) -> list[str]:
    while count_tokens_in_messages(messages) > MAX_TOKENS_BY_MODEL[model] - token_count:
        print(
            f"Warning: removing message with {count_tokens_in_messages(messages)} tokens.")
        messages.pop(0)

    if len(messages) == 0:
        raise ValueError(
            "No messages left after removing messages until token count available.")

    return messages

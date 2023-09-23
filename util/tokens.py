
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

MAX_TOKENS = 8000


def count_tokens_in_messages(messages: list[str]) -> int:
    return sum(count_tokens(message) for message in messages)


def count_tokens(text: str) -> int:
    return len(encoding.encode(text))


def chunk_string_by_tokens(s, start_words=3000, max_tokens=4000):
    # Split the text into words
    words = s.split()

    word_idx = 0
    while word_idx < len(words):
        # Start with a base of `start_words`
        current_words = words[word_idx: word_idx + start_words]
        word_idx += start_words

        # Keep adding words until token limit is reached
        while word_idx < len(words) and count_tokens(' '.join(current_words)) <= max_tokens:
            current_words.append(words[word_idx])
            word_idx += 1

        # When the token limit is reached or we're at the end of the words list,
        # we save the current chunk and move to the next one
        yield (' '.join(current_words))


def remove_messages_until_token_count_available(messages: list[str], token_count: int) -> list[str]:
    while count_tokens_in_messages(messages) > MAX_TOKENS - token_count:
        print("Warning: removing message with " +
              str(count_tokens(messages[0].content)) + " tokens.")
        messages.pop(0)

    if len(messages) == 0:
        raise ValueError(
            "No messages left after removing messages until token count available.")

    return messages

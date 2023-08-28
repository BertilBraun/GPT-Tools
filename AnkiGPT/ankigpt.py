import os

from config import LECTURE, OUTPUT_FILE, OUTPUT_FOLDER, PROMPT, SYSTEM_PROMPT

from util.gpt import gpt_in_parallel
from util.input import input_from_clipboard
from util.time import get_time
from util.tokens import chunk_string_by_tokens

time = get_time()

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

OUTPUT_FILE = OUTPUT_FOLDER + "/" + OUTPUT_FILE.format(time=time)


# Get content from clipboard
clipboard_content = input_from_clipboard("Copy the text you want to turn into flashcards")
print(f"Text copied from clipboard (len {len(clipboard_content)}). Generating flashcards...")


# chunk the content into 4000 tokens (not characters) chunks
prompts = [
    [PROMPT.format(lecture=LECTURE, lecture_content=chunk)]
    for chunk in chunk_string_by_tokens(clipboard_content)
]

flashcards = gpt_in_parallel(prompts, system_message=SYSTEM_PROMPT)

with open(OUTPUT_FILE, "w") as f:
    for flashcard in flashcards:
        f.write(flashcard)

print(f"Flashcards saved to '{OUTPUT_FILE}'")

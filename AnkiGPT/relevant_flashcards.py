
from config import PROMPT, SYSTEM_PROMPT

from util.gpt import gpt_in_parallel
from util.tokens import chunk_string_by_tokens

PROMPT = """
---
{lecture_content}
---
I'm a Masters Computer Science student with focus on AI. You will help me study my lecture on "Advanced Machine Learning" by helping me with flashcards for learning the content of the lecture for the exam.
I've been informing myself passively for the last 2 years via YouTube, podcasts, and books. I've also been actively learning for the last 6 months via online courses and projects. I'm least informed about Robotics and Reinforcement Learning.
Aggressively filter out questions only output the line numbers of the **most relevant fifth** of the questions.
Output the line numbers as a comma separated list.
"""

# Open the combined file in read mode and a new file in write mode
with open('combined_flashcards.txt', 'r') as infile, open('numbered_flashcards.txt', 'w') as outfile:
    for index, line in enumerate(infile, start=1):
        outfile.write(f"{index};{line}\n")

flashcards = open("numbered_flashcards.txt", "r").read()

# chunk the content into 4000 tokens (not characters) chunks
prompts = [
    [PROMPT.format(lecture_content=chunk)]
    for chunk in chunk_string_by_tokens(flashcards)
]

relevant_flashcards_list = gpt_in_parallel(prompts, system_message=SYSTEM_PROMPT)

with open("relevant_flashcards.txt", "w") as f:
    for relevant_flashcards in relevant_flashcards_list:
        relevant_flashcards = relevant_flashcards.replace("'", "").replace('"', "").split(",")
        print(f"Relevant flashcards: {len(relevant_flashcards)} {relevant_flashcards}")

        for relevant_flashcard in relevant_flashcards:
            try:
                # strip of line number and semicolon, then write to file
                flashcard = flashcards[int(relevant_flashcard) - 1]
                f.write(flashcard[flashcard.index(";") + 1:])
            except:
                print(f"Error with flashcard {relevant_flashcard}")

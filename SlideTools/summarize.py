from util.gpt import chat_completion
from util.input import input_from_clipboard

PROMPT = """
This is my Advanced AI Lecture at the KIT.
The following is the content of the lecture:
---

{text}

---

Summarize the Key concepts mentioned in the lecture for me as a recap after listening to the lecture. 
Summarize everything. 
You can write as much as you want.
"""

CONTENT_FORMAT = "\n## {title}\n\n{content}\n"


def find_last_lecture(filename: str) -> str:
    """
    Function to find the last lecture written in the markdown file
    """
    last_lecture = None
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('### '):
                last_lecture = line[4:].strip()  # remove '### ' from the start and any trailing whitespace
    return last_lecture


with open('lectures.md', 'w') as f:
    while True:
        last_lecture_number = find_last_lecture('lectures.md')
        lecture_number = int(last_lecture_number) + 1 if last_lecture_number else 1

        content = input_from_clipboard()
        summary = chat_completion(PROMPT.format(text=content))

        f.write(CONTENT_FORMAT.format(title=str(lecture_number), content=summary))
        f.flush()

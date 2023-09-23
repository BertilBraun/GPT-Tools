
from util.gpt import chat_completion
from util.input import input_from_clipboard


# Get content from clipboard
clipboard_content = input_from_clipboard("Copy the overview of the lecture")
print(
    f"Text copied from clipboard (len {len(clipboard_content)}). Generating topics...")

prompt = f"""
The following is a list of topics covered in the lecture:
---
{clipboard_content}
---
Return a newline-separated list of the most relevant topics covered in the lecture:
"""

topics = chat_completion([prompt], stream_output=True)

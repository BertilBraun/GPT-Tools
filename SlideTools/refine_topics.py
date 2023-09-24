
from util.gpt import chat_completion

PROMPT = """
This is my data science lecture at KIT.
The following are the topics of the lecture:
---

{text}

---
Remove thematically duplicated entries and put the topics in a meaningful order.
Return a list of bullet points containing these topics.
"""

OUTPUT_FILE = 'topics_refined.md'
INPUT_FILE = 'topics.md'


topics = open(INPUT_FILE, 'r').read()

response = chat_completion(PROMPT.format(text=topics))

open(OUTPUT_FILE, 'w').write(response)

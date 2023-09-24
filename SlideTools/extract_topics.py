import os

from util.gpt import GPT3, gpt_in_parallel
from SlideTools.config import LECTURE_DIR, OUTPUT_FILE
from util.pdf import extract_text_from_lecture_pdf
from util.tokens import chunk_string_by_tokens

PROMPTS = [
    """Please analyze the following lecture slides from a Data Science course and list the most relevant academic concepts such as topics, algorithms, data structures, and ideas. The goal is to create a summary of key points in a simple bullet-point list.
Make sure the list includes all the major topics that were covered in the lecture.""",
    """Query types
Traditional indexes like the B-tree allow efficient search
Match queries
E.g., SELECT * FROM Student WHERE gpa = 2.8
Range queries
E.g., SELECT * FROM Student WHERE gpa > 2.0 and gpa < 3.0
But they are limited for other queries (e.g., spatial queries)
k-Nearest Neighbor queries
Where is the closest restaurant? (k = 1)
Ranking queries
Which are the closest hotels? (ordered by increasing distance)
→ Requires multi-dimensional indexes
""",
    """- Query Types
- B-tree
- Match Queries
- Range Queries
- k-Nearest Neighbor Queries
- Ranking Queries
- Inverted Lists
- B Trees
- Spatial Indexes""",
]

pdfs = [
    filename for filename in os.listdir(LECTURE_DIR)
    if filename.endswith('.pdf')
]

# prompts get too long. Instead we want to define the prompts while using for chunk in chunk_string_by_tokens()
lecture_names = []
prompts = []

for filename in pdfs:
    lecture_name = filename.replace('.pdf', '')
    for chunk in chunk_string_by_tokens(extract_text_from_lecture_pdf(os.path.join(LECTURE_DIR, filename)), max_tokens=10000):
        prompts.append(PROMPTS + [chunk])
        lecture_names.append(lecture_name)

topics = gpt_in_parallel(prompts, model=GPT3)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('# Topics\n\n')

    last_lecture_name = None
    for lecture_name, topic in zip(lecture_names, topics):
        if lecture_name != last_lecture_name:
            f.write(f'## {lecture_name}\n\n')
            last_lecture_name = lecture_name
        f.write(f'{topic}\n\n')

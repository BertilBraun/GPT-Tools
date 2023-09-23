import os
from util.gpt import gpt_in_parallel, chat_completion
from util.time import get_date, get_day


def process_lecture_with_topics(lecture: str, topics: str) -> None:

    OUTPUT_FOLDER = f"knowledge/{lecture}"

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    PROMPT = """
The following is an example of a generated information card for the topic "Neural Networks":
---
# Neural Networks

- **Definition**: Neural networks are a set of algorithms modeled after the human brain, designed to recognize patterns.
- **Usage**: Used in applications like image and speech recognition, medical diagnosis, and financial forecasting.
- **Related Topics**: [[Machine Learning]], [[Deep Learning]]
---

Generate an information card for the topic "{topic}" in the context of "{lecture}" including Definition, Usage, and Related Topics:
"""

    topics = topics.split("\n")

    def cleanup(topic: str) -> str:
        # cleanup topics, make sure, that all topics start and end with a normal character [a-zA-Z], otherwise trim until they do
        while len(topic) > 0 and not topic[0].isalpha():
            topic = topic[1:]
        while len(topic) > 0 and not topic[-1].isalpha():
            topic = topic[:-1]
        return topic

    topics = [cleanup(topic) for topic in topics]
    topics = [topic for topic in topics if len(topic) > 0]

    prompts = [
        [PROMPT.format(topic=topic, lecture=lecture)]
        for topic in topics
    ]

    outputs = gpt_in_parallel(prompts)

    PROPERTIES = """---
title: {title}
created: {date} {day}
Tags: Informatics, {lecture}
---

"""

    for knowledge, topic in zip(outputs, topics):
        with open(f"{OUTPUT_FOLDER}/{topic}.md", "w") as f:
            f.write(PROPERTIES.format(title=topic, date=get_date(),
                    day=get_day(), lecture=lecture))

            knowledge = knowledge.replace('---', '').strip()
            f.write(knowledge)

    OVERVIEW = """
# {lecture}

```dataview
LIST
WHERE contains(file.folder, this.file.folder) AND choice(contains(file.name, "_Index_of"), false, true)
```

{topics}
"""

    TOPIC = "- [[{topic}]]"

    with open(f"{OUTPUT_FOLDER}/{lecture}.md", "w") as f:
        f.write(PROPERTIES.format(title=lecture, date=get_date(),
                day=get_day(), lecture=lecture))

        topics = "\n".join([TOPIC.format(topic=topic) for topic in topics])
        f.write(OVERVIEW.format(lecture=lecture, topics=topics))


def generate_overview_page_entries(lectures: list[str]) -> None:

    PROMPT = """
Help me generate an overview page entry for my lectures.
    
The following is an example of an overview page entry for the lecture "Computer Graphics":
---
### [[Computer Graphics]]

Covers fundamental concepts in computer graphics, including rendering, shading, geometry, and animation. Essential for creating visual content using computers.
---

Now generate an overview page entry for each of the lectures:
{lectures}
"""

    prompt = PROMPT.format(lectures="\n".join(lectures))

    output = chat_completion([prompt])

    with open("knowledge/overview.md", "a") as f:
        f.write(output.replace('---', '').strip())

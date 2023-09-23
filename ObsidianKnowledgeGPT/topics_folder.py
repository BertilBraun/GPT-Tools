

# for all files in ObsidianKnowledgeGPT/Topics/: call process_lecture_with_topics(lecture, topics) for each file

import os
import time

from ObsidianKnowledgeGPT.obsidianknowledgegpt import generate_overview_page_entries, process_lecture_with_topics


lectures = [file[:-4]
            for file in os.listdir("ObsidianKnowledgeGPT/Topics/") if file.endswith(".txt")]

for lecture in lectures:
    if lecture != "Natural Language Processing":
        continue
    with open(f"ObsidianKnowledgeGPT/Topics/{lecture}.txt", "r") as f:
        topics = f.read()
        process_lecture_with_topics(lecture, topics)

        # sleep for 1 minute to avoid rate limiting
        time.sleep(120)

generate_overview_page_entries(lectures)

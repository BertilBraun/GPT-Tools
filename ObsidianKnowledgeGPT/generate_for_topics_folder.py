import os

from ObsidianKnowledgeGPT.obsidianknowledgegpt import generate_overview_page_entries, process_lecture_with_topics


lectures = [
    file[:-4]
    for file in os.listdir("ObsidianKnowledgeGPT/Topics/")
    if file.endswith(".txt")
]

for lecture in lectures:
    with open(f"ObsidianKnowledgeGPT/Topics/{lecture}.txt", "r") as f:
        topics = f.read()
        process_lecture_with_topics(lecture, topics)

generate_overview_page_entries(lectures)

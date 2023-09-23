
from ObsidianKnowledgeGPT.obsidianknowledgegpt import generate_overview_page_entries, process_lecture_with_topics
from util.input import input_from_clipboard


lecture = input("Lecture: ")

# Get content from clipboard
clipboard_content = input_from_clipboard(
    "Copy the topics you want to turn into knowledge")
print(
    f"Text copied from clipboard (len {len(clipboard_content)}). Generating knowledge...")

process_lecture_with_topics(lecture, clipboard_content)

generate_overview_page_entries([lecture])

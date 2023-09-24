
OUTPUT_FOLDER = "flashcards"
OUTPUT_FILE = "flashcards-{time}.txt"
LECTURE = "Data Science"
SYSTEM_PROMPT = "You are a helpful professor who helps a student understand the content of a lecture."
PROMPT = """I am a master student of computer science. You will help me learn my lecture on "{lecture}" by creating flashcards to learn the content of the lecture for the exam.
Create 0-2 flashcards per topic that summarize the main content of the lecture.
---
{lecture_content}
---
The format of the flashcards is as follows:
---
Question;Answer
Question;Answer
...
---
For example:
---
What is a B-tree index used for and how is it structured?; Efficiently stores, sorts, and retrieves data in a balanced tree structure, with multiple keys per node and sorted children.
What does a range query do and where is it useful?; Finds records within specific bounds like numerical or date ranges, useful in search functionality.
What is a k-Nearest Neighbor query and how does it work?; Searches for the 'k' closest data points to a given point in a multidimensional space, often using Euclidean distance.
---
"""

from collections import Counter

from pypdf import PdfReader


def extract_text_from_pdf(filename: str) -> str:
    """ Function to extract the text from a pdf file """
    reader = PdfReader(filename)
    return '\n'.join(page.extract_text() for page in reader.pages)


def find_longest_exact_recurring_substrings(text: str, min_word_count: int = 10, max_word_count: int = 35, min_frequency: int = 25):
    # Initialize Counter to count substring occurrences
    counter = Counter()

    # Tokenize the text into words
    words = text.split(' ')

    # Go through all possible substrings and count their occurrences
    for i in range(len(words)):
        for j in range(i + min_word_count, min(i + max_word_count, len(words) + 1)):
            substring = ' '.join(words[i:j])
            counter[substring] += 1

    # Find and return substrings that appear frequently enough
    recurring_substrings = {substring: count for substring,
                            count in counter.items() if count >= min_frequency}

    return max(recurring_substrings, key=len) if len(recurring_substrings) > 0 else ''


def extract_text_from_lecture_pdf(filename: str) -> str:
    pdf_text = extract_text_from_pdf(filename)
    lecture_annotations = find_longest_exact_recurring_substrings(pdf_text)
    print(f"Removing {len(lecture_annotations) * pdf_text.count(lecture_annotations)} characters of lecture annotations from {filename}")
    return pdf_text.replace(lecture_annotations, '').strip()

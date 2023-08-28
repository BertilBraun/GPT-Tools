
import sys

import clipboard

CLIPBOARD_PROMPT = "Copy the text you want to use from your clipboard"


def input_from_clipboard(prompt: str = CLIPBOARD_PROMPT) -> str:
    input(f"{prompt}. Then press Enter to continue...")
    clipboard_content = clipboard.paste()
    return clipboard_content


def multiline_input(prompt: str) -> str:
    try:
        start = input(f"(SUMBIT to commit) {prompt}") + "\n"
        while "SUBMIT" not in start:
            start += input() + "\n"
        return start.replace("SUBMIT", "").strip()
    except KeyboardInterrupt:
        sys.exit(0)

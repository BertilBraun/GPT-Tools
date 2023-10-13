from ProtocolGeneration.config import EXTRACTED_PROTOCOL_FILE, NEW_PROTOCOL_OUTPUT_FILE
from util.gpt import chat_completion

protocol_text = open(EXTRACTED_PROTOCOL_FILE, "r", encoding="utf-8").read()

PROMPT = f"""Generate a new protocol which is similar but not equal to the example protocol:
{protocol_text}"""

new_protocol_text = chat_completion(PROMPT, stream_output=True)

open(NEW_PROTOCOL_OUTPUT_FILE, "w", encoding="utf-8").write(new_protocol_text)

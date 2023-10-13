import os

INPUT_FOLDER = "ProtocolGeneration/Protocols/"
OUTPUT_FOLDER = ".generated/protocol/"

EXTRACTED_PROTOCOL_FILE = OUTPUT_FOLDER + "extracted_protocol.md"
NEW_PROTOCOL_OUTPUT_FILE = OUTPUT_FOLDER + "new_protocol.md"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

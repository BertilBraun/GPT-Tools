import os
from ProtocolGeneration.config import EXTRACTED_PROTOCOL_FILE, INPUT_FOLDER
from util.ocr import extract_text_from_image


text = ""

# list all photos in the INPUT_FOLDER
for photo in os.listdir(INPUT_FOLDER):
    if photo.endswith(".jpg") or photo.endswith(".png"):

        # extract the protocol text from the photos
        extracted_text = extract_text_from_image(INPUT_FOLDER + photo)
        text += extracted_text + "\n\n\n"

# save the protocol text to EXTRACTED_PROTOCOL_FILE
open(EXTRACTED_PROTOCOL_FILE, "w", encoding="utf-8").write(text)

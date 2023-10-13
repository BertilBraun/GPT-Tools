import easyocr


def extract_text_from_image(image_path: str, languages=['en']) -> [str]:
    reader = easyocr.Reader(languages)
    return reader.readtext(image_path, detail=0)

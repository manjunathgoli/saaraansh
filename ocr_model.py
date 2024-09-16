import easyocr

def extract_text_from_image(file_path):
    # Use languages compatible with Devanagari
    reader = easyocr.Reader(['en'])  # Adjust as necessary
    result = reader.readtext(file_path)
    text = ' '.join([res[1] for res in result])
    return text

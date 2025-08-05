import streamlit as st
from transformers import pipeline
from PIL import Image
import easyocr

# Load the pre-trained text generation model
generator = pipeline("text-generation", model="gpt2")

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def generate_content(word):
    """
    Generates content about the given word using a pre-trained LLM.
    """
    prompt = f"Write a detailed description about the word '{word}' and its significance:"
    output = generator(prompt, max_length=150, num_return_sequences=1)
    return output[0]['generated_text']

def extract_text_from_image(image):
    """
    Extracts text from the provided image using OCR (EasyOCR).
    """
    text = reader.readtext(image)
    extracted_text = " ".join([t[1] for t in text])
    return extracted_text.strip()

# Streamlit interface
st.title("Image to Word Content Generator")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Extract text from the image (filename or OCR result)
    file_name = uploaded_image.name.split('.')[0]

    # If image has text, extract the text, else use filename
    if extract_text_from_image(image) != "":
        word = extract_text_from_image(image)
    else:
        word = file_name

    

    # Generate content related to the extracted word
    content = generate_content(word)
    st.write("Generated Content:")
    st.write(content)
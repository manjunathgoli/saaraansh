import streamlit as st
import requests
import os

st.title("Document Summarization App")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded file
    filepath = f"data/{uploaded_file.name}"
    with open(filepath, 'wb') as temp_file:
        temp_file.write(uploaded_file.read())

    # Send the file to Flask for summarization
    with open(filepath, 'rb') as f:
        file_content = f.read()

    # You may need to preprocess and send the file content as text or extract the text here
    # For now, we're simulating this with the file path
    response = requests.post(
        "http://127.0.0.1:5000/summarize",  # Flask API endpoint
        json={"text": filepath}  # Sending the file path for simplicity (ideally, send extracted text)
    )

    if response.status_code == 200:
        summary = response.json().get("summary")
        st.write("Summary:")
        st.write(summary)
    else:
        st.write("Error:", response.json().get("error"))

Multimodal Content Summarization Tool 📝🎧📷🎥

Overview

Omni Summarizer is an advanced tool designed to summarize content from various formats—text, audio, video, and images—into English, irrespective of the original language. Built using powerful models like BART, mBART, Whisper, and EasyOCR, this tool merges and fine-tunes these technologies to create a comprehensive solution for summarization across multiple media formats.

Key Features ✨

Multiformat Summarization: Supports text, audio, video, and image inputs, generating summaries in English.
Multilingual Support: Automatically translates content in different languages into English before summarizing.
Prompt-Based Search: Users can ask questions related to the generated summary, and the tool provides answers based on the previously produced summary.
Unified Platform: Combines text summarization, audio transcription, video analysis, and image-text extraction into a single tool.

Model Architecture 🧠

Our architecture combines multiple specialized models into one system for efficient summarization. Here’s an overview of the models we integrated:

BART/mBART: For summarizing text content.
Whisper: For audio transcription and summarization.
EasyOCR: For extracting text from images.
FFmpeg: For extracting and processing video content.

Workflow 🔄

Input Processing:

  Extracts text from audio, video, and images.
  Translates the extracted text into English if necessary.\
  
Summarization:

  Summarizes the English text, whether extracted or input directly.

Prompt-Based Search:

Users can ask questions based on the summary, and the system responds with relevant information from the summarized content.

Performance 🏅

Our system demonstrates high performance across multiple tasks, achieving:

ROUGE-1: 48.21%
ROUGE-2: 35.31%
ROUGE-L: 45.67%

Language Translation Accuracy: 96%

Image-Text Extraction:

  Word Error Rate (WER): 29.26%
  Character Error Rate (CER): 9.20%
  
Audio-Text Extraction:

  WER: 25.78%
  CER: 5.33%
  
These results show that Omni Summarizer is highly effective for students, researchers, and professionals who need quick summaries from various media types.

Visual Representation 🖼️

Model Architecture Diagram
Insert image of the model architecture here

Sample Summarization Flow
Insert image showcasing the input-to-summary flow here

Installation ⚙️
To set up Omni Summarizer, follow these steps:

Clone the repository:

git clone https: //github.com/manjunathgoli/saaraansh.git

Navigate to the project directory:

cd omni-summarizer
Install the necessary dependencies:

pip install -r requirements.txt
Run the application:

python app.py

Usage 🚀

You can provide content in various formats such as text, audio, video, or images, and the tool will generate a concise summary in English. Additionally, you can use the prompt-based search feature to query specific information from the summarized content.

Contributing 🤝

Contributions are welcome! Please fork this repository, create a feature branch, and submit a pull request with your enhancements.


import subprocess
import json
import requests
import re
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=200, min_length=50):
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=True)
        return summary[0]['summary_text']
    except Exception as e:
        print("Summarization Error:", e)
        return ""

def download_and_extract_subtitles(video_url, lang='en'):
    try:
        command = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-subs",
            "--sub-lang", lang,
            "--sub-format", "vtt",
            "--print-json",
            video_url
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return "Failed to process video."

        video_data = None
        for line in result.stdout.splitlines():
            if line.strip():
                try:
                    video_data = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue
        if not video_data:
            return "Failed to parse video data."

        subtitle_info = video_data.get("requested_subtitles", {}).get(lang)
        if not subtitle_info or "url" not in subtitle_info:
            return "No subtitles available."

        subtitle_url = subtitle_info["url"]
        response = requests.get(subtitle_url)
        if response.status_code == 200:
            subtitle_content = response.text
            lines = subtitle_content.splitlines()

            text_content = [re.sub(r"<[^>]*>", "", line).strip() for line in lines if not re.match(r"^\d{2}:\d{2}:\d{2}", line) and not line.startswith("WEBVTT")]
            return " ".join(text_content)
        else:
            return "Failed to download subtitles."
    except Exception as e:
        print("Error processing video:", e)
        return "Error processing video."

def process_video(video_url, lang='en', max_length=5000):
    try:
        subtitle_content = download_and_extract_subtitles(video_url, lang)
        if subtitle_content:
            extracted_text = subtitle_content[:max_length]  
            
            word_set = set(extracted_text.split())
            
            return " ".join(word_set)
        else:
            return "No subtitles could be extracted from the video."
    except Exception as e:
        print("Error processing video:", e)
        return "Error processing video."

def main():
    video_url = input("Enter YouTube video URL: ")
    lang = 'en'  
    extracted_text = process_video(video_url, lang)
    
    if extracted_text:
        print("\nExtracted Subtitles (Processed Text):\n")
        print(extracted_text)

        
        summary = summarize_text(extracted_text, max_length=200, min_length=50)
        print("\nSummarized Text:\n")
        print(summary)
    else:
        print("Failed to extract subtitles or no subtitles available for this video.")

if __name__ == "__main__":
    main()

import os
import subprocess
from transformers import pipeline

whisper = pipeline('automatic-speech-recognition', model='openai/whisper-medium')

def extract_text_from_audio(audio_path):
    # Perform speech-to-text using Whisper
    result = whisper(audio_path, return_timestamps=False)
    return result['text']

def extract_audio_from_video(video_path):
    output_audio_path = os.path.splitext(video_path)[0] + '.mp3'
    ffmpeg_cmd = [
        'ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame',
        '-ab', '192k', '-ar', '44100', '-y', output_audio_path
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    return output_audio_path

from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from ocr_model import extract_text_from_image
from audio_model import extract_text_from_audio, extract_audio_from_video
from translation_model import translate_text_if_needed
from summarization_model import summarize_text
from transformers import BartTokenizer, BartForConditionalGeneration

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize BART tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    media_type = request.form.get('media_type')
    max_length = int(request.form.get('max_length', 200))
    min_length = int(request.form.get('min_length', 50))

    if media_type in ['image', 'audio', 'video']:
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if media_type == 'image':
            extracted_text = extract_text_from_image(file_path)
        elif media_type == 'audio':
            extracted_text = extract_text_from_audio(file_path)
        elif media_type == 'video':
            audio_path = extract_audio_from_video(file_path)
            extracted_text = extract_text_from_audio(audio_path)

        translated_text = translate_text_if_needed(extracted_text)
        summary = summarize_text(translated_text, max_length=max_length, min_length=min_length)
        return summary

    elif media_type == 'text':
        input_text = request.form.get('input_text', '')
        if not input_text:
            return redirect(request.url)

        translated_text = translate_text_if_needed(input_text)
        summary = summarize_text(translated_text, max_length=max_length, min_length=min_length)
        return summary

    return redirect(request.url)

@app.route('/generate-response', methods=['POST'])
def generate_response():
    # Extract prompt and input_text from the form data
    prompt = request.form.get('prompt')
    input_text = request.form.get('input_text', '')

    # Debugging: Print the received prompt and input text
    print(f"Received prompt: {prompt}")
    print(f"Received input text: {input_text}")

    # Ensure input_text is not empty
    if not input_text:
        return jsonify({'error': 'Input text is required'}), 400

    # Translate and summarize the input_text
    translated_text = translate_text_if_needed(input_text)
    summarized_text = summarize_text(translated_text, max_length=200, min_length=50)

    # Debugging: Print the summarized text
    print(f"Summarized text: {summarized_text}")

    # Tokenize both the summarized text and the prompt
    input_tokenized = tokenizer(summarized_text, padding="max_length", truncation=True, return_tensors="pt")
    prompt_tokenized = tokenizer(prompt, padding=False, truncation=True, return_tensors="pt", add_special_tokens=False)
    
    # Prepare decoder inputs for prompt
    prompt_tokenized = {f"decoder_{k}": v for k, v in prompt_tokenized.items()}

    # Generate summary based on input and prompt
    try:
        generated_ids = model.generate(
            **input_tokenized,
            max_length=200,  # Increase max length for longer summaries
            do_sample=True,
            num_beams=5,  # More beams for better quality
            top_p=0.92,  # Tune top-p sampling for more coherent text
            repetition_penalty=1.5,  # Reduce repetition
            decoder_input_ids=prompt_tokenized['decoder_input_ids']
        )
        # Properly decode the generated tokens into text
        output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
        return jsonify({'summary': output[0]})
    except Exception as e:
        # Debugging: Print any errors that occur
        print(f"Error generating summary: {e}")
        return jsonify({'error': 'Error generating summary'}), 500

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

def translate_text_if_needed(text, src_lang_code="en_XX"):
    # Auto-detect language if not provided
    detected_lang = detect_language(text)  # Implement this function for language detection
    
    if detected_lang != "en_XX":
        tokenizer.src_lang = detected_lang
        encoded_input = tokenizer(text, return_tensors="pt")
        generated_tokens = model.generate(
            **encoded_input,
            forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"]
        )
        translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return translated_text
    return text  # If English, no translation needed

def detect_language(text):
    # Add language detection logic (you could use libraries like `langdetect`)
    return "en_XX"  # Placeholder for English

from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    source_accent = data.get('source_accent', '')
    target_accent = data.get('target_accent', '')

    if not text:
        return jsonify({'success': False, 'error': 'No text provided'}), 400

    if not source_lang:
        return jsonify({'success': False, 'error': 'No source language provided'}), 400

    if not target_lang:
        return jsonify({'success': False, 'error': 'No target language provided'}), 400

    try:
        # Translate the text
        translated_text = translator.translate(text, src=source_lang, dest=target_lang).text

        # Determine the tld for accents (for English only)
        tld = 'com'  # Default tld
        if target_lang == 'en':
            tld = target_accent if target_accent else 'com'

        # Convert translated text to speech in the target language with accent
        tts = gTTS(translated_text, lang=target_lang, tld=tld, slow=False)

        # Save the audio to a temporary file in the 'static' directory
        audio_filename = f"static/{uuid.uuid4()}.mp3"
        tts.save(audio_filename)

        return jsonify({'success': True, 'text': translated_text, 'audio_url': f'/{audio_filename}'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

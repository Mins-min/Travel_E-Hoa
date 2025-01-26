import pyttsx3
import googlemaps
import speech_recognition as sr
from googletrans import Translator
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app)

# Google Maps API key
gmaps = googlemaps.Client(key='AIzaSyDMr8KZNq76ugLFypas2l8Rn3bj1M8AETI')

# Text-to-Speech engine
engine = pyttsx3.init()

# Translator instance
translator = Translator()

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    text = request.json.get('text')
    language = request.json.get('language', 'en')

    # Get available voices and select one based on the language
    voices = engine.getProperty('voices')
    selected_voice = None
    for voice in voices:
        if language in voice.languages:  # Find voice for the given language
            selected_voice = voice
            break
    if selected_voice:
        engine.setProperty('voice', selected_voice.id)
    else:
        engine.setProperty('voice', voices[0].id)  # Default to first voice if not found

    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()
    return jsonify({"message": "Text-to-speech conversion successful"})

# API to convert speech to text
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Please speak...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Use Google's speech recognition to convert speech to text
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return jsonify({"text": text})
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError:
        print("Sorry, there was an issue with the speech service.")
        return jsonify({"error": "Speech service error"}), 500

def translate_text(text, target_language):
    # Translate the text
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Define the API endpoint for translation
@app.route('/translate', methods=['POST'])
def translate_api():
    try:
        # Get the data from the incoming POST request
        data = request.get_json()
        
        # Extract the 'text' and 'target_language' from the request data
        text = data.get('text')
        target_language = data.get('target_language')
        
        if not text or not target_language:
            return jsonify({"error": "Text and target_language are required"}), 400
        
        # Translate the text
        translated_text = translate_text(text, target_language)
        return jsonify({"translated_text": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API to send an emergency alert (play sound and notify users)
@app.route('/emergency', methods=['POST'])
def emergency():
    location = request.json.get('location')
    if not location:
        return jsonify({"error": "Location is required"}), 400
    # Here you could notify emergency contacts or trigger a sound on the frontend
    return jsonify({"message": "Emergency alert triggered!"})

if __name__ == '__main__':
    app.run(debug=True)

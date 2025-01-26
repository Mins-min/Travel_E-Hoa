import pyttsx3
import googlemaps
import speech_recognition as sr
from googletrans import Translator
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from geopy.geocoders import Nominatim
from googletrans import Translator

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

    engine.setProperty('voice', language)
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

    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source)
    
    print("Listening for speech...")
    # Listen to the user's speech
    audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        # Use Google's speech recognition to convert speech to text
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Sorry, there was an issue with the speech service.")


def translate_text(text, target_language):
    # Initialize the Translator object
    translator = Translator()
    
    # Translate the text
    translated = translator.translate(text, dest=target_language)
    
    # Return the translated text
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


# API to send an emergency alert (play sound and notify users)
@app.route('/emergency', methods=['POST'])
def emergency():
    location = request.json.get('location')
    # Here you could notify emergency contacts or trigger a sound on the frontend
    return jsonify({"message": "Emergency alert triggered!"})

if __name__ == '__main__':
    app.run(debug=True)


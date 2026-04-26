import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import wikipedia
import sounddevice as sd
import numpy as np
import io
import wave

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to make assistant speak
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# ✅ FIXED: listen() now uses sounddevice instead of PyAudio
def listen():
    r = sr.Recognizer()

    sample_rate = 16000
    chunk_size = 1024          # How many samples to read at a time
    silence_threshold = 500    # Volume level below this = silence
    silence_limit = 2          # Seconds of silence before stopping
    max_duration = 10          # Max seconds to record (safety limit)

    print("Listening... (speak now)")

    audio_chunks = []
    silent_chunks = 0
    speaking = False

    # How many silent chunks = silence_limit seconds
    max_silent_chunks = int((sample_rate / chunk_size) * silence_limit)
    max_chunks = int((sample_rate / chunk_size) * max_duration)

    try:
        with sd.InputStream(samplerate=sample_rate, channels=1,
                            dtype='int16', blocksize=chunk_size) as mic:
            while len(audio_chunks) < max_chunks:
                chunk, _ = mic.read(chunk_size)
                volume = np.abs(chunk).mean()  # Measure loudness

                if volume > silence_threshold:
                    # Sound detected — start/continue recording
                    speaking = True
                    silent_chunks = 0
                    audio_chunks.append(chunk.copy())

                elif speaking:
                    # Was speaking, now quiet — count silence
                    silent_chunks += 1
                    audio_chunks.append(chunk.copy())  # Keep trailing silence natural

                    if silent_chunks >= max_silent_chunks:
                        # Long enough silence = done speaking
                        break

        if not audio_chunks:
            speak("I didn't hear anything, please try again.")
            return ""

        # Build WAV from recorded chunks
        audio_data = np.concatenate(audio_chunks, axis=0)
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())
        wav_buffer.seek(0)

        # Transcribe
        with sr.AudioFile(wav_buffer) as source:
            audio = r.record(source)

        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand.")
        return ""

    except sr.RequestError:
        speak("Internet issue.")
        return ""

    except Exception as e:
        print("Microphone error:", e)
        speak("There was a problem with the microphone.")
        return ""

# Function to tell time and date
def tell_time_date():
    now = datetime.datetime.now()
    time = now.strftime("%H:%M")
    date = now.strftime("%d %B %Y")
    speak(f"Time is {time} and date is {date}")

# Function to search Google
def search_google(query):
    speak("Searching Google")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Function to open websites
def open_website(name):
    if "youtube" in name:
        webbrowser.open("https://youtube.com")
    elif "google" in name:
        webbrowser.open("https://google.com")
    else:
        speak("Website not recognized")

# Function to get weather
def get_weather(city):
    api_key = "YOUR_API_KEY_HERE"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            speak("City not found")
            return
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"{city} temperature is {temp} degree Celsius with {desc}")
    except:
        speak("Error fetching weather")

# Function to get info from Wikipedia
def ask_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("Couldn't find information")

# Reminder storage
reminders = []

def add_reminder(text):
    reminders.append(text)
    speak("Reminder added")

def show_reminders():
    if reminders:
        for r in reminders:
            speak(r)
    else:
        speak("No reminders")

# Main assistant loop
def run_assistant():
    speak("Hello, I am your assistant")

    while True:
        command = listen()

        if "hello" in command or "hi" in command:
            speak("Hey there!")
        elif "time" in command or "date" in command:
            tell_time_date()
        elif "search" in command:
            speak("What should I search?")
            query = listen()
            search_google(query)
        elif "open youtube" in command or "open google" in command:
            open_website(command)
        elif "weather" in command:
            speak("Which city?")
            city = listen()
            get_weather(city)
        elif "who is" in command or "what is" in command:
            ask_wikipedia(command)
        elif "reminder" in command:
            speak("What should I remind?")
            reminder = listen()
            add_reminder(reminder)
        elif "show reminders" in command:
            show_reminders()
        elif "stop" in command or "bye" in command:
            speak("Goodbye!")
            break
        else:
            speak("I didn't get that")

# Run the assistant
run_assistant()
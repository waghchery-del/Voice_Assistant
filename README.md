# Voice_Assistant
A Python voice assistant using sounddevice, speech_recognition, and pyttsx3

# 🎙️ Python Voice Assistant

A beginner-friendly voice assistant built with Python that works on **Python 3.14** — 
no PyAudio needed!

## Features
- 🗣️ Voice input using `sounddevice` (PyAudio-free)
- 🔊 Text-to-speech with `pyttsx3`
- 🌐 Google Search & website opening
- 🌤️ Live weather updates
- 📖 Wikipedia lookups
- ⏰ Time & date
- 📝 Reminders

## Installation

```bash
pip install speechrecognition pyttsx3 sounddevice numpy scipy requests wikipedia
```

## How to Run

```bash
python Voice_Assistant.py
```

## Note
This project uses `sounddevice` instead of `PyAudio` to fix 
compatibility issues with Python 3.14 on Windows.

Voice Chatbot and Fall Detection System
Overview
This project has two parts:

Voice Chatbot – lets the user talk to a chatbot using voice or text.

Fall Detection – checks for falls using webcam and body posture.

Voice Chatbot
Features
Voice input through microphone.

Converts speech to text using faster-whisper.

Uses DialoGPT to respond.

Speaks the response using gTTS.

Works in both terminal and GUI mode.

Remembers conversation using LangChain memory.

Requirements
Python 3.8 or higher

Install required packages:

nginx
Copy
Edit
pip install sounddevice torch transformers faster-whisper langchain gtts pygame
How to Run
Open your terminal or IDE.

Run:

nginx
Copy
Edit
python app.py
Choose gui or terminal when asked.

Fall Detection
What it Does
Uses webcam and MediaPipe to track body joints. It checks if the user has fallen by looking at posture and angles between joints.

Requirements
Python 3.8 or higher

Install required packages:

nginx
Copy
Edit
pip install opencv-python mediapipe numpy
How to Run
Make sure your webcam is on.

Run:

nginx
Copy
Edit
python fall_detection.py
Press q to quit.
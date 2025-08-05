import os
import queue
import tempfile
import numpy as np
import sounddevice as sd
import torch
from transformers import pipeline
from faster_whisper import WhisperModel
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from gtts import gTTS
import tkinter as tk
from threading import Thread
import pygame
import sys

# Initialize pygame mixer
pygame.mixer.init()

# Audio queue setup
q = queue.Queue()
def callback(indata, frames, time, status):
    q.put(indata.copy())

# Whisper model setup
print("Device set to use", "cuda" if torch.cuda.is_available() else "cpu")
whisper_model = WhisperModel("small", device="cpu", compute_type="int8")

# Load public LLM – No token required
llm = pipeline(
    "text-generation",
    model="microsoft/DialoGPT-medium",
    device=0 if torch.cuda.is_available() else -1
)

# Memory setup
memory = ConversationBufferMemory(return_messages=True)

# Record audio
def record_audio(duration=8, fs=16000):
    q.queue.clear()
    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        print("️ Speak now...")
        audio = np.concatenate([q.get() for _ in range(0, int(fs / 1024 * duration))], axis=0)
    return audio.flatten()

# Transcribe audio
def transcribe(audio_data):
    try:
        segments, _ = whisper_model.transcribe(audio_data, language="en", vad_filter=True)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
    except Exception as e:
        print(" Transcription error:", e)
        return ""

# Generate LLM response
def generate_response(user_input):
    history = ""
    for msg in memory.chat_memory.messages:
        if isinstance(msg, HumanMessage):
            history += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history += f"Assistant: {msg.content}\n"

    prompt = f"{history}\nUser: {user_input}\nAssistant:"

    try:
        output = llm(prompt, max_new_tokens=100, do_sample=True)[0]['generated_text']
        response = output.split("Assistant:")[-1].strip()
    except Exception as e:
        print(" LLM Generation error:", e)
        response = "Sorry, I couldn't process that."

    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(response)
    return response

# Text-to-speech using pygame
def speak_response(response):
    if not response.strip():
        print(" Empty response. Skipping TTS.")
        return
    try:
        tts = gTTS(response)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            pygame.mixer.music.load(fp.name)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
            pygame.mixer.music.unload()
            os.remove(fp.name)
    except Exception as e:
        print(f" TTS Error: {e}")

# Chatbot runner (voice)
def run_chatbot():
    try:
        audio = record_audio()
        user_input = transcribe(audio)
        print(f"\n️ You: {user_input}")

        if not user_input:
            print("️ No speech detected.")
            return

        if "exit" in user_input.lower():
            print(" Exiting.")
            root.quit()
            return

        response = generate_response(user_input)
        print(f" Bot: {response}")
        speak_response(response)
    except Exception as e:
        print(f" Error in chatbot: {e}")

# Terminal mode for text input
def run_terminal_chatbot():
    print(" Terminal Chat Mode (type 'exit' to quit)")
    while True:
        mode = input("Type 'speak' to use mic or 'type' to enter text: ").strip().lower()
        if mode == "exit":
            break
        elif mode == "type":
            user_input = input(" You: ").strip()
        elif mode == "speak":
            audio = record_audio()
            user_input = transcribe(audio)
            print(f"\n️ You: {user_input}")
        else:
            print(" Invalid mode. Type 'speak', 'type', or 'exit'.")
            continue

        if not user_input:
            print("️ No input detected.")
            continue

        response = generate_response(user_input)
        print(f" Bot: {response}")
        speak_response(response)

# GUI setup
def start_gui():
    global root
    root = tk.Tk()
    root.title("Voice Chatbot")
    root.geometry("400x200")
    root.configure(bg="#f0f0f0")

    label = tk.Label(root, text="️ Press the button to speak", font=("Arial", 14), bg="#f0f0f0")
    label.pack(pady=20)

    mic_button = tk.Button(root, text=" Speak", font=("Arial", 16), bg="#4caf50", fg="white", command=lambda: Thread(target=run_chatbot).start())
    mic_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", font=("Arial", 12), bg="#f44336", fg="white", command=root.quit)
    exit_button.pack(pady=5)

    print(" Voice Assistant Ready. Press 'Speak' in the GUI or run terminal mode.")
    root.mainloop()

# Entry point
if __name__ == "__main__":
    mode = input("Start in 'gui' or 'terminal' mode? ").strip().lower()
    if mode == "terminal":
        run_terminal_chatbot()
    else:
        start_gui()

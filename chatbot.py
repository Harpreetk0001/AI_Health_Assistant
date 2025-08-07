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
import pygame
import requests

def save_conversation_to_api(user_input, response):
    try:
        payload = {
            "user_message": user_input,
            "bot_response": response
        }
        r = requests.post("http://localhost:8000/conversations/", json=payload)
        if r.status_code == 200:
            print(" Conversation saved")
        else:
            print(" Failed to save:", r.text)
    except Exception as e:
        print("API error:", e)

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
        print("LLM error:", e)
        response = "Sorry, I couldn't process that."

    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(response)

    #  Save to backend API
    save_conversation_to_api(user_input, response)

    return response

# Init
pygame.mixer.init()
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(indata.copy())

print("Device set to use", "cuda" if torch.cuda.is_available() else "cpu")
whisper_model = WhisperModel("small", device="cpu", compute_type="int8")
llm = pipeline("text-generation", model="microsoft/DialoGPT-medium", device=0 if torch.cuda.is_available() else -1)
memory = ConversationBufferMemory(return_messages=True)

def record_audio(duration=8, fs=16000):
    q.queue.clear()
    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        print("️Speak now...")
        audio = np.concatenate([q.get() for _ in range(0, int(fs / 1024 * duration))], axis=0)
    return audio.flatten()

def transcribe(audio_data):
    try:
        segments, _ = whisper_model.transcribe(audio_data, language="en", vad_filter=True)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
    except Exception as e:
        print(" Transcription error:", e)
        return ""

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
        print("LLM error:", e)
        response = "Sorry, I couldn't process that."
    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(response)
    return response

def speak_response(response):
    if not response.strip():
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
        print(f"TTS Error: {e}")

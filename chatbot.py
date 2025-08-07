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
import os
from threading import Thread

# Globals
whisper_model = None
llm = None
memory = None
q = queue.Queue()

def initialize():
    global whisper_model, llm, memory
    pygame.mixer.init()
    print("Loading models...")
    whisper_model = WhisperModel("small", device="cpu", compute_type="int8")
    llm = pipeline("text-generation", model="microsoft/DialoGPT-medium", device=0 if torch.cuda.is_available() else -1)
    memory = ConversationBufferMemory(return_messages=True)
    print("Models loaded!")

def generate_response(user_input):
    if not llm or not memory:
        raise Exception("Chatbot not initialized! Call initialize() first.")

    # Only keep recent history to avoid long prompt issues
    history = ""
    for msg in memory.chat_memory.messages[-4:]:
        if isinstance(msg, HumanMessage):
            history += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history += f"Assistant: {msg.content}\n"

    prompt = f"{history}User: {user_input}\nAssistant:"

    try:
        output = llm(prompt, max_new_tokens=100, do_sample=True)[0]['generated_text']
        if output.startswith(prompt):
            response = output[len(prompt):].strip()
        else:
            response = output.strip()
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

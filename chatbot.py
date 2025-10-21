import requests

def initialize():
    print("Chatbot initialized.")

def generate_response(user_input):
    """
    Send user input to Rasa REST endpoint and return the first response text.
    """
    try:
        response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "medbuddy", "message": user_input},
            timeout=5  # avoid hanging
        )
        messages = response.json()  # list of dicts
        if messages:
            # Rasa can return multiple messages; concatenate them
            return " ".join([msg.get("text", "") for msg in messages if "text" in msg])
        else:
            return "Sorry, I didn't understand that."
    except requests.exceptions.RequestException as e:
        print("Error contacting Rasa:", e)
        return "Chatbot service is unavailable."

def speak_response(response_text):
    """
    Optional: you can integrate TTS here, e.g., pyttsx3 or any library.
    """
    print("Bot says:", response_text)

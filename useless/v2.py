import serial
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()
# Replace with your COM port
PORT = "COM9"
BAUD = 9600

# Your OpenAI API Key
API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI API endpoint for Chat Completions
API_URL = "https://api.openai.com/v1/chat/completions"

def generate_event(era):
    prompt = f"Create a single absurd and funny historical event in the {era} era."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "gpt-4o-mini",  # or "gpt-4.0"
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 50
    }

    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    
    # Extract the generated text
    return result["choices"][0]["message"]["content"].strip()

# Connect to Arduino
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print("Connected to Arduino.")

while True:
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        if line.startswith("GEN:"):
            era = line[4:]
            print(f"Generating event for: {era}")
            event = generate_event(era)
            ser.write((event + "\n").encode())
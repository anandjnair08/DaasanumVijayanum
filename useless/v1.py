import serial
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()


# Replace with your COM port
PORT = "COM9"
BAUD = 9600

# Your API key (paste yours here safely)
API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI Chat API endpoint
API_URL = "https://api.openai.com/v1/chat/completions"

def generate_event(era):
    # Create prompt
    prompt = f"Create a single absurd and funny historical event in the {era} era."

    # API request payload
    payload = {
        "model": "gpt-4o-mini",  # You can also try "gpt-4.1" or "gpt-4.1-mini"
        "messages": [
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 50
    }

    # API request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Send request to OpenAI
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Connect to Arduino
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print("Connected to Arduino.")

# Main loop
while True:
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        if line.startswith("GEN:"):
            era = line[4:]
            print(f"Generating event for: {era}")
            event = generate_event(era)
            print(f"Sending to Arduino: {event}")
            ser.write((event + "\n").encode())
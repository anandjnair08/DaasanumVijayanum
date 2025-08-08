from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure you have set your OpenAI API key in .env file

# Initialize the OpenAI client with OpenRouter settings
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # OpenRouter base URL
    api_key=API_KEY  # Replace with your OpenRouter API key
)

# Create a chat completion request
completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "https://your-site-url.com",  # Optional: Replace with your site URL
        "X-Title": "Your Site Name"  # Optional: Replace with your site name
    },
    model="openai/gpt-4o",  # Replace with the desired model
    messages=[
        {
            "role": "user",
            "content": "Why is the earth flat?"
        }
    ],
    max_tokens=100  # Reduce the token limit to fit within your credits
)

# Print the response content
print(completion.choices[0].message.content)

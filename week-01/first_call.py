from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

response = client.chat.completions.create(
   model="llama-3.3-70b-versatile",
    messages = [ #list of dictionaries that represent the conversation history
        {"role": "user", "content": "I already have the groq Python package installed and my API key in a .env file. Write a script that connects to Groq API and prints the response."
         }
    ]
)

print(response.choices[0].message.content)
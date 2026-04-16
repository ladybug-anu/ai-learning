from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

print('Anu Bot: ', end = "", flush = True)

stream = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages = [
        {
        "role": "system",
        "content": "you are a helpful assistant, keep response of 100 words"
        },
        {"role": "user",
         "content": "Explain how internet works"}
    ],
    stream=True

)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content is not None:
        print(content , end = "")

print('\n')
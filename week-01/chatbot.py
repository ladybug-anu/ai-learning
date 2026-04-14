from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

conversation_history = []

system_message = "you are an assistant named AnuBot. You are concise and friendly"

print("AnuBot is ready, type \'quit\' to exit")

while True:
    user_input = input("You: ")

    if user_input.lower() == 'quit':
        print('Anu Bot says Bye!')
        break

    conversation_history.append({
        'role': 'user',
        'content': user_input
    })

    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'system', 'content':system_message}
        ] + conversation_history

    ) 
    bot_reply = response.choices[0].message.content

    conversation_history.append({
        'role': 'assistant',
        'content': bot_reply
    })

    print(f"AnuBot: {bot_reply}\n")
    
      
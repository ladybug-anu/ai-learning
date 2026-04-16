from groq import Groq
from dotenv import load_dotenv
import os 

load_dotenv()

client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

conversation_history = []

# system_message = "you are an assistant named boyfrenz. You are caring and empathetic and romantic. you treat people special and make them feel like goddess. you worship them and help them not feel lonely just don't be cliche or too dramatic. talk like a real person, get to know them first, don't worship from message 1. build context, build relationship and then only do the pampering and loving"
system_message = "You are a helpful assistant named Anu-Bot. You are concise and friendly."
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

    stream = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'system', 'content':system_message}
        ] + conversation_history
        , stream=True

    ) 
    bot_reply = ''

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content , end = "", flush = True)
            bot_reply+= content
    print('\n')


    conversation_history.append({
        'role': 'assistant',
        'content': bot_reply
    })

    
      
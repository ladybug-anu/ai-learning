from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# user_text = "I need to create a login page by Friday. It is high priority. Also need to fix a memory leak bug, medium priority, no deadline"
user_text = "i need to sort my life. gym 2 hours, send agent testing report today, cook for 2-3 hours daily, go to office daily, order curtains, set up garden"
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages = [
        {
        "role": "system",
        "content": "You are a task extraction assistant, extract tasks from the user's message and return only a "
        "json array nothing else. no explanation, no markdown, no backticks, just raw json. "
        "each task should have title, priority, deadline or null if not mentioned."
        },
        {
            "role": "user",
            "content": user_text
        }
    ]
)
raw = response.choices[0].message.content
print("Raw: ", raw)

try: #to handle scenarios if LLM returns something apart from json
    tasks = json.loads(raw)
except json.JSONDecodeError:
    #clean it up or retry
    pass
print("Parsed Tasks: /n")
for task in tasks:
    print(f"- {task['title']} | Priority: {task['priority']} | Deadline: {task['deadline']}")
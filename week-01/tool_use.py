from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

def get_weather(city: str) -> str:
    fake_weather = {
         "bangalore": "28°C, partly cloudy, humidity 65%",
        "mumbai": "32°C, humid, humidity 85%",
        "delhi": "35°C, sunny, humidity 40%",
        "chennai": "30°C, cloudy, humidity 75%"
    }
    return fake_weather.get(city.lower(), 'Weather data not available for this city')


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
                 "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

messages = [
    {"role": "user", "content": "What's the weather like in Bangalore today?"}
]


response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools
)

response_message = response.choices[0].message
print("Step 1 - AI decided to call:")
print(response_message.tool_calls)

tool_call = response_message.tool_calls[0]
tool_name = tool_call.function.name
tool_args = json.loads(tool_call.function.arguments)


print(f"\nStep 2 - Running function: {tool_name}({tool_args})")
tool_result = get_weather(tool_args["city"])
print(f"Function returned: {tool_result}")

messages.append(response_message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": tool_result
})

final_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools
)

print(f"\nStep 3 - Final answer:")
print(final_response.choices[0].message.content)
from groq import Groq
from dotenv import load_dotenv
import os
import json
import datetime

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

def get_time(city: str) -> str:
    fake_time = {
         "bangalore": "10 pm",
        "mumbai": "11pm",
        "delhi": "9 pm",
        "chennai": "3 pm"
    }
    return fake_time.get(city.lower(), 'Time data not available for this city')

tools = [
   {
    "type": "function",          # "this is a function"
    "function": {
        "name": "get_weather",   # "its name is get_weather"
        "description": "Get current weather for a city",  # "this is what it does"
        "parameters": {          # "this is what it needs as input"
            "type": "object",    # "the input is a collection of fields"
            "properties": {
                "city": {                           # "one field called city"
                    "type": "string",               # "it's a string"
                    "description": "The city name"  # "this is what it means"
                }
            },
            "required": ["city"]  # "city is mandatory, not optional"
        }
    }
},
    {
        
        "type": "function",
        "function": {
            "name": "get_time",
                 "description": "Get current time for a city",
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

"""
template for tools functions
{
    "type": "function",
    "function": {
        "name": "YOUR_FUNCTION_NAME",
        "description": "WHAT IT DOES IN ONE LINE",
        "parameters": {
            "type": "object",
            "properties": {
                "PARAM_1": {
                    "type": "string",
                    "description": "WHAT THIS PARAM MEANS"
                },
                "PARAM_2": {
                    "type": "number", 
                    "description": "WHAT THIS PARAM MEANS"
                }
            },
            "required": ["PARAM_1"]
        }
    }
}"""

messages = [
    {"role": "user", "content": "What's the weather and time in Bangalore today?"}
]


response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    # model="mixtral-8x7b-32768",
    messages=messages,
    tools=tools
)

response_message = response.choices[0].message
print("Step 1 - AI decided to call:")
print(response_message.tool_calls)

available_tools = {
    "get_weather": get_weather,
    "get_time": get_time
}

messages.append(response_message)

for tool_call in response_message.tool_calls:
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)


    print(f"\nStep 2 - Running function: {tool_name}({tool_args})")
    # if tool_name == 'get_weather':
    #     tool_result = get_weather(tool_args["city"])
    # elif tool_name == 'get_time':
    #     tool_result = get_time(tool_args["city"])
    tool_result = available_tools[tool_name](tool_args["city"])
    print(f"Function returned: {tool_result}")

    
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
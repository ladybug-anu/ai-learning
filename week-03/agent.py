from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ── Tools ─────────────────────────────────────────────
def get_weather(city: str) -> str:
    # Fake implementation for now — we'll make it real later
    weather = {
        "bangalore": "28°C, partly cloudy, humidity 65%",
        "mumbai": "32°C, humid, chance of rain",
        "delhi": "35°C, sunny, very hot",
    }
    return weather.get(city.lower(), f"No weather data for {city}")

def get_news(topic: str) -> str:
    # Fake implementation for now
    news = {
        "ai": "OpenAI released new model. Google announced Gemini updates. Anthropic raised funding.",
        "cricket": "India won the test match. Virat Kohli scored century. IPL auction next month.",
        "bangalore": "Metro extended to Whitefield. New tech park opening in Devanahalli.",
    }
    return news.get(topic.lower(), f"No news found for {topic}")

def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Could not calculate: {e}"

# ── Tool definitions for LLM ──────────────────────────
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Get latest news on a topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "News topic"}
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression to evaluate"}
                },
                "required": ["expression"]
            }
        }
    }
]

available_tools = {
    "get_weather": get_weather,
    "get_news": get_news,
    "calculate": calculate,
}

# ── Agent loop ────────────────────────────────────────
def run_agent(user_input: str) -> str:
    print(f"\n🤔 Thinking about: {user_input}")
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use tools to answer questions. You can call multiple tools if needed."},
        {"role": "user", "content": user_input}
    ]
    
    # ReAct loop — keep going until LLM stops calling tools
    step = 0
    max_steps = 5  # safety limit so it never loops forever
    
    while step < max_steps:
        step += 1
        print(f"\n── Step {step} ──")
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools
        )
        
        message = response.choices[0].message
        
        # If no tool calls — LLM has its final answer
        if not message.tool_calls:
            print(f"✓ Done in {step} steps")
            return message.content
        
        # Otherwise — execute each tool it called
        messages.append(message)
        
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            print(f"🔧 Calling: {name}({args})")
            result = available_tools[name](**args)
            print(f"📦 Result: {result}")
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
    
    return "Reached maximum steps without a final answer."

# ── Run ───────────────────────────────────────────────
print("Agent ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "quit":
        break
    answer = run_agent(user_input)
    print(f"\nAgent: {answer}\n")
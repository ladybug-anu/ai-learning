from groq import Groq
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ── Tools ─────────────────────────────────────────────
def get_weather(city: str) -> str:
    weather = {
        "bangalore": "28°C, partly cloudy, humidity 65%",
        "bengaluru": "28°C, partly cloudy, humidity 65%",
        "mumbai": "32°C, humid, chance of rain",
        "delhi": "35°C, sunny, very hot",
    }
    city_clean = city.lower().strip()
    for key in weather:
        if key in city_clean or city_clean in key:
            return weather[key]
    return f"No weather data for {city}"

def get_news(topic: str) -> str:
    api_key = os.environ.get("NEWS_API_KEY")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "sortBy": "publishedAt",
        "pageSize": 3,
        "language": "en",
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] != "ok":
        return f"Could not fetch news for {topic}"
    articles = data["articles"]
    if not articles:
        return f"No news found for {topic}"
    results = []
    for a in articles:
        results.append(f"- {a['title']} ({a['source']['name']})")
    return f"Latest news about {topic}:\n" + "\n".join(results)

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
            "description": "Get the current weather conditions for a specific city. Use this when the user asks about weather, temperature, or climate in a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get weather for, e.g. 'Bangalore', 'Mumbai', 'Delhi'"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Get the latest news articles about a specific topic or subject. Use this when the user asks about news, current events, or recent developments on any topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to search news for, e.g. 'artificial intelligence', 'cricket', 'stock market'"
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression and return the result. Use this for any arithmetic, calculations, or math problems.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A valid Python mathematical expression to evaluate, e.g. '28 - 32', '100 * 1.18', '(5 + 3) * 2'"
                    }
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
        {"role": "system", "content": "You are a helpful assistant. Use tools to answer questions. When you get tool results, always include the actual content from the results in your final answer — don't just summarise, show the real data."},
        {"role": "user", "content": user_input}
    ]

    step = 0
    max_steps = 5

    while step < max_steps:
        step += 1
        print(f"\n── Step {step} ──")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message

        if not message.tool_calls:
            print(f"✓ Done in {step} steps")
            return message.content

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

    return "Reached maximum steps."


# ── Run ───────────────────────────────────────────────
print("Agent ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "quit":
        break
    answer = run_agent(user_input)
    print(f"\nAgent: {answer}\n")
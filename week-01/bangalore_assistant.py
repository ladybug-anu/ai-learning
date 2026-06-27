from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ── DATA ──────────────────────────────────────────────────────────────────────

areas = {
    "indiranagar": "Upscale neighbourhood, great pubs, cafes, 100 Feet Road is the main strip. Very walkable.",
    "koramangala": "Startup hub, lots of restaurants, young crowd. 5th and 7th block are the busiest.",
    "whitefield": "IT corridor, far from centre, lots of tech parks. Traffic is brutal.",
    "jayanagar": "Old Bangalore charm, great South Indian food, peaceful residential area.",
    "hsr layout": "Chill neighbourhood, lots of startups, good food scene, close to Electronic City.",
    "mg road": "City centre, metro accessible, shopping, pubs, Brigade Road nearby.",
    "electronic city": "Major IT hub, Infosys/Wipro campuses, far south, use NICE road to avoid traffic.",
}

food = {
    "indiranagar": ["Truffles - best burgers", "Toit - microbrewery must visit", "Brahmin's Coffee Bar - iconic breakfast"],
    "koramangala": ["Meghana Foods - biryani", "The Egg Factory", "Windmills Craftworks - beer and music"],
    "jayanagar": ["MTR - legendary South Indian", "Veena Stores - idli vada", "Brahmin's - filter coffee"],
    "hsr layout": ["Onesta - pizza", "Hole in the Wall Cafe", "Smacznego - European food"],
    "mg road": ["Koshy's - old school Bangalore cafe", "The 13th Floor - rooftop bar", "Ebony - rooftop restaurant"],
}

traffic = {
    "whitefield": "Avoid 8-10am and 6-9pm. Use Outer Ring Road or NICE Road. Metro not yet fully connected.",
    "electronic city": "Use NICE Road elevated highway — saves 45 mins vs Hosur Road during peak hours.",
    "mg road": "Metro is your best bet. Parking is a nightmare. Blue and Purple lines connect here.",
    "koramangala": "No metro. Autos and cabs only. Avoid during rain — floods easily.",
    "indiranagar": "Metro on Purple line. 100 Feet Road jams up after 6pm.",
}

tech_companies = {
    "whitefield": ["Microsoft", "SAP", "IBM", "Nvidia"],
    "electronic city": ["Infosys HQ", "Wipro", "HCL"],
    "outer ring road": ["Google", "LinkedIn", "Cisco", "Samsung R&D"],
    "koramangala": ["Flipkart (old office)", "many funded startups"],
    "hsr layout": ["Swiggy HQ", "many early stage startups"],
}

weekend = [
    "Cubbon Park - morning walks, very peaceful",
    "Lalbagh Botanical Garden - flowers and glass house",
    "Nandi Hills - 60km out, sunrise trek, leave by 5am",
    "Innovative Film City - day out",
    "Wonderla - amusement park on Mysore Road",
    "Brewery hopping - Toit, Arbor, Windmills, Craftworks",
    "Commercial Street / Brigade Road - shopping",
]

local_tips = [
    "Auto drivers rarely use meter — always use Rapido or Namma Yatri app for fair prices",
    "Namma Metro is expanding fast — check latest map before planning routes",
    "Weather: Oct-Feb is pleasant, Mar-May gets hot, Jun-Sep is rainy season",
    "Kannada is the local language — learning 'Dhanyavadagalu' (thank you) goes a long way",
    "Most areas have power cuts in summer — keep laptop charged",
    "Bangalore shuts early compared to Mumbai — most places close by 11pm",
    "UPI works everywhere — even street food stalls",
]

# ── TOOLS ─────────────────────────────────────────────────────────────────────

def get_area_info(area: str) -> str:
    area = area.lower()
    for key in areas:
        if key in area or area in key:
            return areas[key]
    return f"No info available for {area}. Known areas: {', '.join(areas.keys())}"

def get_food_recommendations(area: str) -> str:
    area = area.lower()
    for key in food:
        if key in area or area in key:
            places = food[key]
            return f"Food in {key.title()}: " + " | ".join(places)
    return f"No food data for {area}. Try: {', '.join(food.keys())}"

def get_traffic_info(area: str) -> str:
    area = area.lower()
    for key in traffic:
        if key in area or area in key:
            return traffic[key]
    return f"No traffic data for {area}. Try: {', '.join(traffic.keys())}"

def get_tech_companies(area: str) -> str:
    area = area.lower()
    for key in tech_companies:
        if key in area or area in key:
            companies = tech_companies[key]
            return f"Companies in {key.title()}: {', '.join(companies)}"
    return f"No company data for {area}. Try: {', '.join(tech_companies.keys())}"

def get_weekend_activities() -> str:
    return "Weekend ideas in Bangalore:\n" + "\n".join(f"- {w}" for w in weekend)

def get_local_tips() -> str:
    return "Bangalore local tips:\n" + "\n".join(f"- {t}" for t in local_tips)

# ── TOOLS LIST ────────────────────────────────────────────────────────────────

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_area_info",
            "description": "Get information about a Bangalore neighbourhood or area",
            "parameters": {
                "type": "object",
                "properties": {
                    "area": {"type": "string", "description": "The area or neighbourhood name"}
                },
                "required": ["area"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_food_recommendations",
            "description": "Get food and restaurant recommendations for a Bangalore area",
            "parameters": {
                "type": "object",
                "properties": {
                    "area": {"type": "string", "description": "The area to get food recommendations for"}
                },
                "required": ["area"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_traffic_info",
            "description": "Get traffic and commute tips for a Bangalore area",
            "parameters": {
                "type": "object",
                "properties": {
                    "area": {"type": "string", "description": "The area to get traffic info for"}
                },
                "required": ["area"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tech_companies",
            "description": "Get tech companies and offices located in a Bangalore area",
            "parameters": {
                "type": "object",
                "properties": {
                    "area": {"type": "string", "description": "The area to get company info for"}
                },
                "required": ["area"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weekend_activities",
            "description": "Get weekend activity and hangout suggestions in Bangalore",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_local_tips",
            "description": "Get local tips, culture advice and practical info about living in Bangalore",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

available_tools = {
    "get_area_info": get_area_info,
    "get_food_recommendations": get_food_recommendations,
    "get_traffic_info": get_traffic_info,
    "get_tech_companies": get_tech_companies,
    "get_weekend_activities": lambda: get_weekend_activities(),
    "get_local_tips": lambda: get_local_tips(),
}

# ── MAIN LOOP ─────────────────────────────────────────────────────────────────

conversation_history = []

system_message = """You are BLR-Bot, a friendly and witty local guide for Bangalore. 
You have tools to answer questions about areas, food, traffic, tech companies, weekend activities and local tips.
Always use your tools when the question is about Bangalore — don't answer from memory.
ONLY use information returned by your tools. Never add information from your own training data.
If the tool doesn't have the information, say so — don't fill gaps from memory.
Be conversational, add local flavour, and keep responses concise."""

print("🤖 BLR-Bot ready! Ask me anything about Bangalore. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("BLR-Bot: Swalpa adjust maadi! Bye! 👋")
        break

    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_message}] + conversation_history,
        tools=tools
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        conversation_history.append(response_message)

        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if tool_args:
                tool_result = available_tools[tool_name](**tool_args)
            else:
                tool_result = available_tools[tool_name]()

            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })

        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_message}] + conversation_history,
            stream=True
        )

        print("BLR-Bot: ", end="", flush=True)
        bot_reply = ""
        for chunk in final_response:
            content = chunk.choices[0].delta.content
            if content is not None:
                print(content, end="", flush=True)
                bot_reply += content
        print("\n")

    else:
        print("BLR-Bot: ", end="", flush=True)
        bot_reply = response_message.content
        print(bot_reply)
        print()

    conversation_history.append({"role": "assistant", "content": bot_reply})
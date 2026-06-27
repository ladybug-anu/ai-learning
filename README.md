# ai-learning
Anu learns AI and documents whatever is there

**bangalore_assistant.py**
This project is a Bot that acts as an assistant for Bangalore. It tells things like local tips, weekend plans, tech companies, areas, food. It fetches data from hard coded functions, uses LLM to decipher user input and decide which function to call, and runs that and gives the answer in natural language. It does not use any training data or internet for now, just the functions that are defined. It also displays output in streaming pattern and is an interactive bot.

# BLR-Bot 🤖

A Bangalore local guide chatbot built with tool use / function calling.

The LLM reads the user's question, decides which function to call, 
and answers using only the data returned by that function — no training 
data, no internet. Output streams in real time.

## What it covers
- Neighbourhoods, food, traffic, tech companies, weekend activities, local tips

## Tech
- Groq API (llama-3.3-70b-versatile)
- Tool use / function calling
- Streaming responses
- Python 3.11

## Run it
pip install groq python-dotenv
Add GROQ_API_KEY to .env
python bangalore_assistant.py
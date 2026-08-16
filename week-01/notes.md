**day 1- 13th april 2026**
    1. set up environment - vs code, python, git, repo, groq api
    2. created a script that sends a prompt to groq and prints its response to the screen
    3. Learnt what venv is and why we use it
    4. Learnt what API keys are and why they need to be kept private
    5. Learnt what tokens in API calls are
    6. Hit a model deprecation error and fixed it by reading error message and used different model
    7. AI agents - chatgpt, copilot, claude etc are just code + api calls + display

**day 2 14th april 2026**
    1. understood AI has no memory by default
    2. the way to have a memory is to send entire conversation history and then get response as per that.
    3. 3 roles user, assistant, system
    4. system message - firm hard coded rules for AI, no one can override them mid conversation
    5. built a working chatbot terminal and can set personalities 
    6. learnt about context window limits and token accumulation problem
    7. Prompt injection is overriding system message mid conversation

**day 3 15th april 2026**
    1. Learned the difference between gen output and structured output
    2. AI can return only json which we can parse and use for our work
    3. System prompt controls output strictly
    4. Output reliability that is based on this is a real challenge
    5. json.loads() parses AI response into python objects
    6. Production apps need to have try catch around JSON parsing in case LLM sent more than what we asked for

**day 4 16th april 2026**
    1. time to first token, how much time before user sees first word in a streaming response
    2. streaming chunks
    3. flush, stream, delta, flush means display as it comes, stream means send as soon as generated, delta is the difference 
    4. made streaming chatbot
    
**day 5 21st april 2026**
    1. AI can't run code itself, it decides which function to call and then we run it from our script
    2. tools list is a function description for AI to read and understand what tools we have available for what use
    3. tool calls is AI decision of which function to call and what parameters to give
    4. available tools dict is cleaner way to call functions if multiple tools are present
    5. functions are first class objects and can be stored in dicts
    6. messages. append for response happens outside loop
    7. tool result inside loop for each tool that is being called
    
**day 6 28th June 2026**
RAG day 1:
- embeddings = text converted to numbers (384 dimensions)
- similar meaning = similar numbers = close in vector space
- chromadb stores chunks + their vectors
- retrieval = embed question, find closest chunks
- LLM only sees those chunks, not the whole PDF
- "I don't have that information" = grounding working correctly
Model used for embedding - all-MiniLM-L6-v2. this is small, fast and has 384 dimensions, other models like OpenAI text3-embedding-3-small has 1536 and text-embedding-3-large has 3072 dimensions

made interactive pdf reader
then proceed to add memory to it 
resources can get exhausted so put limits to conversation history and added rolling window as a trade off between memory and tokens. 

additionally, added query rewriting in case of vague follow up questions.

**day 7 29th June 2026**
1. increased rolling window limits to preserve more memory
2. added reference to the original doc - gives excerpts in interactive-pdf-reader-memory-citation and then give page numbers, will probably refine this later

**day 8 30th june 2026**
deployed on Streamlit UI
I had a stale state bug across sessions in a multi-tenant context, traced it to a hardcoded collection name, fixed it with a delete-then-create pattern

**day 9 1st july 2026**
ReAct program, code running, need to understand

**day 10 8th July 2026**
Chunk text function:
- range step = size - overlap (not size)
- slice = text[i:i+size] (always full size)
- overlap only affects where next chunk STARTS
- string slicing: text[start:end]
- snake_case not camelCase in Python
- try/except around risky operations (user input, type conversion)


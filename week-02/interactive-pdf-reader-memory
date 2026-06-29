from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import chromadb
import re
import os

load_dotenv()

# ── Models and clients ────────────────────────────────
model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ── Step 1: Load and clean PDF ────────────────────────
def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = [p.extract_text() for p in reader.pages if p.extract_text()]
    raw = "\n".join(pages)
    cleaned = re.sub(r'(?<=[a-zA-Z]) (?=[a-zA-Z])', '', raw)
    cleaned = re.sub(r' -(?=[a-zA-Z])', '-', cleaned)
    return cleaned

# ── Step 2: Chunk ─────────────────────────────────────
def chunk_text(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start : start + size])
        start += size - overlap
    return chunks

# ── Step 3: Index into ChromaDB ───────────────────────
def build_index(chunks: list[str]) -> chromadb.Collection:
    client = chromadb.Client()
    collection = client.create_collection("sadhesati")
    embeddings = model.encode(chunks).tolist()
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    return collection

def rewrite_query(query: str, history: list) -> str:
    if not history:
        return query  # no history yet, use as is
    
    system = "You are a helpful assistant. Rewrite the user's question into a standalone, self-contained search query based on the conversation history. Return ONLY the rewritten query, nothing else."
    
    messages = history[-4:] + [{"role": "user", "content": f"Rewrite this into a standalone question: {query}"}]
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + messages
    )
    return response.choices[0].message.content

def summarise_history(history: list) -> list:
    if len(history) < 8:
        return history  # not long enough to summarise yet
    
    conversation = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in history
    )
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"Summarise this conversation in 5 sentences, preserving all key facts and points discussed:\n\n{conversation}"
        }]
    )
    
    summary = response.choices[0].message.content
    
    # Replace full history with just the summary as a system-style message
    return [{"role": "assistant", "content": f"Summary of our conversation so far: {summary}"}]


# ── Step 4: Answer a question ─────────────────────────
def answer(query: str, collection: chromadb.Collection, history: list) -> str:
    # Retrieve relevant chunks for this question
    # query_embedding = model.encode([query]).tolist()
    search_query = rewrite_query(query, history)
    query_embedding = model.encode([search_query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=3)
    chunks_found = results["documents"][0]
    context = "\n\n---\n\n".join(chunks_found)

    # Build the system prompt with context injected
    system = f"""You are a helpful assistant that answers questions about a Sadesati report.
Answer using ONLY the context below. If the answer isn't there, say "I don't have that information."
Never make things up.

Context from the document:
{context}"""

    # Add current question to history
    history.append({"role": "user", "content": query})

    # Call LLM with full history + system prompt
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + history
    )
    
    reply = response.choices[0].message.content
    
    # Add reply to history
    history.append({"role": "user", "content": query})

    # Keep only last 6 messages (3 turns)
    if len(history) > 10:
        history = history[-10:]

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + history
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    return reply
    
    

# ── Run ───────────────────────────────────────────────
text = load_pdf("sadhesati.pdf")
chunks = chunk_text(text)
collection = build_index(chunks)
print(f"Ready. Indexed {len(chunks)} chunks.\n")

history = []
while True:
    query = input("Ask: ").strip()
    if query.lower() == "quit":
        break
    print(f"\n{answer(query, collection, history)}\n")
    history = summarise_history(history)
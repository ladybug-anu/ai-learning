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
def load_pdf(path: str) -> tuple[str, list[str]]:
    reader = PdfReader(path)
    pages = [p.extract_text() for p in reader.pages if p.extract_text()]
    cleaned_pages = []
    for page in pages:
        cleaned = re.sub(r'(?<=[a-zA-Z]) (?=[a-zA-Z])', '', page)
        cleaned = re.sub(r' -(?=[a-zA-Z])', '-', cleaned)
        cleaned_pages.append(cleaned)
    full_text = "\n".join(cleaned_pages)
    return full_text, cleaned_pages

# ── Step 2: Chunk ─────────────────────────────────────
def chunk_text(text: str, pages: list[str], size: int = 500, overlap: int = 50) -> tuple[list[str], list[int]]:
    chunks, chunk_pages, start, page_idx = [], [], 0, 0
    full_text = "\n".join(pages)
    
    # Track which page each character belongs to
    page_boundaries = []
    pos = 0
    for i, page in enumerate(pages):
        page_boundaries.append((pos, pos + len(page), i + 1))
        pos += len(page) + 1
    
    def get_page(char_pos):
        for start_p, end_p, num in page_boundaries:
            if start_p <= char_pos < end_p:
                return num
        return 1
    
    while start < len(full_text):
        chunks.append(full_text[start : start + size])
        chunk_pages.append(get_page(start))
        start += size - overlap
    
    return chunks, chunk_pages
# build index
def build_index(chunks: list[str], chunk_pages: list[int]) -> chromadb.Collection:
    client = chromadb.Client()
    collection = client.create_collection("sadhesati")
    embeddings = model.encode(chunks).tolist()
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"page": p} for p in chunk_pages]
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
    search_query = rewrite_query(query, history)
    query_embedding = model.encode([search_query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=3)
    chunks_found = results["documents"][0]
    pages_found = [m["page"] for m in results["metadatas"][0]]
    context = "\n\n---\n\n".join(chunks_found)

    system = f"""You are a helpful assistant that answers questions about a Sadesati report.
Answer using ONLY the context below. If the answer isn't there, say "I don't have that information."
Never make things up.

Context from the document:
{context}"""

    history.append({"role": "user", "content": query})

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + history
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    sources = [f"Page {pages_found[i]}: ...{chunks_found[i][:80]}..." for i in range(len(chunks_found))]
    source_text = "\n".join(f"[{i+1}] {s}" for i, s in enumerate(sources))
    return f"{reply}\n\nSources:\n{source_text}"
    
    

# ── Run ───────────────────────────────────────────────
# ── Run ───────────────────────────────────────────────
if __name__ == "__main__":
    text, pages = load_pdf("sadhesati.pdf")
    chunks, chunk_pages = chunk_text(text, pages)
    collection = build_index(chunks, chunk_pages)
    print(f"Ready. Indexed {len(chunks)} chunks.\n")

    history = []

    while True:
        query = input("Ask: ").strip()
        if query.lower() == "quit":
            break
        print(f"\n{answer(query, collection, history)}\n")
        history = summarise_history(history)
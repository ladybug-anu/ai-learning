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

# ── Step 4: Answer a question ─────────────────────────
def answer(query: str, collection: chromadb.Collection) -> str:
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=3)
    chunks_found = results["documents"][0]
    context = "\n\n---\n\n".join(chunks_found)

    prompt = f"""Answer the question using ONLY the context below.
If the answer isn't in the context, say "I don't have that information."
Never make things up.

Context:
{context}

Question: {query}

Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ── Run ───────────────────────────────────────────────
text = load_pdf("sadhesati.pdf")
chunks = chunk_text(text)
collection = build_index(chunks)
print(f"Ready. Indexed {len(chunks)} chunks.\n")

# Interactive loop
while True:
    query = input("Ask: ").strip()
    if query.lower() == "quit":
        break
    print(f"\n{answer(query, collection)}\n")
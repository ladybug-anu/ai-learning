# from sentence_transformers import SentenceTransformer
# from pypdf import PdfReader
# import chromadb

# # Load the embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Test it — embed a sentence and print the vector shape
# test = model.encode(["Bangalore is a great city for tech jobs"])
# print(f"Embedding shape: {test.shape}")
# print(f"First 5 values: {test[0][:5]}")

from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

# ── Step 1: Read the PDF ──────────────────────────────
# def load_pdf(path: str) -> str:
#     reader = PdfReader(path)
#     pages = [p.extract_text() for p in reader.pages if p.extract_text()]
#     return "\n".join(pages)
def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = [p.extract_text() for p in reader.pages if p.extract_text()]
    raw = "\n".join(pages)
    import re
    # Remove spaces between letters (T h i s → This)
    cleaned = re.sub(r'(?<=[a-zA-Z]) (?=[a-zA-Z])', '', raw)
    # Fix broken hyphen words (life -changing → life-changing)
    cleaned = re.sub(r' -(?=[a-zA-Z])', '-', cleaned)
    return cleaned

text = load_pdf("sadhesati.pdf")

# print(f"Total characters: {len(text)}")
# print(f"\nFirst 500 characters:\n{text[:500]}")

def chunk_text(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start : start + size])
        start += size - overlap
    return chunks

chunks = chunk_text(text)
# print(f"Total chunks: {len(chunks)}")
# print(f"\nFirst chunk:\n{chunks[0]}")
# print(f"\nSecond chunk:\n{chunks[1]}")

client = chromadb.Client()

collection = client.create_collection("sadhesati")

embeddings = model.encode(chunks).tolist()

collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print(f"Indexed {collection.count()} chunks into ChromaDB")

query = "what does sadesati mean for my career"

query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

print("Top 3 relevant chunks:\n")
for i, doc in enumerate(results["documents"][0]):
    print(f"── Chunk {i+1} ──")
    print(doc)
    print()


from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def answer(query: str) -> str:
    # Step 1: embed the question
    query_embedding = model.encode([query]).tolist()
    
    # Step 2: find relevant chunks
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )
    chunks_found = results["documents"][0]
    
    # Step 3: build context from chunks
    context = "\n\n---\n\n".join(chunks_found)
    
    # Step 4: ask LLM to answer using ONLY that context
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

# Test it
print(answer("what is sadesati?"))
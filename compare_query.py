from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

# ---- 1. Load embeddings + DB ----
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma(
    persist_directory="gojiraDB",
    embedding_function=embeddings
)

# ---- 2. Retrieve overview sections ----
query = "Compare the album technical analysis."

# Album 1 - The Link
docs_link = db.similarity_search(
    query,
    k=5,
    filter={"$and": [{"album": "The Link"}, {"section": "technical_analysis"}]}
)

# Album 2 - From Mars to Sirius
docs_fmts = db.similarity_search(
    query,
    k=5,
    filter={"$and": [{"album": "From Mars to Sirius"}, {"section": "technical_analysis"}]}
)

# ---- 3. Combine context ----
context = "\n\n--- THE LINK ---\n" + "\n\n".join(doc.page_content for doc in docs_link)
context += "\n\n--- FROM MARS TO SIRIUS ---\n" + "\n\n".join(doc.page_content for doc in docs_fmts)

# ---- 4. Build prompt ----
prompt = f"""
You are an AI assistant comparing two albums based on their TECHNICAL ANALYSIS sections.

INSTRUCTIONS:
1. Compare the albums in terms of:
   - Guitar work
   - Drum performance
   - Bass guitar
   - Vocal approach
2. Highlight similarities and differences clearly.
3. Use ONLY the provided CONTEXT.
4. Do NOT guess or use outside knowledge.

CONTEXT:
{context}

QUESTION:
Compare the album technical analysis of the two albums, answer in detail with technical analysis of the two albums.

ANSWER:
"""

# ---- 5. Generate answer ----
llm = OllamaLLM(model="llama3")
response = llm.invoke(prompt)

print("\n🤖 Overview Comparison:\n")
print(response)

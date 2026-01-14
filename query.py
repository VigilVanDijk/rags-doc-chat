from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
import sys

# 1. Load embeddings + vector DB
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="fmtsDB",
    embedding_function=embeddings
)

# 2. Retrieve relevant context
query = "Which album was released in 2003?"
docs = db.similarity_search(query, k=12)

context = "\n\n".join(doc.page_content for doc in docs)

# 3. Build prompt
prompt = f"""
You are an assistant answering questions only on the given context.

Context:
{context}

Question:
{query}

Answer in detail and factually.
"""

# 4. Local LLM
llm = OllamaLLM(model="llama3")

# 5. Generate answer
response = llm.invoke(prompt)

print("\n🤖 Answer:\n")
print(response)

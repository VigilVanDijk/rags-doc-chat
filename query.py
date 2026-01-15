from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
import sys

# 1. Load embeddings + vector DB
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="gojiraDB",
    embedding_function=embeddings
)

# 2. Retrieve relevant context
query = "How many songs are in the album The link?"
docs = db.similarity_search(
    query,
    k=10,
    filter={"$and": [{"album": "The Link"}, {"section": "tracklist"}]}
)

context = "\n\n".join(doc.page_content for doc in docs)

# 3. Build prompt
prompt = f"""
You are an AI assistant answering questions using a provided knowledge base.

INSTRUCTIONS:
1. Carefully analyze the QUESTION to determine what information is being requested.
2. Use ONLY the provided CONTEXT to answer.
3. If the question requires counting:
   - Identify an explicit list of items in the context
   - Count ONLY items that appear in that list
   - Do NOT use summary statements, inferred totals, or descriptive claims
4. If multiple sections mention items, use ONLY the section that explicitly enumerates them.
5. Do NOT guess or use outside knowledge.
6. If an explicit list is not present, clearly say so.
7. If the list is incomplete or ambiguous, do NOT provide a final count.


CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
- First, explain which section you used
- Then list the items found
- Finally, provide the count

"""



# 4. Local LLM
llm = OllamaLLM(model="llama3")

# 5. Generate answer
response = llm.invoke(prompt)

print("\n🤖 Answer:\n")
print(response)

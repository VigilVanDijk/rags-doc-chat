from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Load document
loader = TextLoader("data/linkInfo.txt")
documents = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_documents(documents)

# 3. Local embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 4. Load existing Chroma database
db = Chroma(
    persist_directory="fmtsDB",
    embedding_function=embeddings
)

# 5. Add new documents to existing database
db.add_documents(chunks)

print("✅ New documents added to fmtsDB successfully")

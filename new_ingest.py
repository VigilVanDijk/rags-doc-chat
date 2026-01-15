from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# ---- 0. Embeddings + DB ----
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="gojiraDB",
    embedding_function=embeddings
)

# ---- 1. TRACKLIST (NO SPLITTING) ----
tracklist_loader = TextLoader("data/theLink/tracklist.txt")
tracklist_docs = tracklist_loader.load()

tracklist_doc = Document(
    page_content=tracklist_docs[0].page_content,
    metadata={
        "album": "The Link",
        "section": "tracklist",
        "type": "enumeration"
    }
)

db.add_documents([tracklist_doc])

# ---- 2. PROSE (SPLIT) ----
prose_loader = TextLoader("data/theLink/overview.txt")
prose_docs = prose_loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

prose_chunks = splitter.split_documents(prose_docs)

# Safe metadata assignment
prose_docs_with_meta = []
for doc in prose_chunks:
    prose_docs_with_meta.append(
        Document(
            page_content=doc.page_content,
            metadata={
                "album": "The Link",
                "section": "overview",
                "type": "prose"
            }
        )
    )

db.add_documents(prose_docs_with_meta)

# ---- 3. ANALYSIS (SPLIT) ----
analysis_loader = TextLoader("data/theLink/analysis.txt")
analysis_docs = analysis_loader.load()
analysis_chunks = splitter.split_documents(analysis_docs)

analysis_docs_with_meta = []
for doc in analysis_chunks:
    analysis_docs_with_meta.append(
        Document(
            page_content=doc.page_content,
            metadata={
                "album": "The Link",
                "section": "analysis",
                "type": "prose"
            }
        )
    )

db.add_documents(analysis_docs_with_meta)

# ---- 4. METADATA/FACTS (NO SPLITTING) ----
meta_loader = TextLoader("data/theLink/metadata.txt")
meta_docs = meta_loader.load()

meta_doc = Document(
    page_content=meta_docs[0].page_content,
    metadata={
        "album": "The Link",
        "section": "metadata",
        "type": "facts"
    }
)

db.add_documents([meta_doc])

# ---- 5. Persist ----
# Note: With langchain_chroma, persistence is automatic when persist_directory is set
# No need to call persist() - changes are saved automatically

print("✅ Ingestion complete for tracklist, overview, analysis, and metadata")

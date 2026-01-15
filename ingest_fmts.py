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

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# ---- 1. TRACKLIST (NO SPLITTING) ----
tracklist_loader = TextLoader("data/fmts/tracklist.txt")
tracklist_docs = tracklist_loader.load()

tracklist_doc = Document(
    page_content=tracklist_docs[0].page_content,
    metadata={
        "album": "From Mars to Sirius",
        "section": "tracklist",
        "type": "enumeration"
    }
)

db.add_documents([tracklist_doc])

# ---- 2. OVERVIEW (SPLIT) ----
overview_loader = TextLoader("data/fmts/overview.txt")
overview_docs = overview_loader.load()
overview_chunks = splitter.split_documents(overview_docs)

overview_docs_with_meta = []
for doc in overview_chunks:
    overview_docs_with_meta.append(
        Document(
            page_content=doc.page_content,
            metadata={
                "album": "From Mars to Sirius",
                "section": "overview",
                "type": "prose"
            }
        )
    )

db.add_documents(overview_docs_with_meta)

# ---- 3. MUSICAL CHARACTERISTICS (SPLIT) ----
music_loader = TextLoader("data/fmts/musical_characteristics.txt")
music_docs = music_loader.load()
music_chunks = splitter.split_documents(music_docs)

music_docs_with_meta = []
for doc in music_chunks:
    music_docs_with_meta.append(
        Document(
            page_content=doc.page_content,
            metadata={
                "album": "From Mars to Sirius",
                "section": "musical_characteristics",
                "type": "prose"
            }
        )
    )

db.add_documents(music_docs_with_meta)

# ---- 4. LYRICAL THEMES & CONCEPTS (SPLIT) ----
lyrics_loader = TextLoader("data/fmts/lyrical_themes.txt")
lyrics_docs = lyrics_loader.load()
lyrics_chunks = splitter.split_documents(lyrics_docs)

lyrics_docs_with_meta = []
for doc in lyrics_chunks:
    lyrics_docs_with_meta.append(
        Document(
            page_content=doc.page_content,
            metadata={
                "album": "From Mars to Sirius",
                "section": "lyrics_themes",
                "type": "prose"
            }
        )
    )

db.add_documents(lyrics_docs_with_meta)

# ---- 5. CRITICAL RECEPTION & MUSICAL INFLUENCE (SPLIT) ----
reception_loader = TextLoader("data/fmts/critical_reception.txt")
reception_docs = reception_loader.load()
reception_chunks = splitter.split_documents(reception_docs)

reception_docs_with_meta = []
for doc in reception_chunks:
    reception_docs_with_meta.append(
        Document(
            page_content=doc.page_content,
            metadata={
                "album": "From Mars to Sirius",
                "section": "reception_influence",
                "type": "prose"
            }
        )
    )

db.add_documents(reception_docs_with_meta)

# ---- 6. TECHNICAL ANALYSIS (SPLIT) ----
technical_loader = TextLoader("data/fmts/technical_analysis.txt")
technical_docs = technical_loader.load()
technical_chunks = splitter.split_documents(technical_docs)

technical_docs_with_meta = []
for doc in technical_chunks:
    technical_docs_with_meta.append(
        Document(
            page_content=doc.page_content,
            metadata={
                "album": "From Mars to Sirius",
                "section": "technical_analysis",
                "type": "prose"
            }
        )
    )

db.add_documents(technical_docs_with_meta)

# ---- 7. CULTURAL IMPACT, RECORDING, LIVE HISTORY, COMMERCIAL, PHILOSOPHY, CONCLUSION (SPLIT) ----
final_sections = [
    ("cultural_impact.txt", "cultural_context"),
    ("recording_production.txt", "recording_production"),
    ("live_history.txt", "live_history"),
    ("commercial_performances.txt", "commercial_performance"),
    ("philosophy.txt", "philosophy"),
    ("conclusion.txt", "conclusion"),
    ("artistic_achievement.txt", "artistic_achievement"),
    ("basic_info.txt", "basic_info")
]

for file_name, section_name in final_sections:
    loader = TextLoader(f"data/fmts/{file_name}")
    docs = loader.load()
    chunks = splitter.split_documents(docs)
    
    docs_with_meta = []
    for doc in chunks:
        docs_with_meta.append(
            Document(
                page_content=doc.page_content,
                metadata={
                    "album": "From Mars to Sirius",
                    "section": section_name,
                    "type": "prose"
                }
            )
        )
    db.add_documents(docs_with_meta)

print("✅ Ingestion complete for From Mars to Sirius")

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def ingest_album(
    file_path: str,
    artist: str,
    album: str,
    persist_directory: str
):
    # 1. Load document
    loader = TextLoader(file_path)
    documents = loader.load()

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    # 3. Attach metadata
    for chunk in chunks:
        chunk.metadata.update({
            "artist": artist,
            "album": album,
            "source": file_path
        })

        # Optional: detect section heuristically
        if "TRACK-BY-TRACK" in chunk.page_content.upper():
            chunk.metadata["section"] = "tracklist"

    # 4. Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # 5. Load existing DB
    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    # 6. Append documents
    db.add_documents(chunks)
    db.persist()

    print(f"✅ Ingested album: {album}")

if __name__ == "__main__":
    ingest_album(
        file_path="data/linkInfo.txt",
        artist="Gojira",
        album="The Link",
        persist_directory="musicDB"
    )

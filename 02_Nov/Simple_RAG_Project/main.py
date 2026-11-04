
import os
import tiktoken
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_FOLDER = os.path.join(BASE_DIR, "Documents")
DB_FOLDER = os.path.join(BASE_DIR, "chroma_db")

CHUNK_SIZE = 120
CHUNK_OVERLAP = 20

documents = []
all_chunks = []

encoding = tiktoken.get_encoding("cl100k_base")

# Load documents

print("Loading documents...")

for filename in os.listdir(DOCUMENTS_FOLDER):

    if filename.lower().endswith(".txt"):

        file_path = os.path.join(DOCUMENTS_FOLDER, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        if not content.strip():
            continue

        tokens = encoding.encode(content)

        chunks = []
        start = 0

        while start < len(tokens):

            end = start + CHUNK_SIZE

            chunk_tokens = tokens[start:end]
            chunk_text = encoding.decode(chunk_tokens)

            chunks.append(chunk_text)

            all_chunks.append({
                "filename": filename,
                "chunk_id": len(chunks) - 1,
                "text": chunk_text
            })

            start += CHUNK_SIZE - CHUNK_OVERLAP

        documents.append({
            "filename": filename,
            "content": content,
            "chunks": chunks
        })

print("Total documents:", len(documents))
print("Total chunks:", len(all_chunks))

if not all_chunks:
    print("No chunks available. Check your Documents folder.")
    exit()

# Generate embeddings

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [chunk["text"] for chunk in all_chunks]

embeddings = model.encode(texts)

print("Embeddings generated:", len(embeddings))

# Connect to ChromaDB

print("\nConnecting to ChromaDB...")

client = chromadb.PersistentClient(path=DB_FOLDER)

collection = client.get_or_create_collection(
    name="rag_documents"
)

# Store chunks and embeddings

ids = [
    f"{chunk['filename']}_{chunk['chunk_id']}"
    for chunk in all_chunks
]

metadatas = [
    {
        "filename": chunk["filename"],
        "chunk_id": chunk["chunk_id"]
    }
    for chunk in all_chunks
]

collection.upsert(
    ids=ids,
    documents=texts,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print("\nData stored successfully in ChromaDB!")

print("Total records in database:", collection.count())

print("\nSample stored record:")

result = collection.get(
    ids=[ids[0]],
    include=["documents", "metadatas"]
)

print("Document:", result["metadatas"][0]["filename"])
print("Text:", result["documents"][0])

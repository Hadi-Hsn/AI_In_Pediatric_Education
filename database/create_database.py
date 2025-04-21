import os
import json
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from chromadb.config import Settings

# Load environment variables
print("🔧 Loading environment variables...")
load_dotenv()
openai_api_key = os.environ["OPENAI_API_KEY"]
print("✅ Environment variables loaded.")

# Paths
DATA_PATH = "./data"
COLLECTION_NAME = "ai_in_education_collection"

def process_single_file(filepath, filename, db):
    print(f"\n📄 Processing file: {filename}")
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            documents = []

            if isinstance(data, list):
                print(f"🔢 Found list with {len(data)} items.")
                for i, sentence in enumerate(data):
                    documents.append(Document(
                        page_content=sentence,
                        metadata={"source": filename, "item_index": i}
                    ))
            elif isinstance(data, dict):
                print(f"🧩 Found dict structure.")
                documents.append(Document(
                    page_content=json.dumps(data),
                    metadata={"source": filename}
                ))
            else:
                print(f"⚠️ Unsupported format in {filename}, skipping.")
                return

            print(f"📦 Created {len(documents)} documents from {filename}.")

            if documents:
                print(f"📤 Uploading documents from {filename} to ChromaDB...")
                db.add_documents(documents)
                print(f"✅ Uploaded {len(documents)} documents from {filename}.")
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")

def main():
    print("🚀 Starting document embedding pipeline...")

    print("🔌 Initializing OpenAI embedding function...")
    embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)
    print("✅ Embedding function initialized.")

    print("🔧 Connecting to ChromaDB server...")
    settings = Settings(chroma_api_impl="chromadb.api.fastapi.FastAPI")
    chroma_client = chromadb.HttpClient(host="localhost", port=8000, settings=settings)
    print("✅ Connected to ChromaDB.")

    # Ensure collection exists
    try:
        chroma_client.get_collection(name=COLLECTION_NAME)
        print(f"📁 Collection '{COLLECTION_NAME}' already exists.")
    except Exception as e:
        print(f"📁 Collection '{COLLECTION_NAME}' not found. Creating... ({e})")
        chroma_client.create_collection(name=COLLECTION_NAME)
        print(f"✅ Collection '{COLLECTION_NAME}' created.")

    print("🏗️ Initializing vector store interface...")
    db = Chroma(
        client=chroma_client,
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_function
    )
    print("✅ Vector store ready.")

    print(f"\n🔍 Looking for JSON files in {DATA_PATH}...")
    files = [f for f in os.listdir(DATA_PATH) if f.endswith(".json")]

    if not files:
        print("⚠️ No JSON files found. Exiting.")
        return

    print(f"📂 Found {len(files)} JSON file(s) to process.")

    # Process each file individually
    for filename in files:
        filepath = os.path.join(DATA_PATH, filename)
        process_single_file(filepath, filename, db)

    print("\n🎉 Done! All files processed.")

if __name__ == "__main__":
    main()

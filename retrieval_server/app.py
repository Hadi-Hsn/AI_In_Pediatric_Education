from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys  # Add this for error handling

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import chromadb
from chromadb.config import Settings

import uvicorn 


# Prompt template
PROMPT_TEMPLATE = """Convert the following question into a declarative statement using only the information explicitly present in the question. Do not add, infer, or rely on any external or prior knowledge: {query_text}"""

# Load environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print("❌ Error: OPENAI_API_KEY is not set in the environment variables.", file=sys.stderr)
    sys.exit(1)  # Exit the application if the API key is missing

# FastAPI app
app = FastAPI(title="AI In Education Query API")

# Request body model
class QueryRequest(BaseModel):
    query: str

# Initialize at module level so they're shared across requests
print("🚀 Initializing ChromaDB and model...")
embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)

settings = Settings(chroma_api_impl="chromadb.api.fastapi.FastAPI")
chroma_client = chromadb.HttpClient(host="host.docker.internal", port=8000, settings=settings)
db = Chroma(client=chroma_client, collection_name="ai_in_education_collection", embedding_function=embedding_function)

model = ChatOpenAI(openai_api_key=openai_api_key)
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
print("✅ Server is ready to accept requests.")

@app.post("/query")
def query_endpoint(request: QueryRequest):
    query_text = request.query
    print(f"📨 Received query: {query_text}")
    prompt = prompt_template.format(query_text=query_text)
    
    rephrased_query = model.invoke(prompt)
    print(f"🔍 Rephrased query: {rephrased_query.content}")
    results = db.similarity_search_with_relevance_scores(rephrased_query.content, k=3)
    if not results or results[0][1] < 0.6:
        raise HTTPException(status_code=404, detail="No relevant documents found.")

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    sources = [doc.metadata.get("source", "unknown") for doc, _ in results]

    return {
        "query": query_text,
        "rephrased_query": rephrased_query.content,
        "answers_context": context_text,
        "sources": sources,
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)


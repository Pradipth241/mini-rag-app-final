# Full Path: C:\Users\pradi\mini-rag-app\logic.py

import os
import re
import fitz
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from langchain_cohere import CohereEmbeddings
from groq import Groq
from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- 1. CONFIGURATION & INITIALIZATION ---
load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

embedding_model = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=cohere_api_key,
    request_timeout=120
)

qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
groq_client = Groq(api_key=groq_api_key)

QDRANT_COLLECTION_NAME = "my_mini_rag_collection"

# --- 2. DOCUMENT PARSING & CLEANING ---
async def parse_document(file: UploadFile) -> str:
    file_extension = file.filename.split('.')[-1].lower()
    contents = await file.read()
    text = ""
    if file_extension == "txt":
        text = contents.decode("utf-8")
    elif file_extension == "pdf":
        with fitz.open(stream=contents, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()

    lines = text.split('\n')
    cleaned_lines = [line for line in lines if len(line.strip()) > 10 and re.search('[a-zA-Z]', line)]
    text = "\n".join(cleaned_lines)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    cleaned_text = text.strip()
    return cleaned_text

# --- 3. TEXT PROCESSING AND STORAGE ---
def create_and_store_embeddings(text: str):
    qdrant_client.recreate_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
    )
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, length_function=len)
    text_chunks = text_splitter.split_text(text)
    embeddings = embedding_model.embed_documents(text_chunks)
    qdrant_client.upsert(
        collection_name=QDRANT_COLLECTION_NAME,
        points=models.Batch(ids=list(range(len(text_chunks))), payloads=[{"text": chunk} for chunk in text_chunks], vectors=embeddings),
    )
    print("Embeddings created with Cohere and stored successfully.")

# --- 4. QUERY PROCESSING AND ANSWERING ---
def generate_sub_queries(query: str) -> list[str]:
    prompt = f"You are a helpful AI assistant. Your task is to generate 3 different search queries based on a single user question. Provide ONLY a numbered list of the queries. Original Question: \"{query}\""
    try:
        chat_completion = groq_client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.1-8b-instant") # Replace with a valid model from your dashboard
        response_text = chat_completion.choices[0].message.content
        queries = [line.split('. ', 1)[1] for line in response_text.strip().split('\n') if '. ' in line]
        queries.append(query)
        return list(set(queries))
    except Exception:
        return [query]

def query_and_generate_answer(query: str) -> dict:
    sub_queries = generate_sub_queries(query)

    all_retrieved_docs = []
    for sub_query in sub_queries:
        query_embedding = embedding_model.embed_query(sub_query)
        search_results = qdrant_client.search(collection_name=QDRANT_COLLECTION_NAME, query_vector=query_embedding, limit=3)
        all_retrieved_docs.extend([result.payload['text'] for result in search_results])

    unique_docs = list(dict.fromkeys(all_retrieved_docs))
    
    # Using the retrieved documents directly and bypassing the reranker
    context_docs = unique_docs[:5]

    if not context_docs:
        return {"answer": "I cannot find a sufficiently relevant answer in the provided document.", "sources": []}

    context_str = "\n\n".join([f"Source [{i+1}]:\n{doc}" for i, doc in enumerate(context_docs)])
    prompt = f"CONTEXT:\n{context_str}\n\nQUESTION:\n{query}\n\nANSWER:"

    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant", # Make sure to replace this with a valid model ID from your Groq dashboard
    )
    final_answer = chat_completion.choices[0].message.content

    return {"answer": final_answer, "sources": context_docs}
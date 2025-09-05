# Full Path: C:\Users\pradi\mini-rag-app\main.py

from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from logic import create_and_store_embeddings, query_and_generate_answer, parse_document
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mini RAG Service", version="5.0.0")

# CORS Middleware
origins = ["http://localhost:3000"] # Add your Vercel URL here for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models for JSON requests
class TextInput(BaseModel):
    text: str

class QueryInput(BaseModel):
    query: str

# API Endpoints
@app.get("/", tags=["General"])
def read_root():
    return {"status": "API is online!"}

@app.post("/process-text-input", tags=["Processing"])
def process_text_input_endpoint(payload: TextInput):
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    try:
        create_and_store_embeddings(payload.text)
        return {"status": "success", "message": "Text processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-text", tags=["Processing"])
async def process_text_file_endpoint(file: UploadFile = File(...)):
    filename = file.filename
    if not (filename.endswith(".txt") or filename.endswith(".pdf")):
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported.")
    
    try:
        extracted_text = await parse_document(file)
        if not extracted_text:
             raise HTTPException(status_code=400, detail=f"Could not extract text from '{filename}'.")
        create_and_store_embeddings(extracted_text)
        return {"status": "success", "message": f"File '{filename}' processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", tags=["Querying"])
def query_endpoint(payload: QueryInput):
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query field cannot be empty.")
    try:
        result = query_and_generate_answer(payload.query)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from database import process_and_index_pdf
from pipeline import stream_rag_response

app = FastAPI(title="Medical RAG Core API")

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    question: str

@app.post("/upload")
async def upload_document(user_id: str = Form(...), file: UploadFile = File(...)):
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        num_chunks = process_and_index_pdf(temp_file_path, user_id)
        os.remove(temp_file_path)
        
        return {"status": "success", "chunks_indexed": num_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_bot(request: ChatRequest):
    try:
        # We create a generator function that yields words as they arrive
        def word_generator():
            for chunk in stream_rag_response(
                user_id=request.user_id,
                session_id=request.session_id,
                question=request.question
            ):
                yield chunk

        # Return the live stream instead of a static JSON dictionary
        return StreamingResponse(word_generator(), media_type="text/plain")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
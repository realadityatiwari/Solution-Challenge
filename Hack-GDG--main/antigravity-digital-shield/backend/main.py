import os
import shutil
import uuid
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# FIX 1: Import at the top to avoid request-time latency
try:
    from fingerprint import check_similarity, index_authorized_video
except ImportError:
    # Fallback for initial scaffolding
    def check_similarity(path): return {"score": 0.0}
    def index_authorized_video(path, vid): return False

try:
    from analyst import analyze_news
except ImportError:
    def analyze_news(text): return {"violation_likelihood": 0.0, "reasoning": "Mock fallback"}

app = FastAPI(title="Antigravity Digital Shield")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessMediaResponse(BaseModel):
    status: str
    message: str
    media_id: str
    match_score: float

class ProcessNewsRequest(BaseModel):
    news_text: str

class ProcessNewsResponse(BaseModel):
    status: str
    message: str
    report: dict

class FingerprintResponse(BaseModel):
    status: str
    message: str
    video_id: str

@app.get("/")
def read_root():
    return {"status": "online"}

# FIX 2: Removed 'async' so FastAPI uses a thread pool for blocking CPU tasks
@app.post("/process-media", response_model=ProcessMediaResponse)
def process_media(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # FIX 3: Use UUID to prevent filename collisions if two users upload 'video.mp4'
    media_id = str(uuid.uuid4())
    temp_path = f"temp_{media_id}_{file.filename}"
    
    try:
        # Securely save the uploaded file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Logic execution
        result = check_similarity(temp_path)
        score = result.get("score", 0.0)
        
    except Exception as e:
        # Log the error for the 'Analyst Agent'
        print(f"Error processing media: {e}")
        raise HTTPException(status_code=500, detail="Internal processing error")
    
    finally:
        # Cleanup: Close the upload file and remove temp local file
        file.file.close()
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    is_infringing = score > 10.0 
    
    return ProcessMediaResponse(
        status="success",
        message="Potential infringement flagged!" if is_infringing else "Media clear.",
        media_id=media_id,
        match_score=score
    )

@app.post("/process-news", response_model=ProcessNewsResponse)
def process_news(news_text: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    if not news_text and not file:
        raise HTTPException(status_code=400, detail="Must provide either text or an image.")
        
    temp_path = None
    if file:
        media_id = str(uuid.uuid4())
        temp_path = f"temp_news_{media_id}_{file.filename}"
        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to save image")
        finally:
            file.file.close()
            
    try:
        report = analyze_news(news_text, temp_path)
        is_fake = report.get("confidence_score", 0.0) > 0.6
        
        return ProcessNewsResponse(
            status="success",
            message="Warning: High probability of Fake News detected!" if is_fake else "News source appears to be factual.",
            report=report
        )
    except Exception as e:
        print(f"Error processing news: {e}")
        raise HTTPException(status_code=500, detail="Internal processing error")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/fingerprint-asset", response_model=FingerprintResponse)
def fingerprint_asset(video_id: str = Form(...), file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No video file uploaded")
        
    temp_path = f"temp_index_{uuid.uuid4()}_{file.filename}"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        success = index_authorized_video(temp_path, video_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to extract keyframes or index video.")
            
        return FingerprintResponse(
            status="success",
            message="Video successfully fingerprinted and added to ChromaDB Vault.",
            video_id=video_id
        )
    except Exception as e:
        print(f"Error fingerprinting video: {e}")
        raise HTTPException(status_code=500, detail="Internal indexing error")
    finally:
        file.file.close()
        if os.path.exists(temp_path):
            os.remove(temp_path)
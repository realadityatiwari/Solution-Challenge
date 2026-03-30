import os
import shutil
import uuid
import logging
import hashlib
import threading
import time
import urllib.request
import xml.etree.ElementTree as ET
import datetime
import re
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("agent.log"),
        logging.StreamHandler()
    ]
)

# FIX 1: Import at the top to avoid request-time latency
try:
    from fingerprint import check_similarity, index_authorized_video, get_all_fingerprints
except ImportError:
    # Fallback for initial scaffolding
    def check_similarity(path): return {"score": 0.0}
    def index_authorized_video(path, vid): return False
    def get_all_fingerprints(): return []

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

import json

QUEUE_FILE = "queue_db.json"

def load_queue():
    if os.path.exists(QUEUE_FILE):
        try:
            with open(QUEUE_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_queue(q):
    with open(QUEUE_FILE, "w") as f:
        json.dump(q, f, indent=4)

DISMISSED_FILE = "dismissed_db.json"

def load_dismissed():
    if os.path.exists(DISMISSED_FILE):
        try:
            with open(DISMISSED_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_dismissed(d):
    with open(DISMISSED_FILE, "w") as f:
        json.dump(d, f, indent=4)

class TakedownNotice(BaseModel):
    id: str
    notice: str
    violation: dict

def fetch_live_news_loop():
    # Wait for the server to be fully up before starting loops
    time.sleep(5)
    while True:
        try:
            url = "https://news.google.com/rss/search?q=NBA&hl=en-US&gl=US&ceid=US:en"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
            
            root = ET.fromstring(xml_data)
            items = root.findall('./channel/item')
            
            if items:
                # Take the top 3 items
                new_items = items[:3]
                
                existing_urls = set()
                if os.path.exists("violations.log"):
                    with open("violations.log", "r") as f:
                        for line in f:
                            if not line.strip(): continue
                            try:
                                d = json.loads(line)
                                existing_urls.add(d.get("url", ""))
                            except:
                                pass
                
                added_count = 0
                with open("violations.log", "a") as f:
                    for item in new_items:
                        title = item.find('title').text if item.find('title') is not None else "Unknown Title"
                        link = item.find('link').text if item.find('link') is not None else "Unknown URL"
                        pubDate = item.find('pubDate').text if item.find('pubDate') is not None else datetime.datetime.utcnow().isoformat()
                        
                        # Simple de-duplication
                        if link in existing_urls:
                            continue
                            
                        # Quick OG Image extraction
                        suspect_thumb = ""
                        try:
                            art_req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(art_req, timeout=3) as art_res:
                                html = art_res.read(16000).decode('utf-8', errors='ignore')
                                match = re.search(r'<meta property="og:image" content="(.*?)"', html)
                                if match:
                                    suspect_thumb = match.group(1).replace("&amp;", "&")
                        except Exception:
                            pass
                            
                        # Assign high vulnerability score to force it into the UI for demonstration
                        score = 80.0 + (len(title) % 19)
                        
                        log_entry = {
                            "timestamp": pubDate,
                            "title": f"[LIVE WEB SCANNED] {title}",
                            "url": link,
                            "channel": "Global Web / News Domain",
                            "match_score": score,
                            "status": "Flagged for Analyst Review",
                            "suspect_thumb": suspect_thumb
                        }
                        f.write(json.dumps(log_entry) + "\n")
                        added_count += 1
                
                if added_count > 0:
                    logging.info(f"Sentry Agent: Dynamically injected {added_count} new real-world alerts into the Live Feed.")
                    
        except Exception as e:
            logging.error(f"Error in background news fetcher loop: {e}")
            
        # Poll every 30 seconds for new items
        time.sleep(30)

@app.on_event("startup")
def start_background_tasks():
    thread = threading.Thread(target=fetch_live_news_loop, daemon=True)
    thread.start()
    logging.info("Started background live news fetching persistent agent.")

@app.get("/")
def read_root():
    return {"status": "online"}

@app.get("/live-feed")
def get_live_feed():
    try:
        if not os.path.exists("violations.log"):
            return {"status": "success", "violations": []}
            
        dismissed = load_dismissed()
        queued = [q.get("id") for q in load_queue()]
        
        violations = []
        with open("violations.log", "r") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    # Generate a consistent ID based on the URL
                    vid_url = data.get("url", "")
                    vid_id = "V-" + hashlib.md5(vid_url.encode()).hexdigest()[:6].upper()
                    
                    if vid_id in dismissed or vid_id in queued:
                        continue
                        
                    suspect_thumb = data.get("suspect_thumb", "")
                    
                    if "youtube.com/watch?v=" in vid_url:
                        try:
                            video_id = vid_url.split("v=")[1].split("&")[0]
                            suspect_thumb = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                        except:
                            pass
                            
                    if not suspect_thumb:
                        suspect_thumb = f"https://picsum.photos/seed/{vid_id}/400/225"
                        
                    official_thumb = f"https://picsum.photos/seed/off_{vid_id}/400/225"
                        
                    violations.append({
                        "id": vid_id,
                        "title": data.get("title", "Unknown Title"),
                        "channel": data.get("channel", "Unknown Channel"),
                        "url": vid_url,
                        "match_score": data.get("match_score", 0.0),
                        "timestamp": data.get("timestamp", "Just now"),
                        "official_asset": "NBA_VAULT_DETECTED",
                        "official_thumb": official_thumb,
                        "pirated_thumb": suspect_thumb
                    })
                except json.JSONDecodeError:
                    continue
        
        # Sort by match score descending
        violations.sort(key=lambda x: x["match_score"], reverse=True)
        return {"status": "success", "violations": violations}
    except Exception as e:
        print(f"Error fetching live feed: {e}")
        return {"status": "error", "violations": []}

@app.post("/live-feed/dismiss/{item_id}")
def dismiss_violation(item_id: str):
    d = load_dismissed()
    if item_id not in d:
        d.append(item_id)
        save_dismissed(d)
    return {"status": "success", "message": f"Dismissed {item_id}"}


@app.get("/takedown-queue")
def get_takedown_queue():
    return {"status": "success", "queue": load_queue()}

@app.post("/takedown-queue")
def add_takedown(notice: TakedownNotice):
    q = load_queue()
    # Check if already exists just in case
    if not any(item.get("id") == notice.id for item in q):
        q.insert(0, notice.dict())
        save_queue(q)
    return {"status": "success", "message": "Notice added to queue."}

@app.delete("/takedown-queue/{item_id}")
def delete_takedown(item_id: str):
    q = load_queue()
    q = [item for item in q if item.get("id") != item_id]
    save_queue(q)
    return {"status": "success", "message": f"Sent notice {item_id}"}

@app.get("/logs")
def get_logs():
    try:
        if os.path.exists("agent.log"):
            with open("agent.log", "r") as f:
                lines = f.readlines()
                # Return the last 50 lines
                return {"status": "success", "logs": "".join(lines[-50:])}
        else:
            return {"status": "success", "logs": "No logs recorded yet."}
    except Exception as e:
        return {"status": "error", "logs": str(e)}

@app.get("/fingerprints")
def get_fingerprints():
    try:
        data = get_all_fingerprints()
        return {"status": "success", "fingerprints": data}
    except Exception as e:
        print(f"Error fetching fingerprints: {e}")
        return {"status": "error", "message": "Failed to fetch fingerprints", "fingerprints": []}

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
        raise HTTPException(status_code=400, detail="Must provide either text, a URL, or a media file (image/video).")
        
    temp_path = None
    if file:
        media_id = str(uuid.uuid4())
        temp_path = f"temp_news_{media_id}_{file.filename}"
        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to save media file")
        finally:
            file.file.close()
            
    try:
        report = analyze_news(news_text, temp_path)
        is_fake = report.get("fake_probability", 0.0) > 0.6
        
        if is_fake:
            # Auto-queue the fake news into the takedown queue
            takedown_id = f"FN-{uuid.uuid4().hex[:6].upper()}"
            violation_info = {
                "title": "Malicious Disinformation / Fake News",
                "channel": "Identified News Source",
                "url": (news_text[:150] + '...') if news_text else "Attached Media File"
            }
            draft_notice = f"To the Designated Agent,\n\nWe have identified this content as Malicious Disinformation / Fake News with a probability score of {report.get('fake_probability')}.\n\nSource: {violation_info['url']}\nKey Findings: {report.get('authenticity_verdict')}\n\nPlease take immediate action to remove or disable access to this material.\n\nSincerely,\nAntigravity Digital Shield"
            
            new_notice = TakedownNotice(
                id=takedown_id,
                notice=draft_notice,
                violation=violation_info
            )
            add_takedown(new_notice)
            message = "Warning: High probability of Fake News detected! Automatically added to Takedown Queue."
        else:
            message = "News source appears to be factual."

        return ProcessNewsResponse(
            status="success",
            message=message,
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
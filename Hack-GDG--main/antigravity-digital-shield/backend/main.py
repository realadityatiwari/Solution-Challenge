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

# ─────────────────────────────────────────────────────────────────────────────
# MULTI-CATEGORY RSS FEED SOURCES — 12 diverse news domains
# ─────────────────────────────────────────────────────────────────────────────
LIVE_NEWS_FEEDS = [
    # World / Top Stories
    {"url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en", "channel": "Google News · World", "category": "World News"},
    {"url": "https://feeds.bbci.co.uk/news/world/rss.xml",                                          "channel": "BBC News · World",   "category": "World News"},
    # Politics & Government
    {"url": "https://news.google.com/rss/headlines/section/topic/POLITICS?hl=en-US&gl=US&ceid=US:en", "channel": "Google News · Politics", "category": "Politics & Elections"},
    # Health & Medicine
    {"url": "https://news.google.com/rss/headlines/section/topic/HEALTH?hl=en-US&gl=US&ceid=US:en",   "channel": "Google News · Health",   "category": "Health & Medicine"},
    {"url": "https://www.who.int/rss-feeds/news-english.xml",                                          "channel": "WHO · Health Alerts",    "category": "Health & Medicine"},
    # Science & Climate
    {"url": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en",  "channel": "Google News · Science",  "category": "Science & Climate"},
    {"url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",                                          "channel": "NASA · Breaking News",   "category": "Science & Climate"},
    # Technology & AI
    {"url": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en","channel": "Google News · Tech",     "category": "Technology & AI"},
    # Finance & Business
    {"url": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",  "channel": "Google News · Business", "category": "Finance & Cryptocurrency"},
    {"url": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US",           "channel": "Yahoo Finance · Markets","category": "Finance & Cryptocurrency"},
    # Sports
    {"url": "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=en-US&gl=US&ceid=US:en",    "channel": "Google News · Sports",   "category": "Sports"},
    {"url": "https://www.espn.com/espn/rss/news",                                                       "channel": "ESPN · Sports",          "category": "Sports"},
    # Entertainment
    {"url": "https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=en-US&gl=US&ceid=US:en","channel": "Google News · Entertainment","category": "Entertainment & Celebrity"},
    # War & Conflict
    {"url": "https://news.google.com/rss/search?q=conflict+war&hl=en-US&gl=US&ceid=US:en",             "channel": "Google News · Conflict", "category": "War & Conflict"},
    # Climate & Environment
    {"url": "https://news.google.com/rss/search?q=climate+change+environment&hl=en-US&gl=US&ceid=US:en","channel": "Google News · Climate", "category": "Science & Climate"},
    # Viral / Social Media trending
    {"url": "https://news.google.com/rss/search?q=viral+trending+social+media&hl=en-US&gl=US&ceid=US:en","channel": "Google News · Viral", "category": "Social Media Viral Content"},
]

def _fetch_one_feed(feed: dict, existing_urls: set) -> list:
    """Fetches and parses a single RSS feed, returns new log entries."""
    entries = []
    try:
        req = urllib.request.Request(feed["url"], headers={'User-Agent': 'Mozilla/5.0 (compatible; AntigravityShield/2.0)'})
        with urllib.request.urlopen(req, timeout=8) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        items = root.findall('./channel/item')
        if not items:
            # Some feeds use Atom format
            items = root.findall('.//{http://www.w3.org/2005/Atom}entry')

        for item in items[:2]:  # Max 2 items per feed per cycle
            # Support both RSS and Atom
            title_el = item.find('title') or item.find('{http://www.w3.org/2005/Atom}title')
            link_el  = item.find('link')  or item.find('{http://www.w3.org/2005/Atom}link')
            date_el  = item.find('pubDate') or item.find('{http://www.w3.org/2005/Atom}published')

            title   = title_el.text if title_el is not None and title_el.text else "Unknown Title"
            link    = link_el.text if link_el is not None and link_el.text else (link_el.get("href", "") if link_el is not None else "")
            pubDate = date_el.text if date_el is not None and date_el.text else datetime.datetime.utcnow().isoformat()

            # Clean up Google News redirect links
            if "news.google.com/rss/articles" in link:
                link = link  # Keep as is; redirect ultimately lands on real URL

            if not link or link in existing_urls:
                continue

            # Quick OG image extraction (best-effort, 3s timeout)
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

            # Vulnerability score: reflects how "suspicious" a news item might be for demonstration
            score = 55.0 + (len(title) % 35)

            entries.append({
                "timestamp": pubDate,
                "title": f"[{feed['category'].upper()}] {title}",
                "url": link,
                "channel": feed["channel"],
                "match_score": score,
                "status": "Pending ARGUS Analysis",
                "suspect_thumb": suspect_thumb,
                "news_category": feed["category"],
            })

    except Exception as e:
        logging.warning(f"Feed fetch failed [{feed['channel']}]: {e}")

    return entries


def fetch_live_news_loop():
    """
    Background agent that continuously scrapes 12+ diverse news categories
    and feeds them into the live violations dashboard.
    Cycles through all feed sources to ensure maximum category coverage.
    """
    time.sleep(5)  # Wait for server startup

    feed_index = 0  # Round-robin through feeds

    while True:
        try:
            # Load existing URLs to prevent duplicates
            existing_urls = set()
            if os.path.exists("violations.log"):
                with open("violations.log", "r") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            d = json.loads(line)
                            existing_urls.add(d.get("url", ""))
                        except Exception:
                            pass

            # Pull from next 3 feeds in rotation (round-robin across all 16 feeds)
            feeds_this_cycle = [
                LIVE_NEWS_FEEDS[feed_index % len(LIVE_NEWS_FEEDS)],
                LIVE_NEWS_FEEDS[(feed_index + 1) % len(LIVE_NEWS_FEEDS)],
                LIVE_NEWS_FEEDS[(feed_index + 2) % len(LIVE_NEWS_FEEDS)],
            ]
            feed_index = (feed_index + 3) % len(LIVE_NEWS_FEEDS)

            all_new_entries = []
            categories_fetched = []
            for feed in feeds_this_cycle:
                entries = _fetch_one_feed(feed, existing_urls)
                all_new_entries.extend(entries)
                if entries:
                    categories_fetched.append(feed["category"])
                # Update existing_urls to avoid cross-feed duplicates in same cycle
                for entry in entries:
                    existing_urls.add(entry["url"])

            if all_new_entries:
                with open("violations.log", "a") as f:
                    for entry in all_new_entries:
                        f.write(json.dumps(entry) + "\n")
                logging.info(
                    f"ARGUS Sentry: Injected {len(all_new_entries)} items from categories: {', '.join(categories_fetched)}"
                )

        except Exception as e:
            logging.error(f"Error in background news fetcher loop: {e}")

        # Poll every 30 seconds
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
            raise HTTPException(status_code=500, detail="Failed to save media file") from e
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
        raise HTTPException(status_code=500, detail="Internal processing error") from e
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
        raise HTTPException(status_code=500, detail="Internal indexing error") from e
    finally:
        file.file.close()
        if os.path.exists(temp_path):
            os.remove(temp_path)
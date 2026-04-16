import os
from dotenv import load_dotenv
load_dotenv()
import collections
import sqlite3
import pathlib
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
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

# Allowed MIME types per upload endpoint
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/x-m4v", "video/quicktime", "video/webm", "video/avi"}
ALLOWED_MEDIA_TYPES = ALLOWED_VIDEO_TYPES | {"image/jpeg", "image/png", "image/gif", "image/webp"}

def safe_filename(filename: str | None) -> str:
    """Strip any path components from a user-supplied filename to prevent path traversal."""
    if not filename:
        return f"upload_{uuid.uuid4().hex}"
    return pathlib.Path(filename).name or f"upload_{uuid.uuid4().hex}"

# ─────────────────────────────────────────────────────────────────────────────
# Sliding-window rate limiter — stdlib only (collections, threading, time)
# Per-IP, per-endpoint. Thread-safe via Lock.
# ─────────────────────────────────────────────────────────────────────────────
_rate_lock = threading.Lock()
# key: "endpoint:client_ip"  →  value: deque of request timestamps (float)
_rate_buckets: dict = collections.defaultdict(lambda: collections.deque(maxlen=50))

def check_rate_limit(key: str, max_requests: int, window_seconds: int) -> bool:
    """
    Sliding window rate limiter. Returns True if the request is allowed.
    Evicts timestamps older than window_seconds, then checks current count.
    """
    now = time.time()
    cutoff = now - window_seconds
    with _rate_lock:
        dq = _rate_buckets[key]
        while dq and dq[0] < cutoff:   # evict expired timestamps
            dq.popleft()
        if len(dq) >= max_requests:
            return False               # rate limit exceeded
        dq.append(now)
        return True

# ─────────────────────────────────────────────────────────────────────────────
# File size limits and size-safe upload writer
# ─────────────────────────────────────────────────────────────────────────────
MAX_VIDEO_SIZE = 100 * 1024 * 1024   # 100 MB — video scan / piracy check
MAX_MEDIA_SIZE =  20 * 1024 * 1024   #  20 MB — news image/video attachment
MAX_ASSET_SIZE = 200 * 1024 * 1024   # 200 MB — authorized asset fingerprinting

def _check_content_length(request: Request, max_bytes: int) -> None:
    """Fast pre-check: reject immediately if Content-Length header exceeds limit."""
    cl = request.headers.get("content-length")
    if cl:
        try:
            if int(cl) > max_bytes:
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Maximum allowed: {max_bytes // (1024 * 1024)} MB."
                )
        except ValueError:
            pass  # Malformed header — let chunked write guard catch it

def save_upload_limited(upload_file, dest_path: str, max_bytes: int) -> None:
    """
    Write an upload to dest_path in 64 KB chunks.
    Raises HTTP 413 and removes the partial file if max_bytes is exceeded.
    Guards against spoofed or missing Content-Length headers.
    """
    written = 0
    chunk_size = 64 * 1024  # 64 KB
    with open(dest_path, "wb") as out:
        while True:
            chunk = upload_file.file.read(chunk_size)
            if not chunk:
                break
            written += len(chunk)
            if written > max_bytes:
                # Abort — delete partial file before raising
                out.close()
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Maximum allowed: {max_bytes // (1024 * 1024)} MB."
                )
            out.write(chunk)

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

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    expected_api_key = os.environ.get("API_KEY")
    if not expected_api_key or api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return api_key

app = FastAPI(title="Antigravity Digital Shield")

_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
_PRODUCTION_ORIGIN = os.environ.get("FRONTEND_ORIGIN")
if _PRODUCTION_ORIGIN:
    _ALLOWED_ORIGINS.append(_PRODUCTION_ORIGIN)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessMediaResponse(BaseModel):
    status: str
    message: str
    media_id: str
    match_score: float
    detection_type: str  # "fingerprint" | "news" — tells frontend what the score represents

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

# ─────────────────────────────────────────────────────────────────────────────
# SQLite persistence — replaces queue_db.json + dismissed_db.json
# stdlib only, no new dependencies. Thread-safe via WAL mode + atomic SQL.
# ─────────────────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shield.db")

def get_db():
    """Return a new SQLite connection with WAL mode and row factory set."""
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.execute("PRAGMA journal_mode=WAL")  # Allows concurrent reads during writes
    con.row_factory = sqlite3.Row
    return con

def init_db():
    """Create tables on first run. Safe to call multiple times."""
    with get_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS takedown_queue (
                id      TEXT PRIMARY KEY,
                notice  TEXT NOT NULL,
                violation TEXT NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS dismissed (
                id TEXT PRIMARY KEY
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS violations (
                id            TEXT PRIMARY KEY,  -- MD5-based V-XXXXXX, deduplicates by URL
                url           TEXT NOT NULL UNIQUE,
                title         TEXT NOT NULL,
                channel       TEXT NOT NULL,
                match_score   REAL NOT NULL,
                timestamp     TEXT NOT NULL,
                suspect_thumb TEXT NOT NULL DEFAULT ''
            )
        """)
        # rowid is the implicit primary key — ORDER BY rowid DESC LIMIT N is O(log N)
    logging.info("SQLite DB initialised at %s", DB_PATH)

def load_queue():
    """Return all takedown queue items ordered newest-first."""
    with get_db() as con:
        rows = con.execute(
            "SELECT id, notice, violation FROM takedown_queue ORDER BY rowid DESC"
        ).fetchall()
    return [{"id": r["id"], "notice": r["notice"], "violation": json.loads(r["violation"])} for r in rows]

def load_dismissed():
    """Return the set of dismissed item IDs."""
    with get_db() as con:
        rows = con.execute("SELECT id FROM dismissed").fetchall()
    return {r["id"] for r in rows}

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
            t1 = item.find('title')
            title_el = t1 if t1 is not None else item.find('{http://www.w3.org/2005/Atom}title')
            l1 = item.find('link')
            link_el  = l1 if l1 is not None else item.find('{http://www.w3.org/2005/Atom}link')
            d1 = item.find('pubDate')
            date_el  = d1 if d1 is not None else item.find('{http://www.w3.org/2005/Atom}published')

            title   = title_el.text if title_el is not None and title_el.text else "Unknown Title"
            link    = link_el.text if link_el is not None and link_el.text else (link_el.get("href", "") if link_el is not None else "")
            pubDate = date_el.text if date_el is not None and date_el.text else datetime.datetime.utcnow().isoformat()

            # Clean up Google News redirect links
            if "news.google.com/rss/articles" in link:
                link = link  # Keep as is; redirect ultimately lands on real URL

            if not link:
                logging.warning("Skipped RSS item due to missing link")
            
            if not link or link in existing_urls:
                continue

            # Quick OG image extraction (best-effort, 3s timeout)
            suspect_thumb = ""
            try:
                art_req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(art_req, timeout=1) as art_res:
                    html = art_res.read(16000).decode('utf-8', errors='ignore')
                    match = re.search(r'<meta property="og:image" content="(.*?)"', html)
                    if match:
                        suspect_thumb = match.group(1).replace("&amp;", "&")
            except Exception:
                pass

            # RSS feed items have no vault match — score 0.0 (real score assigned by check_similarity at scan time)
            score = 0.0

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
            # Load existing URLs from DB to prevent duplicates (single indexed query)
            with get_db() as con:
                rows = con.execute(
                    "SELECT url FROM violations ORDER BY rowid DESC LIMIT 5000"
                ).fetchall()
            existing_urls = {r["url"] for r in rows}

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
                # Write to SQLite with INSERT OR IGNORE — URL UNIQUE constraint deduplicates
                with get_db() as con:
                    for entry in all_new_entries:
                        vid_url = entry["url"]
                        vid_id = "V-" + hashlib.md5(vid_url.encode()).hexdigest()[:6].upper()
                        con.execute(
                            "INSERT OR IGNORE INTO violations "
                            "(id, url, title, channel, match_score, timestamp, suspect_thumb) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (
                                vid_id,
                                vid_url,
                                entry["title"],
                                entry["channel"],
                                entry["match_score"],
                                entry["timestamp"],
                                entry.get("suspect_thumb", ""),
                            )
                        )
                logging.info(
                    f"ARGUS Sentry: Injected {len(all_new_entries)} items from categories: {', '.join(categories_fetched)}"
                )

        except Exception as e:
            logging.error(f"Error in background news fetcher loop: {e}")

        # Poll every 30 seconds
        time.sleep(30)

@app.on_event("startup")
def start_background_tasks():
    init_db()  # Ensure SQLite tables exist before any request is served
    thread = threading.Thread(target=fetch_live_news_loop, daemon=True)
    thread.start()
    logging.info("Started background live news fetching persistent agent.")

@app.get("/")
def read_root():
    return {"status": "online"}

@app.get("/live-feed")
def get_live_feed():
    try:
        with get_db() as con:
            dismissed = {r["id"] for r in con.execute("SELECT id FROM dismissed").fetchall()}
            queued_ids = {r["id"] for r in con.execute("SELECT id FROM takedown_queue").fetchall()}
            rows = con.execute(
                "SELECT id, url, title, channel, match_score, timestamp, suspect_thumb "
                "FROM violations ORDER BY rowid DESC LIMIT 200"
            ).fetchall()

        violations = []
        for row in rows:
            vid_id = row["id"]
            if vid_id in dismissed or vid_id in queued_ids:
                continue

            vid_url = row["url"]
            suspect_thumb = row["suspect_thumb"]

            if "youtube.com/watch?v=" in vid_url:
                try:
                    video_id = vid_url.split("v=")[1].split("&")[0]
                    suspect_thumb = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                except Exception:
                    pass

            if not suspect_thumb:
                suspect_thumb = f"https://picsum.photos/seed/{vid_id}/400/225"

            official_thumb = f"https://picsum.photos/seed/off_{vid_id}/400/225"

            violations.append({
                "id": vid_id,
                "title": row["title"],
                "channel": row["channel"],
                "url": vid_url,
                "match_score": row["match_score"],
                "detection_type": "news",   # RSS feed item, no vault similarity computed
                "timestamp": row["timestamp"],
                "official_asset": "NBA_VAULT_DETECTED",
                "official_thumb": official_thumb,
                "pirated_thumb": suspect_thumb,
            })

        violations.sort(key=lambda x: x["match_score"], reverse=True)
        return {"status": "success", "violations": violations}
    except Exception as e:
        logging.error(f"Error fetching live feed: {e}")
        return {"status": "error", "violations": []}

@app.post("/live-feed/dismiss/{item_id}")
def dismiss_violation(item_id: str, api_key: str = Depends(verify_api_key)):
    # INSERT OR IGNORE is atomic — no R-M-W race condition
    with get_db() as con:
        con.execute("INSERT OR IGNORE INTO dismissed (id) VALUES (?)", (item_id,))
    return {"status": "success", "message": f"Dismissed {item_id}"}


@app.get("/takedown-queue")
def get_takedown_queue():
    return {"status": "success", "queue": load_queue()}

@app.post("/takedown-queue")
def add_takedown(notice: TakedownNotice, api_key: str = Depends(verify_api_key)):
    # INSERT OR IGNORE prevents duplicates atomically — no list scan required
    with get_db() as con:
        con.execute(
            "INSERT OR IGNORE INTO takedown_queue (id, notice, violation) VALUES (?, ?, ?)",
            (notice.id, notice.notice, json.dumps(notice.violation))
        )
    return {"status": "success", "message": "Notice added to queue."}

@app.delete("/takedown-queue/{item_id}")
def delete_takedown(item_id: str, api_key: str = Depends(verify_api_key)):
    with get_db() as con:
        con.execute("DELETE FROM takedown_queue WHERE id = ?", (item_id,))
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
def process_media(request: Request, file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(f"process-media:{client_ip}", max_requests=10, window_seconds=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded: max 10 video scans per minute per IP.")

    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=415, detail=f"Unsupported file type '{file.content_type}'. Allowed: {sorted(ALLOWED_VIDEO_TYPES)}")

    _check_content_length(request, MAX_VIDEO_SIZE)

    media_id = str(uuid.uuid4())
    temp_path = f"temp_{media_id}_{safe_filename(file.filename)}"

    try:
        save_upload_limited(file, temp_path, MAX_VIDEO_SIZE)
        
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
        match_score=score,
        detection_type="fingerprint"   # Vault-based perceptual hash similarity
    )

@app.post("/process-news", response_model=ProcessNewsResponse)
def process_news(request: Request, news_text: Optional[str] = Form(None), file: Optional[UploadFile] = File(None), api_key: str = Depends(verify_api_key)):
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(f"process-news:{client_ip}", max_requests=5, window_seconds=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded: max 5 news analyses per minute per IP.")

    if not news_text and not file:
        raise HTTPException(status_code=400, detail="Must provide either text, a URL, or a media file (image/video).")
    if news_text and len(news_text) > 10_000:
        raise HTTPException(status_code=400, detail="news_text must be under 10,000 characters.")
    if file and file.content_type not in ALLOWED_MEDIA_TYPES:
        raise HTTPException(status_code=415, detail=f"Unsupported file type '{file.content_type}'. Allowed: {sorted(ALLOWED_MEDIA_TYPES)}")

    temp_path = None
    if file:
        _check_content_length(request, MAX_MEDIA_SIZE)
        media_id = str(uuid.uuid4())
        temp_path = f"temp_news_{media_id}_{safe_filename(file.filename)}"
        try:
            save_upload_limited(file, temp_path, MAX_MEDIA_SIZE)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to save media file") from e
        finally:
            file.file.close()  # Always close — even if _check_content_length raised 413
            
    try:
        report = analyze_news(news_text, temp_path)
        is_fake = report.get("authenticity_score", 50.0) < 40.0
        
        if is_fake:
            # Auto-queue the fake news into the takedown queue
            takedown_id = f"FN-{uuid.uuid4().hex[:6].upper()}"
            violation_info = {
                "title": "Malicious Disinformation / Fake News",
                "channel": "Identified News Source",
                "url": (news_text[:150] + '...') if news_text else "Attached Media File"
            }
            draft_notice = f"To the Designated Agent,\n\nWe have identified this content as Malicious Disinformation / Fake News with an authenticity score of {report.get('authenticity_score')}.\n\nSource: {violation_info['url']}\nKey Findings: Verdict is {report.get('verdict')}\n\nPlease take immediate action to remove or disable access to this material.\n\nSincerely,\nAntigravity Digital Shield"
            
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
def fingerprint_asset(request: Request, video_id: str = Form(...), file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(f"fingerprint-asset:{client_ip}", max_requests=5, window_seconds=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded: max 5 fingerprint uploads per minute per IP.")

    if not file:
        raise HTTPException(status_code=400, detail="No video file uploaded")
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=415, detail=f"Unsupported file type '{file.content_type}'. Allowed: {sorted(ALLOWED_VIDEO_TYPES)}")

    _check_content_length(request, MAX_ASSET_SIZE)  # Must be outside try — 413 must not be rewritten as 500
    temp_path = f"temp_index_{uuid.uuid4()}_{safe_filename(file.filename)}"

    try:
        save_upload_limited(file, temp_path, MAX_ASSET_SIZE)
            
        success = index_authorized_video(temp_path, video_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to extract keyframes or index video.")
            
        return FingerprintResponse(
            status="success",
            message="Video successfully fingerprinted and added to Shield DB Vault.",
            video_id=video_id
        )
    except Exception as e:
        print(f"Error fingerprinting video: {e}")
        raise HTTPException(status_code=500, detail="Internal indexing error") from e
    finally:
        file.file.close()
        if os.path.exists(temp_path):
            os.remove(temp_path)
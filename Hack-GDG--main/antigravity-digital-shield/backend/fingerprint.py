import os
import sqlite3
import cv2
import imagehash
from PIL import Image

# ─────────────────────────────────────────────────────────────────────────────
# Fingerprint Vault — backed by shield.db (same DB as main.py)
# Replaces ChromaDB. Uses real Hamming distance, not cosine similarity on text.
# ─────────────────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shield.db")

HAMMING_THRESHOLD = 10  # bits — frames with distance <= this are considered a match


def _get_db():
    """Return a WAL-mode SQLite connection to the shared shield.db."""
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.execute("PRAGMA journal_mode=WAL")
    con.row_factory = sqlite3.Row
    return con


# Create fingerprints table on module load (safe to call if already exists)
with _get_db() as _init_con:
    _init_con.execute("""
        CREATE TABLE IF NOT EXISTS fingerprints (
            id        TEXT PRIMARY KEY,   -- "{video_id}_{frame_index}"
            video_id  TEXT NOT NULL,
            hash_hex  TEXT NOT NULL       -- dHash as 16-char hex string
        )
    """)


# ─────────────────────────────────────────────────────────────────────────────
# Frame extraction
# ─────────────────────────────────────────────────────────────────────────────

def extract_keyframes(video_path: str, num_frames: int = 10) -> list:
    """Extracts evenly spaced keyframes from a video using OpenCV."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Warning: Could not open video {video_path}")
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        cap.release()
        return []

    step = max(total_frames // num_frames, 1)
    frames = []

    for i in range(0, total_frames, step):
        if len(frames) >= num_frames:
            break
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR → RGB for PIL
            frames.append(frame)

    cap.release()
    return frames


# ─────────────────────────────────────────────────────────────────────────────
# Hashing utilities
# ─────────────────────────────────────────────────────────────────────────────

def generate_dhash(image_array) -> str:
    """Generates a 64-bit Difference Hash (dHash) and returns it as a hex string."""
    img = Image.fromarray(image_array)
    return str(imagehash.dhash(img))  # 16-char hex, e.g. "a3f9c2b7e10d4f68"


def hamming_distance(hash_hex_a: str, hash_hex_b: str) -> int:
    """
    Compute the Hamming distance between two dHash hex strings.
    XOR the integers, then count set bits (differing bit positions).
    This is the correct comparison for perceptual hashes — NOT cosine similarity.
    """
    try:
        return bin(int(hash_hex_a, 16) ^ int(hash_hex_b, 16)).count('1')
    except ValueError:
        return 64  # Max distance for a 64-bit hash — treat as no match


# ─────────────────────────────────────────────────────────────────────────────
# Public API (same signatures as before — main.py import is unchanged)
# ─────────────────────────────────────────────────────────────────────────────

def check_similarity(new_clip_path: str) -> dict:
    """
    Returns a match score (0–100%) for a video clip against the authorized vault.
    Extracts keyframes, generates dHashes, and compares via Hamming distance.
    A frame is 'matched' if its closest vault hash is within HAMMING_THRESHOLD bits.
    """
    frames = extract_keyframes(new_clip_path)
    if not frames:
        return {"score": 0.0, "message": "Could not extract frames."}

    # Load all authorized hashes once — one DB round-trip for the whole check
    with _get_db() as con:
        rows = con.execute("SELECT hash_hex FROM fingerprints").fetchall()
    vault_hashes = [r["hash_hex"] for r in rows]

    if not vault_hashes:
        return {"score": 0.0, "message": "Vault is empty — no authorized assets indexed yet."}

    total_frames = len(frames)
    matched_frames = 0

    for frame in frames:
        clip_hash = generate_dhash(frame)
        # Find the minimum Hamming distance to any fingerprint in the vault
        min_distance = min(hamming_distance(clip_hash, vh) for vh in vault_hashes)
        if min_distance <= HAMMING_THRESHOLD:
            matched_frames += 1

    score_percentage = (matched_frames / total_frames) * 100.0
    return {
        "score": score_percentage,
        "matched_frames": matched_frames,
        "total": total_frames,
    }


def index_authorized_video(video_path: str, video_id: str) -> bool:
    """Ingests an authorized video clip into the SQLite fingerprint vault."""
    frames = extract_keyframes(video_path)
    if not frames:
        return False

    with _get_db() as con:
        for i, frame in enumerate(frames):
            d_hash = generate_dhash(frame)
            # INSERT OR REPLACE allows re-indexing the same video_id safely
            con.execute(
                "INSERT OR REPLACE INTO fingerprints (id, video_id, hash_hex) VALUES (?, ?, ?)",
                (f"{video_id}_{i}", video_id, d_hash),
            )
    return True


def get_all_fingerprints() -> list:
    """Returns a list of unique indexed video assets with frame counts."""
    with _get_db() as con:
        rows = con.execute(
            "SELECT video_id, COUNT(*) as frame_count FROM fingerprints GROUP BY video_id"
        ).fetchall()

    return [
        {
            "id": r["video_id"],
            "name": f"Authorized Asset: {r['video_id']}",
            "date": "Shield DB Vault",
            "count": r["frame_count"],
            "matchRate": 100.0,
        }
        for r in rows
    ]

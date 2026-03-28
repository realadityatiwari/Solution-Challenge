import cv2
import imagehash
from PIL import Image
import chromadb

# Initialize Local ChromaDB MVP
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="authorized_vault")

def extract_keyframes(video_path, num_frames=10):
    """Extracts a set of evenly spaced keyframes from a video using OpenCV."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Warning: Could not open video {video_path}")
        return []
        
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        return []

    # Calculate frame steps
    step = max(total_frames // num_frames, 1)
    frames = []

    for i in range(0, total_frames, step):
        if len(frames) >= num_frames:
            break
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            # Convert BGR to RGB for PIL
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
            
    cap.release()
    return frames

def generate_dhash(image_array):
    """Generates a Difference Hash (dHash) for an image array."""
    img = Image.fromarray(image_array)
    # Return as string to store in DB
    return str(imagehash.dhash(img))

def check_similarity(new_clip_path, threshold_distance=10):
    """
    Returns a matching score against our 'Authorized Vault' of sports clips.
    Extracts keyframes of the new clip, gets dHashes, and queries ChromaDB MVP.
    """
    frames = extract_keyframes(new_clip_path)
    if not frames:
        return {"score": 0.0, "message": "Could not extract frames."}
        
    total_frames = len(frames)
    matched_frames = 0
    
    # Note: In MVP, Chroma uses sentence-transformers to embed the dHash string.
    # A true system would index binary vectors and search by Hamming Distance in Vector DB, 
    # but storing standard string hashes in Chroma MVP suffices for mocking logic flow.
    for frame in frames:
        clip_hash = generate_dhash(frame)
        
        results = collection.query(
            query_texts=[clip_hash],
            n_results=1
        )
        
        # Check against an arbitrary distance threshold indicating "close text"
        if results['distances'] and len(results['distances'][0]) > 0:
            distance = results['distances'][0][0]
            if distance < 1.0:
                matched_frames += 1
                
    score_percentage = (matched_frames / total_frames) * 100.0
    return {"score": score_percentage, "matched_frames": matched_frames, "total": total_frames}

def index_authorized_video(video_path, video_id):
    """Helper script to ingest an authorized sports clip into the vault."""
    frames = extract_keyframes(video_path)
    if not frames:
        return False
        
    documents = []
    ids = []
    
    for i, frame in enumerate(frames):
        d_hash = generate_dhash(frame)
        documents.append(d_hash)
        ids.append(f"{video_id}_{i}")
        
    collection.add(
        documents=documents,
        ids=ids,
        metadatas=[{"video_id": video_id, "type": "authorized"}] * len(frames)
    )
    return True

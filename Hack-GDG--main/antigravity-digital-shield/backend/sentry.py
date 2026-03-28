import json
import logging
from datetime import datetime
from fingerprint import check_similarity
import cv2
import numpy as np
import os

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def create_dummy_video(path):
    """Creates a tiny dummy video file to represent a downloaded YouTube snippet for the MVP."""
    out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (64, 64))
    frame = np.zeros((64, 64, 3), dtype=np.uint8)
    out.write(frame)
    out.release()

def run_sentry_pipeline():
    # Load metadata dumped by Browser Agent
    try:
        with open("scraped_data.json", "r") as f:
            scraped_data = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load scraped data: {e}")
        return

    logging.info(f"Sentry Agent: Starting scan of {len(scraped_data)} videos...")
    
    with open("violations.log", "a") as log_file:
        for video in scraped_data:
            logging.info(f"Processing URL: {video['video_url']}")
            
            # 1. Download snippet (Mocked via dummy video)
            video_id = video['video_url'].split('v=')[-1]
            temp_video_path = f"temp_{video_id}.mp4"
            create_dummy_video(temp_video_path)
            
            # 2. Pass to Validator (fingerprint.check_similarity)
            # This extracts keyframes and checks against ChromaDB
            result = check_similarity(temp_video_path)
            
            # For MVP simulation: 'NBA' official channel videos force a severe match score
            if "NBA" in video["channel_name"]:
                score = 99.1
            else:
                score = result.get("score", 0.0)
            
            # 3. Update violations.log if match found
            if score > 50.0:
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "title": video["title"],
                    "url": video["video_url"],
                    "channel": video["channel_name"],
                    "match_score": score,
                    "status": "Flagged for Analyst Review"
                }
                log_file.write(json.dumps(log_entry) + "\n")
                logging.warning(f"VIOLATION LOGGED: {video['title']} (Score: {score}%)")
            else:
                logging.info(f"CLEAR: {video['title']}")
                
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
                
    logging.info("Sentry pipeline complete.")

if __name__ == "__main__":
    run_sentry_pipeline()

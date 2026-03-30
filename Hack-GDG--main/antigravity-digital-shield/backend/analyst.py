import json
import logging
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Any

import os
from dotenv import load_dotenv

# Ensure GOOGLE_API_KEY is available in your environment variables
load_dotenv()
client = None
try:
    client = genai.Client()
except Exception as e:
    logging.warning(f"Could not initialize genai.Client: {e}. Set GOOGLE_API_KEY environment variable.")


class ViolationReport(BaseModel):
    is_official_broadcast: bool
    source_type: str = Field(description="official broadcast stream, social media re-post, or fan-filmed footage")
    logos_identified: list[str]
    scoreboards_detected: bool
    commentary_style: str
    violation_likelihood: float = Field(description="Score between 0.0 and 1.0 indicating likelihood of IP violation.")
    reasoning: str

def analyze_video(video_path: str) -> dict[str, Any]:
    """
    Service that sends suspicious video snippets to Gemini 1.5 Flash.
    Acts as an IP Protection Officer to analyze sports media streams.
    Ensures the JSON response includes a violation_likelihood score.
    """
    logging.info("Uploading suspicious clip for analysis: %s", video_path)
    
    if client is None:
        return {"error": "GenAI Client is not initialized. Please set GOOGLE_API_KEY environment variable.", "violation_likelihood": 0.0}
    
    try:
        # Upload the video file using the GenAI File API
        video_file = client.files.upload(file=video_path)
    except Exception as e:
        return {"error": f"Failed to upload video to Gemini: {str(e)}", "violation_likelihood": 0.0}
    
    system_instruction = (
        "You are an IP Protection Officer. Analyze this video. "
        "Is this an official broadcast stream, a social media re-post, or fan-filmed footage? "
        "Identify logos, scoreboards, and commentary style."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                video_file, 
                "Please analyze the video snippet carefully and provide a rigorous violation likelihood score."
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=ViolationReport,
                temperature=0.2
            )
        )
        
        # Parse the structured JSON output
        parsed_data = json.loads(response.text)
        
        # Verify output includes violation_likelihood
        if "violation_likelihood" not in parsed_data:
            parsed_data["violation_likelihood"] = 0.0
            parsed_data["error"] = "Agent failed to provide violation_likelihood score."
        else:
            # Ensure it is a float
            parsed_data["violation_likelihood"] = float(parsed_data["violation_likelihood"])
            
        return parsed_data
        
    except Exception as e:
        logging.error("Failed to analyze video with Gemini: %s", str(e))
        return {
            "error": "Model reasoning failed or output format was invalid.",
            "violation_likelihood": 0.0
        }
    finally:
        # Clean up the file to minimize storage costs
        try:
            client.files.delete(name=video_file.name)
        except Exception:
            pass

    return {
        "error": "Unexpected execution path",
        "violation_likelihood": 0.0
    }

class NewsViolationReport(BaseModel):
    authenticity_verdict: str = Field(description="A quick single-word/phrase summary: Verified, Mostly True, Mixed/Unverified, Mostly False, Completely Fake")
    fake_probability: float = Field(description="Decimal ranging 0.0 to 1.0 reflecting how likely the news is FAKE (1.0 = completely fake, 0.0 = completely true)")
    key_claims_analysis: list[str] = Field(description="Break down the major claims made in the text and analyze the likelihood of each being true or false based on logical consistency")
    red_flags: list[str] = Field(description="Identify any sensationalism, emotional manipulation, logical fallacies, or lack of verifiable sources")
    contextual_gaps: str = Field(description="Point out what information is missing that would be necessary to fully verify the story")

def analyze_news(news_text: str = None, media_path: str = None) -> dict[str, Any]:
    """
    Checks news articles, text paragraphs, URLs, images, or videos for fake news, misinformation, and deepfakes.
    """
    logging.info("Analyzing news snippet (text len: %s, media: %s)", len(news_text) if news_text else 0, media_path)
    
    if client is None:
        return {"error": "GenAI Client is not initialized.", "confidence_score": 0.0}
        
    system_instruction = (
        "You are an Elite Omni-Modal Forensics and Fake News Detection AI. Your objective is rigorous truth deduction.\n\n"
        "You evaluate unstructured data across modalities: URLs, links, text, paragraphs, photos, and videos. Apply these investigative protocols:\n"
        "► TEXT & PARAGRAPHS: Detect clickbait structures, logical fallacies, emotional manipulation, and contradictions. Check if paragraphs logically follow each other or rely on unsourced rumors.\n"
        "► URLs & LINKS: Analyze domains mentioned for credibility (e.g., recognizable mainstream sites versus 'pink slime' journalism hubs, deceptive typosquatting, or known propaganda outlets).\n"
        "► PHOTOS: Conduct visual forensics looking for AI-generated artifacts (e.g., six fingers, garbled text, unnatural skin textures, perfect symmetry, or impossible lighting).\n"
        "► VIDEOS: Screen for temporal deepfakes, unnatural blinking, synthetic voice cloning artifacts, disjointed audio/visual sync, and physical physics impossibilities.\n\n"
        "Provide a detailed report strictly reflecting this structure:\n"
        "1. Authenticity Verdict: A quick phrase summary.\n"
        "2. Fake Probability Score: 0.0 to 1.0 where 1.0 means COMPLETELY FAKE or DECEPTIVE, and 0.0 means 100% FACTUAL VERIFIED TRUTH.\n"
        "3. Key Claims Analysis: Map out claims from the text, URL content hints, or media. Analyze their strict likelihood of truth.\n"
        "4. Red Flags: List any detected manipulation tactics, AI hallmarks in media, or suspiciously unreliable domain links.\n"
        "5. Contextual Gaps: Point out missing official sources, unverified quotes, or lack of credible corroboration."
    )
    
    contents = []
    if news_text:
        contents.append(news_text)
        
    uploaded_file = None
    try:
        if media_path:
            uploaded_file = client.files.upload(file=media_path)
            contents.append(uploaded_file)
            
        contents.append("Please evaluate the provided URLs, text paragraphs, photos, or videos utilizing your rigorous advanced forensics protocol. Output in EXACT structured JSON schema.")
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=NewsViolationReport,
                temperature=0.2
            )
        )
        
        parsed_data = json.loads(response.text)
        
        if "fake_probability" not in parsed_data:
            parsed_data["fake_probability"] = 0.0
            parsed_data["error"] = "Agent failed to provide fake_probability."
        else:
            parsed_data["fake_probability"] = float(parsed_data["fake_probability"])
            
        return parsed_data
        
    except Exception as e:
        logging.error("Failed to analyze news data: %s", str(e))
        return {
            "error": "Model reasoning failed or output format was invalid.",
            "fake_probability": 0.0
        }
    finally:
        # Clean up the file to minimize storage costs
        if uploaded_file:
            try:
                client.files.delete(name=uploaded_file.name)
            except Exception:
                pass


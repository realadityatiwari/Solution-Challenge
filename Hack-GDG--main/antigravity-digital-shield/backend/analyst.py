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
            model='gemini-1.5-flash',
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
    classification: str = Field(description="Authentic, Misleading, Manipulated, Fake / Fabricated, or Unauthorized Redistribution")
    confidence_score: float = Field(description="Decimal ranging 0.0 to 1.0 reflecting your confidence")
    source_credibility: str = Field(description="Official, Verified Media, Suspicious, or Unknown")
    misappropriation_detected: bool = Field(description="True if content appears reused without authorization")
    anomaly_detected: bool = Field(description="True if content is spreading in a suspicious pattern")
    key_flags: list[str] = Field(description="Inconsistencies or suspicious elements identified")
    explanation: str = Field(description="Clear explanation of WHY the content was flagged")
    takedown_letter_draft: str = Field(description="Formal Cease & Desist / Warning letter generated if fake or misappropriated. Leave empty if authentic.")

def analyze_news(news_text: str = None, image_path: str = None) -> dict[str, Any]:
    """
    Checks news articles, text transcripts, or images for unauthorized use of broadcast IP.
    """
    logging.info("Analyzing news snippet (text len: %s, image: %s)", len(news_text) if news_text else 0, image_path)
    
    if client is None:
        return {"error": "GenAI Client is not initialized.", "confidence_score": 0.0}
        
    system_instruction = (
        "You are an advanced Digital Asset Protection and Fake News Detection AI specializing in sports media.\n"
        "Your responsibilities include:\n"
        "1. CONTENT AUTHENTICITY ANALYSIS: Determine whether the given sports-related content is authentic, manipulated, or potentially fake. Identify signs of tampering, misleading edits, or deepfake characteristics.\n"
        "2. SOURCE VERIFICATION: Evaluate the credibility of the source. Classify sources as: Official, Verified Media, Suspicious, or Unknown. Cross-check claims with known patterns of official sports communication.\n"
        "3. MISAPPROPRIATION DETECTION: Detect if the content appears to be reused, reposted, or redistributed without authorization. Identify watermark absence, altered branding, or mismatched metadata.\n"
        "4. VIRAL ANOMALY DETECTION: Flag sudden spikes, bot-like distribution, or coordinated sharing.\n"
        "5. FAKE NEWS CLASSIFICATION: Classify the content strictly as: Authentic, Misleading, Manipulated, Fake / Fabricated, or Unauthorized Redistribution.\n"
        "6. CONFIDENCE SCORE: Parse out to a float matching 0.0 to 1.0 based on analysis.\n"
        "7. EXPLANATION: Clearly explain WHY the content was flagged. Highlight specific inconsistencies, suspicious elements, or verification failures.\n"
        "Rules: Be skeptical but not biased. Do not assume content is fake without evidence. Prefer structured reasoning over vague statements. Focus on sports media context.\n"
        "If classification is fake or misappropriated, draft a legal takedown letter."
    )
    
    contents = []
    if news_text:
        contents.append(news_text)
        
    uploaded_file = None
    try:
        if image_path:
            uploaded_file = client.files.upload(file=image_path)
            contents.append(uploaded_file)
            
        contents.append("Please output in the exact requested STRICT JSON format per the defined rules.")
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=NewsViolationReport,
                temperature=0.2
            )
        )
        
        parsed_data = json.loads(response.text)
        
        if "confidence_score" not in parsed_data:
            parsed_data["confidence_score"] = 0.0
            parsed_data["error"] = "Agent failed to provide confidence_score."
        else:
            parsed_data["confidence_score"] = float(parsed_data["confidence_score"])
            
        return parsed_data
        
    except Exception as e:
        logging.error("Failed to analyze news data: %s", str(e))
        return {
            "error": "Model reasoning failed or output format was invalid.",
            "confidence_score": 0.0
        }
    finally:
        # Clean up the file to minimize storage costs
        if uploaded_file:
            try:
                client.files.delete(name=uploaded_file.name)
            except Exception:
                pass


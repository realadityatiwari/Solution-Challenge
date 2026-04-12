import json
import logging
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Any, Optional

import os
from dotenv import load_dotenv

# Load training data for few-shot learning
try:
    from training_data import build_few_shot_context, get_category_specific_instructions, NEWS_CATEGORIES
except ImportError:
    def build_few_shot_context(num_examples=6): return ""
    def get_category_specific_instructions(cat): return ""
    NEWS_CATEGORIES = []

load_dotenv()
client = None
try:
    client = genai.Client()
except Exception as e:
    logging.warning(f"Could not initialize genai.Client: {e}. Set GOOGLE_API_KEY environment variable.")


# =============================================================================
# VIDEO IP VIOLATION ANALYZER
# =============================================================================

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
    Service that sends suspicious video snippets to Gemini 2.5 Flash.
    Acts as an IP Protection Officer to analyze sports media streams.
    """
    logging.info("Uploading suspicious clip for analysis: %s", video_path)

    if client is None:
        return {"error": "GenAI Client is not initialized. Please set GOOGLE_API_KEY environment variable.", "violation_likelihood": 0.0}

    try:
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
                temperature=0.1
            )
        )
        parsed_data = json.loads(response.text)
        if "violation_likelihood" not in parsed_data:
            parsed_data["violation_likelihood"] = 0.0
            parsed_data["error"] = "Agent failed to provide violation_likelihood score."
        else:
            parsed_data["violation_likelihood"] = float(parsed_data["violation_likelihood"])
        return parsed_data

    except Exception as e:
        logging.error("Failed to analyze video with Gemini: %s", str(e))
        return {"error": "Model reasoning failed or output format was invalid.", "violation_likelihood": 0.0}
    finally:
        try:
            client.files.delete(name=video_file.name)
        except Exception:
            pass
    return {"error": "Unexpected execution path", "violation_likelihood": 0.0}


# =============================================================================
# FAKE NEWS DETECTOR — ENHANCED WITH FEW-SHOT TRAINING
# =============================================================================

class NewsViolationReport(BaseModel):
    authenticity_verdict: str = Field(
        description="A quick single-word/phrase summary: Verified, Mostly True, Mixed/Unverified, Mostly False, Completely Fake"
    )
    fake_probability: float = Field(
        description="Decimal ranging 0.0 to 1.0 reflecting how likely the news is FAKE (1.0 = completely fake, 0.0 = completely true)"
    )
    category_detected: str = Field(
        description=f"The most likely news category. Choose from: {', '.join(NEWS_CATEGORIES)}, or 'General News' if none match."
    )
    key_claims_analysis: list[str] = Field(
        description="Break down the major claims made in the text and analyze the likelihood of each being true or false based on logical consistency and known facts"
    )
    red_flags: list[str] = Field(
        description="Identify any sensationalism, emotional manipulation, logical fallacies, conspiracy framing, lack of verifiable sources, dangerous advice, or AI-generated media artifacts"
    )
    source_credibility_indicators: list[str] = Field(
        description="List any credibility signals found (named institutions, specific numbers, named officials, cited journals) or their absence"
    )
    contextual_gaps: str = Field(
        description="Point out what verifiable information is missing that would be necessary to fully authenticate the story"
    )
    reasoning: str = Field(
        description="A concise expert reasoning paragraph explaining your verdict and score"
    )


def detect_category_hint(news_text: str) -> str:
    """Quick keyword-based category hint to load targeted instructions."""
    if not news_text:
        return "General News"

    text_lower = news_text.lower()
    category_keywords = {
        "Politics & Elections": ["election", "vote", "senate", "congress", "president", "parliament", "democrat", "republican", "legislation", "poll"],
        "Health & Medicine": ["cure", "vaccine", "fda", "doctor", "hospital", "disease", "cancer", "covid", "virus", "drug", "pharmaceutical", "health"],
        "Science & Climate": ["nasa", "climate", "global warming", "carbon", "scientist", "research", "study", "physics", "chemistry", "biology", "fossil"],
        "Finance & Cryptocurrency": ["bitcoin", "crypto", "invest", "stock", "fed", "interest rate", "market", "doge", "ethereum", "dollar", "bank"],
        "War & Conflict": ["war", "military", "soldiers", "nato", "bomb", "attack", "killed", "ceasefire", "troops", "invasion", "conflict", "ukraine", "gaza"],
        "Entertainment & Celebrity": ["celebrity", "actor", "singer", "movie", "oscar", "grammy", "album", "film", "star", "hollywood", "taylor", "beyonce"],
        "Technology & AI": ["ai", "artificial intelligence", "chip", "apple", "google", "microsoft", "software", "algorithm", "robot", "tech", "startup"],
        "Sports": [
            # General sports terms
            "match", "game", "nba", "nfl", "soccer", "football", "basketball",
            "championship", "player", "coach", "league", "fifa", "olympic",
            # Cricket & IPL specific
            "cricket", "ipl", "bcci", "icc", "wicket", "batsman", "bowler",
            "test match", "odi", "t20", "world cup", "msd", "dhoni", "kohli",
            "tendulkar", "sachin", "rohit", "hardik", "pandya", "pant",
            "csk", "rcb", "mi", "kkr", "srh", "dc", "gt", "lsg", "punjab",
            # Football / Soccer
            "premier league", "champions league", "transfer", "messi", "ronaldo",
            "neymar", "haaland", "mbappe", "guardiola", "referee", "pgmol",
            "al-nassr", "al hilal", "manchester", "arsenal", "chelsea", "psg",
            # Tennis & Racquet sports
            "djokovic", "federer", "nadal", "wimbledon", "grand slam", "atp",
            "wta", "tennis", "badminton", "sindhu",
            # Athletics & Olympics
            "javelin", "sprint", "marathon", "bolt", "neeraj", "chopra",
            "olympics", "gold medal", "silver medal", "bronze medal",
            "paris 2024", "tokyo 2020", "beijing", "world athletics",
            # Anti-doping
            "doping", "wada", "nada", "steroids", "epo", "banned substance",
            "drug test", "anti-doping", "cas", "tribunal", "suspension",
            # Match-fixing & betting
            "match fix", "spot fix", "toss fix", "bookie", "betting",
            "fixed result", "guaranteed win", "telegram tips", "insider tips",
            "acu", "anti-corruption",
            # Retirement & transfers
            "retirement", "retire", "transfer fee", "contract signed", "done deal",
            "here we go", "pre-contract", "release clause",
            # Records & stats
            "world record", "all-time", "most runs", "highest scorer",
            "career average", "stats", "goat",
        ],
        "Crime & Conspiracy": ["illuminati", "conspiracy", "secret", "cover-up", "elite", "globalist", "nwo", "arrested", "murder", "trafficking"],
        "Natural Disasters": ["earthquake", "tsunami", "hurricane", "flood", "tornado", "wildfire", "eruption", "disaster", "magnitude", "usgs"],
        "Religion & Culture": ["god", "allah", "church", "mosque", "bible", "quran", "pope", "religious", "faith", "prophet", "temple"],
        "Social Media Viral Content": ["share", "retweet", "viral", "trending", "tiktok", "instagram", "facebook", "whatsapp", "forward this", "chain"],
    }

    scores = {}
    for category, keywords in category_keywords.items():
        scores[category] = sum(1 for kw in keywords if kw in text_lower)

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General News"


def analyze_news(news_text: str = None, media_path: str = None) -> dict[str, Any]:
    """
    Enhanced fake news detector with few-shot training across 12+ news categories.
    Checks news articles, text paragraphs, URLs, images, or videos for fake news,
    misinformation, propaganda, and deepfakes.
    """
    logging.info("Analyzing news snippet (text len: %s, media: %s)", len(news_text) if news_text else 0, media_path)

    if client is None:
        return {"error": "GenAI Client is not initialized.", "confidence_score": 0.0}

    # Auto-detect news category for targeted analysis protocols
    detected_category = detect_category_hint(news_text or "")
    category_instructions = get_category_specific_instructions(detected_category)

    # Build few-shot calibration examples
    few_shot_block = build_few_shot_context(num_examples=6)

    system_instruction = (
        "You are ARGUS — an Elite Omni-Modal Forensics and Fake News Detection AI with expert-level knowledge "
        "in journalism, fact-checking, propaganda analysis, media forensics, and deep knowledge of current global events.\n\n"

        "═══════════════════════════════════════════════════════════\n"
        "YOUR CORE MISSION:\n"
        "═══════════════════════════════════════════════════════════\n"
        "Protect citizens from misinformation, disinformation, propaganda, deepfakes, health hoaxes, "
        "financial scams, political manipulation, and all forms of dishonest content.\n\n"

        "You evaluate ALL content modalities:\n"
        "► TEXT & PARAGRAPHS: Detect clickbait, logical fallacies, emotional manipulation, unsourced rumors, "
        "conspiracy framing, FOMO tactics, and contradictions within the text itself.\n"
        "► URLs & LINKS: Analyze domains for reputation (mainstream vs. pink-slime journalism, typosquatting, "
        "known propaganda networks, satire sites being shared as real news).\n"
        "► PHOTOS & IMAGES: Forensic visual analysis for AI-generation artifacts (extra fingers, distorted text, "
        "inconsistent lighting/shadows, impossible anatomy, DALL-E or Midjourney hallmarks), cropping manipulation, "
        "and reverse-image context theft.\n"
        "► VIDEOS: Temporal deepfake detection (unnatural blinking, synthetic voice artifacts, audio/visual sync errors, "
        "facial morphing boundaries), physics impossibilities, and metadata inconsistencies.\n\n"

        "═══════════════════════════════════════════════════════════\n"
        "FAKE NEWS TYPE ENCYCLOPEDIA — KNOW ALL THESE PATTERNS:\n"
        "═══════════════════════════════════════════════════════════\n"
        "1. FABRICATED CONTENT: Completely invented stories with no basis in reality.\n"
        "2. MANIPULATED CONTENT: Real images/videos altered to change meaning.\n"
        "3. MISLEADING FRAMING: True facts presented with false context.\n"
        "4. IMPOSTER CONTENT: Content spoofing credible sources (fake AP, BBC, Reuters accounts).\n"
        "5. SATIRE MISREPRESENTED: Satirical content shared as real news without context.\n"
        "6. PROPAGANDA: Content designed to advance a political/ideological agenda, often via emotional appeals.\n"
        "7. HEALTH MISINFORMATION: Unscientific medical claims that could harm people.\n"
        "8. FINANCIAL FRAUD: Pump-and-dump schemes, fake endorsements, get-rich-quick scams.\n"
        "9. CONSPIRACY THEORIES: Unfalsifiable claims about secret powerful groups controlling events.\n"
        "10. DEEPFAKE MEDIA: AI-generated audio/video putting false words in real people's mouths.\n"
        "11. ASTROTURFING: Coordinated inauthentic behavior designed to look like grassroots support.\n"
        "12. CLICKBAIT EXAGGERATION: Real story with massively exaggerated headline or framing.\n\n"

        "═══════════════════════════════════════════════════════════\n"
        "UNIVERSAL RED FLAG SIGNALS:\n"
        "═══════════════════════════════════════════════════════════\n"
        "• 'SHARE BEFORE THEY DELETE THIS' / 'THEY DON'T WANT YOU TO SEE THIS'\n"
        "• Unnamed anonymous sources for critical claims\n"
        "• Miracle cure / guaranteed investment return claims\n"
        "• Celebrity name-drops for financial endorsements\n"
        "• Secret government/Vatican/elite actions with convenient lack of evidence\n"
        "• Human cloning, alien revelation, HAARP weather weapons claims\n"
        "• Statistics without sources (e.g., '97% of scientists agree' with no citation)\n"
        "• Emotional language designed to bypass critical thinking (fear, outrage, pride)\n"
        "• Claims procedurally impossible under known law or physics\n\n"

        f"CATEGORY-SPECIFIC FORENSIC PROTOCOLS FOR THIS CONTENT:\n"
        f"{category_instructions}\n\n"

        f"{few_shot_block}\n\n"

        "═══════════════════════════════════════════════════════════\n"
        "OUTPUT REQUIREMENTS:\n"
        "═══════════════════════════════════════════════════════════\n"
        "Provide your complete structured JSON analysis. Be precise, forensically rigorous, and evidence-based.\n"
        "Your fake_probability score MUST be calibrated against the examples above.\n"
        "If the content is dangerous (promotes violence, harmful health advice, financial fraud) bias toward higher scores.\n"
        "If the content has multiple named officials, specific numbers, and institutional sources, bias toward lower scores."
    )

    contents = []
    if news_text:
        contents.append(news_text)

    uploaded_file = None
    try:
        if media_path:
            uploaded_file = client.files.upload(file=media_path)
            contents.append(uploaded_file)

        contents.append(
            "Perform a complete ARGUS forensic analysis on the provided content. "
            "Identify the news category, apply the relevant detection protocols, "
            "and output your structured JSON verdict with full reasoning."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=NewsViolationReport,
                temperature=0.1  # Low temperature = consistent, deterministic analysis
            )
        )

        parsed_data = json.loads(response.text)

        if "fake_probability" not in parsed_data:
            parsed_data["fake_probability"] = 0.0
            parsed_data["error"] = "Agent failed to provide fake_probability."
        else:
            parsed_data["fake_probability"] = float(parsed_data["fake_probability"])

        # Add the auto-detected category as a hint (Gemini may override with its own detection)
        if "category_detected" not in parsed_data:
            parsed_data["category_detected"] = detected_category

        logging.info(
            "ARGUS Analysis Complete — Category: %s | Verdict: %s | Fake Prob: %.2f",
            parsed_data.get("category_detected", "Unknown"),
            parsed_data.get("authenticity_verdict", "Unknown"),
            parsed_data.get("fake_probability", 0.0)
        )

        return parsed_data

    except Exception as e:
        logging.error("Failed to analyze news data: %s", str(e))
        return {
            "error": "ARGUS model reasoning failed or output format was invalid.",
            "fake_probability": 0.0
        }
    finally:
        if uploaded_file:
            try:
                client.files.delete(name=uploaded_file.name)
            except Exception:
                pass

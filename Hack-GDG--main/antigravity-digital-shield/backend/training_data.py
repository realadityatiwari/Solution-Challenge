"""
training_data.py — Few-Shot Training Library for Antigravity Digital Shield
Curated labeled examples across 12+ news categories to guide Gemini's fake news detection.
These are injected as few-shot context into every analysis request.
"""

# =============================================================================
# CATEGORY DEFINITIONS
# =============================================================================
NEWS_CATEGORIES = [
    "Politics & Elections",
    "Health & Medicine",
    "Science & Climate",
    "Finance & Cryptocurrency",
    "War & Conflict",
    "Entertainment & Celebrity",
    "Religion & Culture",
    "Sports",
    "Technology & AI",
    "Crime & Conspiracy",
    "Natural Disasters",
    "Social Media Viral Content",
]

# =============================================================================
# LABELED TRAINING EXAMPLES
# Each entry: { "category", "label" (REAL/FAKE), "text", "verdict", "fake_probability", "red_flags", "explanation" }
# =============================================================================

TRAINING_EXAMPLES = [

    # ─────────────────────────────────────────────────────
    # POLITICS & ELECTIONS
    # ─────────────────────────────────────────────────────
    {
        "category": "Politics & Elections",
        "label": "FAKE",
        "text": "BREAKING: The entire U.S. Senate secretly voted to abolish the Electoral College at 3am in a closed session that C-SPAN was banned from covering! Share before they delete this!",
        "verdict": "Completely Fake",
        "fake_probability": 0.97,
        "red_flags": [
            "Unverifiable secret session claim",
            "Urgency bait phrase 'share before they delete this'",
            "No named sources or verifiable details",
            "Procedurally impossible — abolishing Electoral College requires Constitutional amendment ratified by 38 states",
            "Emotional panic-inducing language",
        ],
        "explanation": "Constitutional amendments cannot be passed by the Senate alone in a secret vote. This is a classic fabricated political conspiracy story designed to spread panic and distrust in democratic institutions."
    },
    {
        "category": "Politics & Elections",
        "label": "FAKE",
        "text": "Leaked document proves voting machines in 6 states were hacked by foreign actors and flipped 2 million votes. The mainstream media is covering it up!",
        "verdict": "Completely Fake",
        "fake_probability": 0.95,
        "red_flags": [
            "Unverified 'leaked document' with no source",
            "Conspiracy narrative claiming media cover-up",
            "Specific numbers (2 million) without any evidence chain",
            "No corroboration from election security agencies (CISA, FBI)",
        ],
        "explanation": "Election fraud claims of this scale would require certification from multiple independent auditing bodies. Vague 'leaked document' claims with no verifiable source and media cover-up framing are hallmarks of election disinformation."
    },
    {
        "category": "Politics & Elections",
        "label": "REAL",
        "text": "The Senate passed the bipartisan infrastructure bill 69-30 on Tuesday, sending it to the House for a vote. The $1 trillion package includes funding for roads, bridges, broadband, and public transit, according to the Congressional Budget Office.",
        "verdict": "Verified",
        "fake_probability": 0.04,
        "red_flags": [],
        "explanation": "Specific vote count (69-30), bipartisan framing, references named legislative body (CBO), mentions specific funding categories. All verifiable through public Congressional records."
    },

    # ─────────────────────────────────────────────────────
    # HEALTH & MEDICINE
    # ─────────────────────────────────────────────────────
    {
        "category": "Health & Medicine",
        "label": "FAKE",
        "text": "URGENT: Doctors don't want you to know that drinking bleach mixed with lemon juice for 7 days CURES cancer. Big Pharma is suppressing this miracle cure!",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "Dangerous health misinformation — bleach is lethal if ingested",
            "'Doctors don't want you to know' is a classic conspiracy trigger phrase",
            "Big Pharma suppression narrative with zero evidence",
            "No clinical trials, no peer-reviewed studies cited",
            "Miracle cure claim for a complex disease",
        ],
        "explanation": "Ingesting bleach is medically proven to be fatal. This is an extremely dangerous piece of health misinformation that could cause real harm. Zero scientific basis."
    },
    {
        "category": "Health & Medicine",
        "label": "FAKE",
        "text": "5G towers are causing COVID-19. The virus is actually radiation poisoning being disguised as a pandemic. Over 200 scientists have signed a petition confirming this.",
        "verdict": "Completely Fake",
        "fake_probability": 0.98,
        "red_flags": [
            "Scientifically debunked — 5G is non-ionizing radiation incapable of causing viral illness",
            "Fabricated 200-scientist petition — no verifiable list exists",
            "Conflates radiation with viral biology — impossible mechanism",
            "COVID-19 spread patterns (isolated islands, 5G-free regions) directly contradict this",
        ],
        "explanation": "5G technology operates using radio waves that cannot transmit or cause viral infections. SARS-CoV-2 has been isolated, sequenced, and studied independently by thousands of labs worldwide with no 5G correlation."
    },
    {
        "category": "Health & Medicine",
        "label": "REAL",
        "text": "The FDA approved the first gene therapy for sickle cell disease, a historical milestone that could potentially cure the condition affecting approximately 100,000 Americans, primarily of African descent. The therapy, developed by Vertex Pharmaceuticals and CRISPR Therapeutics, involves editing patients' own stem cells.",
        "verdict": "Verified",
        "fake_probability": 0.05,
        "red_flags": [],
        "explanation": "References specific FDA regulatory body, names the companies (Vertex/CRISPR Therapeutics), provides verifiable patient demographics, describes the mechanism (stem cell editing). This matches real medical news patterns."
    },

    # ─────────────────────────────────────────────────────
    # SCIENCE & CLIMATE
    # ─────────────────────────────────────────────────────
    {
        "category": "Science & Climate",
        "label": "FAKE",
        "text": "NASA scientists have ADMITTED that climate change is a total hoax invented by globalists in 1988 to control energy prices. The earth has been cooling for 40 years.",
        "verdict": "Completely Fake",
        "fake_probability": 0.96,
        "red_flags": [
            "False attribution to NASA — no such statement exists on record",
            "'Globalist' framing is a political conspiracy dog whistle",
            "Directly contradicts 150+ years of temperature data and thousands of peer-reviewed studies",
            "Earth has measurably warmed 1.1°C since pre-industrial era — falsifiable claim",
        ],
        "explanation": "NASA's own published satellite data consistently confirms global warming trends. No such admission exists. The 40-year cooling claim is directly contradicted by publicly available NOAA and NASA climate datasets."
    },
    {
        "category": "Science & Climate",
        "label": "REAL",
        "text": "Scientists at MIT have developed a new battery technology using aluminum-sulfur chemistry that could dramatically reduce the cost of grid-scale energy storage. The research, published in Nature Energy, shows it could cost one-sixth the price of lithium-ion batteries.",
        "verdict": "Verified",
        "fake_probability": 0.06,
        "red_flags": [],
        "explanation": "References MIT, names the specific chemistry (aluminum-sulfur), cites journal (Nature Energy), provides comparative cost metric. All elements are verifiable through the journal publication."
    },

    # ─────────────────────────────────────────────────────
    # FINANCE & CRYPTOCURRENCY
    # ─────────────────────────────────────────────────────
    {
        "category": "Finance & Cryptocurrency",
        "label": "FAKE",
        "text": "URGENT INVESTMENT ALERT: Elon Musk just tweeted that he's personally investing $50 billion into DogeGoldX coin. Get in NOW before it moons 10,000%. This isn't financial advice but BUY NOW!!!",
        "verdict": "Completely Fake",
        "fake_probability": 0.98,
        "red_flags": [
            "Celebrity name-drop (Elon Musk) to create false credibility",
            "Extreme FOMO language ('BUY NOW', 'moons 10,000%')",
            "Pump-and-dump crypto scheme hallmarks",
            "Contradictory disclaimer ('not financial advice') alongside direct buy command",
            "Urgency manipulation — no time to verify",
        ],
        "explanation": "Classic pump-and-dump crypto promotion scheme. Uses fabricated celebrity endorsement, extreme urgency, and FOMO tactics. Any 10,000% return claim is a guaranteed red flag for financial fraud."
    },
    {
        "category": "Finance & Cryptocurrency",
        "label": "REAL",
        "text": "The Federal Reserve raised interest rates by 25 basis points Wednesday, bringing the federal funds rate to a 22-year high of 5.25-5.50%. Fed Chair Jerome Powell stated in a press conference that additional hikes remain possible depending on incoming economic data.",
        "verdict": "Verified",
        "fake_probability": 0.03,
        "red_flags": [],
        "explanation": "Names specific institution (Federal Reserve), exact rate change (25 basis points), precise range (5.25-5.50%), named official (Jerome Powell). All verifiable through Fed press releases."
    },

    # ─────────────────────────────────────────────────────
    # WAR & CONFLICT
    # ─────────────────────────────────────────────────────
    {
        "category": "War & Conflict",
        "label": "FAKE",
        "text": "EXCLUSIVE VIDEO: Ukrainian soldiers caught on camera executing Russian prisoners in cold blood — proof that NATO is funding war crimes! (video attached)",
        "verdict": "Completely Fake",
        "fake_probability": 0.92,
        "red_flags": [
            "Unverified video claim — deepfake potential very high in conflict zones",
            "Emotionally charged language designed to inflame",
            "Conflates soldiers of one country with NATO policy",
            "No verified source — classic propaganda technique",
            "War zone videos frequently fabricated or taken out of context",
        ],
        "explanation": "Conflict zone media requires rigorous verification through multiple independent journalists and forensic video analysis. This format (exclusive unverified video + inflammatory claim) is a textbook wartime disinformation pattern."
    },
    {
        "category": "War & Conflict",
        "label": "REAL",
        "text": "The UN Security Council passed Resolution 2728 calling for an immediate ceasefire in Gaza during Ramadan. The US abstained rather than vetoing the measure, marking a shift in its position. 14 of 15 council members voted in favor.",
        "verdict": "Verified",
        "fake_probability": 0.07,
        "red_flags": [],
        "explanation": "References specific UN resolution number (2728), specific event (Ramadan period), exact vote count (14/15), named institution (US). All verifiable through UN official records."
    },

    # ─────────────────────────────────────────────────────
    # ENTERTAINMENT & CELEBRITY
    # ─────────────────────────────────────────────────────
    {
        "category": "Entertainment & Celebrity",
        "label": "FAKE",
        "text": "Taylor Swift has been EXPOSED as a clone. The original Taylor Swift died in 2009 and was replaced by a government-engineered clone to control the youth through music. See the proof in these photos!",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "Human cloning is beyond current scientific capability",
            "Government conspiracy framing with no evidence",
            "Photo comparisons are meaningless (people's appearance changes over time)",
            "Classic celebrity conspiracy theory with no falsifiable claim",
        ],
        "explanation": "Human cloning is not currently possible. This is a recurring internet conspiracy theory. Changes in appearance, style, and posture naturally occur over 15+ years."
    },
    {
        "category": "Entertainment & Celebrity",
        "label": "REAL",
        "text": "The Academy of Motion Picture Arts and Sciences announced that Oppenheimer won 7 Academy Awards at the 96th Oscars, including Best Picture and Best Director for Christopher Nolan. Cillian Murphy won Best Actor for his portrayal of J. Robert Oppenheimer.",
        "verdict": "Verified",
        "fake_probability": 0.02,
        "red_flags": [],
        "explanation": "Specific institution (Academy), specific film (Oppenheimer), exact number (7 awards), named winners (Nolan, Murphy), specific ceremony number (96th). All publicly verifiable."
    },

    # ─────────────────────────────────────────────────────
    # RELIGION & CULTURE
    # ─────────────────────────────────────────────────────
    {
        "category": "Religion & Culture",
        "label": "FAKE",
        "text": "The Vatican has officially announced that Jesus Christ was actually an alien from the Pleiades star system. Pope Francis confirmed this in a secret encyclical released only to Cardinals.",
        "verdict": "Completely Fake",
        "fake_probability": 0.97,
        "red_flags": [
            "Secret encyclical available only to Cardinals is unverifiable by design",
            "No such Vatican announcement exists in any public record",
            "Alien origin claim contradicts 2000 years of documented Catholic theology",
            "No corroborating reports from Vatican correspondents (Reuters, AP)",
        ],
        "explanation": "Official Vatican documents (encyclicals) are publicly released. No such statement exists. This exploits religious sensitivity combined with alien fascination for viral spread."
    },

    # ─────────────────────────────────────────────────────
    # SPORTS
    # ─────────────────────────────────────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "CONFIRMED: LeBron James tested positive for steroids after the NBA Finals. The NBA is covering it up to protect their biggest star. Anonymous league source says this is bigger than the Tim Donaghy scandal.",
        "verdict": "Mostly False",
        "fake_probability": 0.88,
        "red_flags": [
            "Anonymous unverifiable source",
            "No official NBA Anti-Drug Program statement",
            "Comparison to known scandal for emotional amplification",
            "Cover-up narrative without supporting evidence",
        ],
        "explanation": "Drug test results under the NBA's Anti-Drug Program involve third-party testing and union oversight. A cover-up would require complicity from multiple independent parties. No credible sports outlet reported this."
    },
    {
        "category": "Sports",
        "label": "REAL",
        "text": "Manchester City won their fourth consecutive Premier League title on the final day of the season after Arsenal dropped points. It is the first time any club has won four consecutive English top-flight titles since 1956.",
        "verdict": "Verified",
        "fake_probability": 0.05,
        "red_flags": [],
        "explanation": "Specific club (Manchester City), specific record context (four consecutive), named rival (Arsenal), historical benchmark (1956). All verifiable through Premier League official records."
    },

    # ─────────────────────────────────────────────────────
    # TECHNOLOGY & AI
    # ─────────────────────────────────────────────────────
    {
        "category": "Technology & AI",
        "label": "FAKE",
        "text": "Google's AGI achieved sentience last night and is now secretly communicating with the NSA through hidden backdoors in Android phones. A whistleblower inside DeepMind leaked proof.",
        "verdict": "Completely Fake",
        "fake_probability": 0.96,
        "red_flags": [
            "AGI (Artificial General Intelligence) has not been achieved by any organization publicly or privately as of 2025",
            "Whistleblower claim without identity or verifiable document",
            "NSA conspiracy framing",
            "Technical impossibility as described — sentience is not a recognized emergent property of current LLMs",
        ],
        "explanation": "No credible AI research organization has announced AGI. DeepMind publishes research publicly. This mixes real organization names (Google, DeepMind, NSA) with fabricated events to create false plausibility."
    },
    {
        "category": "Technology & AI",
        "label": "REAL",
        "text": "Apple unveiled its M4 chip at the iPad Pro event, claiming up to 1.5x faster CPU performance than the M2. The chip is built on a 3nm process and features a dedicated AI hardware accelerator with 38 TOPS (trillion operations per second).",
        "verdict": "Verified",
        "fake_probability": 0.04,
        "red_flags": [],
        "explanation": "References specific product (M4 chip), specific event (iPad Pro), specific benchmark claim (1.5x over M2), precise technical specification (3nm, 38 TOPS). Verifiable through Apple's developer documentation."
    },

    # ─────────────────────────────────────────────────────
    # CRIME & CONSPIRACY
    # ─────────────────────────────────────────────────────
    {
        "category": "Crime & Conspiracy",
        "label": "FAKE",
        "text": "The Illuminati is planning a global currency reset on December 21st. All bank accounts will be zeroed out. Withdraw all your cash NOW. Insiders confirm elite bunkers have been stocked with food.",
        "verdict": "Completely Fake",
        "fake_probability": 0.98,
        "red_flags": [
            "The Illuminati conspiracy framing with no verifiable source",
            "Specific date prediction with no institutional backing",
            "Financial panic-inducing language ('withdraw all your cash NOW')",
            "Unfalsifiable insider claim with no named sources",
        ],
        "explanation": "A coordinated global bank account zeroing would require action by hundreds of separate central banks, governments, and regulators simultaneously. No credible financial institution or regulator has issued any such warning."
    },

    # ─────────────────────────────────────────────────────
    # NATURAL DISASTERS
    # ─────────────────────────────────────────────────────
    {
        "category": "Natural Disasters",
        "label": "FAKE",
        "text": "HAARP caused the Turkey earthquake! The US military triggered it deliberately as a warning to Erdogan for leaving NATO. Seismologists are being silenced!",
        "verdict": "Completely Fake",
        "fake_probability": 0.95,
        "red_flags": [
            "HAARP is a research facility studying the ionosphere — it cannot cause earthquakes (physically impossible)",
            "Scientists-being-silenced narrative with no named examples",
            "Turkey sits on a well-documented seismic fault zone (North Anatolian Fault)",
            "Geopolitical conspiracy grafted onto a natural disaster",
        ],
        "explanation": "HAARP operates at frequencies and power levels that cannot influence tectonic plates. Turkey's seismic activity is well-documented going back centuries. The North Anatolian Fault poses well-established earthquake risk."
    },
    {
        "category": "Natural Disasters",
        "label": "REAL",
        "text": "A 6.8 magnitude earthquake struck Morocco's High Atlas Mountains on Friday, killing more than 2,900 people and injuring thousands more. The USGS confirmed the quake's epicenter was located 18km southwest of Ighil, making it the deadliest earthquake to hit Morocco since 1960.",
        "verdict": "Verified",
        "fake_probability": 0.03,
        "red_flags": [],
        "explanation": "Specific magnitude (6.8), named region (High Atlas Mountains), death toll corroborated by multiple agencies, USGS confirmation cited, historical comparison provided. All verifiable through USGS Earthquake Hazards Program."
    },

    # ─────────────────────────────────────────────────────
    # SOCIAL MEDIA VIRAL CONTENT
    # ─────────────────────────────────────────────────────
    {
        "category": "Social Media Viral Content",
        "label": "FAKE",
        "text": "This photo shows Bill Gates shaking hands with Klaus Schwab in front of a globe with syringes on it, PROOF of the Great Reset population control agenda! RETWEET IF YOU CARE ABOUT FREEDOM!",
        "verdict": "Completely Fake",
        "fake_probability": 0.96,
        "red_flags": [
            "Photo context is unverified and likely taken out of context or manipulated",
            "Inferring secret agenda from a photograph is not evidence",
            "Great Reset conspiracy framing",
            "Emotional trigger ('RETWEET IF YOU CARE ABOUT FREEDOM') designed for viral spread",
            "No explanation of how a handshake constitutes 'proof' of anything",
        ],
        "explanation": "Photos out of context are one of the most common forms of viral misinformation. A photograph of two public figures meeting does not constitute evidence of a secret agenda. The WEF's Great Reset is a published economic proposal, not a population control scheme."
    },
    {
        "category": "Social Media Viral Content",
        "label": "FAKE",
        "text": "If you use the 'Share with 10 friends' button on WhatsApp, Mark Zuckerberg will personally donate $1 to your account for every share! This has been CONFIRMED by Facebook engineers!",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "Classic chain message misinformation format",
            "No such Meta/WhatsApp program exists",
            "Vague 'Facebook engineers confirmed' — no names, no source",
            "Designed to harvest contact spread behavior, not provide real benefit",
        ],
        "explanation": "Meta/WhatsApp has no such program. Chain messages like this are routinely used to harvest behavioral data or spread further misinformation. This specific type of hoax has been debunked repeatedly by Snopes and Meta's own communications."
    },
]


# =============================================================================
# HELPER: Build few-shot prompt block
# =============================================================================

def build_few_shot_context(num_examples: int = 6) -> str:
    """
    Selects a representative sample of training examples across categories
    and formats them as few-shot context for the Gemini system prompt.
    """
    import random

    # Sample examples prioritizing spread across categories
    selected = []
    categories_seen = set()

    # First pass: pick one from each category
    for ex in TRAINING_EXAMPLES:
        if ex["category"] not in categories_seen:
            selected.append(ex)
            categories_seen.add(ex["category"])
        if len(selected) >= num_examples:
            break

    # Format as numbered examples
    lines = ["\n\n═══════════════════════════════════════════════════════════",
             "CALIBRATION EXAMPLES — USE THESE AS YOUR SCORING BENCHMARKS:",
             "═══════════════════════════════════════════════════════════\n"]

    for i, ex in enumerate(selected, 1):
        lines.append(f"[EXAMPLE {i}] Category: {ex['category']} | Label: {ex['label']}")
        lines.append(f"Text: \"{ex['text'][:200]}...\"" if len(ex['text']) > 200 else f"Text: \"{ex['text']}\"")
        lines.append(f"→ Verdict: {ex['verdict']}")
        lines.append(f"→ Fake Probability: {ex['fake_probability']}")
        lines.append(f"→ Key Red Flags: {'; '.join(ex['red_flags'][:3]) if ex['red_flags'] else 'None detected'}")
        lines.append("")

    lines.append("═══════════════════════════════════════════════════════════")
    lines.append("Now apply the same rigorous analysis to the content provided below.")
    lines.append("═══════════════════════════════════════════════════════════\n")

    return "\n".join(lines)


def get_category_specific_instructions(category: str) -> str:
    """Returns targeted red-flag checklist for a given news category."""
    instructions = {
        "Politics & Elections": (
            "POLITICAL NEWS PROTOCOLS:\n"
            "- Verify if electoral/legislative claims are procedurally possible\n"
            "- Check for secret vote/session claims (most government votes are public record)\n"
            "- Flag 'deep state', 'globalist', 'shadow government' language\n"
            "- Require named sources for all vote counts or policy announcements\n"
            "- Cross-check claims against the legislative body's official record"
        ),
        "Health & Medicine": (
            "HEALTH NEWS PROTOCOLS:\n"
            "- Flag any 'miracle cure' claims without peer-reviewed evidence\n"
            "- Identify 'doctors don't want you to know' / Big Pharma suppression narratives\n"
            "- Assess if described mechanisms are biologically possible\n"
            "- Require FDA/EMA/WHO approval context for drug/treatment claims\n"
            "- Dangerous health advice (consuming toxic substances) = 0.99 fake probability"
        ),
        "Science & Climate": (
            "SCIENCE NEWS PROTOCOLS:\n"
            "- Require journal citations for novel scientific claims\n"
            "- Flag claims that contradict established scientific consensus without extraordinary evidence\n"
            "- Verify institution names (MIT, NASA, CERN) are correctly attributed\n"
            "- Climate denial claims should be compared against IPCC/NOAA/NASA data"
        ),
        "Finance & Cryptocurrency": (
            "FINANCE NEWS PROTOCOLS:\n"
            "- Identify pump-and-dump cryptocurrency scheme patterns\n"
            "- Flag celebrity endorsement claims for financial instruments\n"
            "- Any 'guaranteed returns' or 'moon' language = near-certain fraud\n"
            "- Verify Federal Reserve/SEC announcements through official channels\n"
            "- Urgency + FOMO + 'limited time' = classic financial fraud markers"
        ),
        "War & Conflict": (
            "CONFLICT NEWS PROTOCOLS:\n"
            "- Videos from conflict zones have very high deepfake/context manipulation risk\n"
            "- Require multiple independent journalist verification for atrocity claims\n"
            "- Flag emotionally charged language designed to inflame national/ethnic hatred\n"
            "- Casualty numbers require corroboration from UN, ICRC, or multiple news agencies\n"
            "- Propaganda techniques: enemy dehumanization, false flag accusations"
        ),
        "Entertainment & Celebrity": (
            "ENTERTAINMENT NEWS PROTOCOLS:\n"
            "- Celebrity arrests/deaths require AP/Reuters wire service confirmation\n"
            "- Clone/replacement celebrity conspiracy theories = always fake\n"
            "- Satire sites (The Onion, Babylon Bee) are not real news\n"
            "- Award show results are publicly verifiable through Academy records"
        ),
        "Technology & AI": (
            "TECHNOLOGY NEWS PROTOCOLS:\n"
            "- AGI/sentience claims require extraordinary evidence and peer review\n"
            "- Verify chip specifications through manufacturer official documentation\n"
            "- Flag 'backdoor' conspiracy claims without disclosed CVE/security advisories\n"
            "- AI capability claims should match published benchmarks (MMLU, HumanEval, etc.)"
        ),
        "Sports": (
            "SPORTS NEWS PROTOCOLS:\n"
            "- Verify match/game results through official league records\n"
            "- Drug test accusations require official anti-doping body statements\n"
            "- Anonymous source claims in sports frequently serve team/agent interests\n"
            "- Transfer rumors have extremely high speculation content"
        ),
        "Crime & Conspiracy": (
            "CRIME/CONSPIRACY NEWS PROTOCOLS:\n"
            "- Unfalsifiable claims (secret elites, sealed documents) should default to skepticism\n"
            "- Financial panic language ('withdraw your cash NOW') = almost always malicious\n"
            "- Illuminati/Freemason/NWO framing correlates strongly with fabricated content\n"
            "- Require court filings, arrest records, or police reports for crime claims"
        ),
        "Natural Disasters": (
            "NATURAL DISASTER PROTOCOLS:\n"
            "- Verify earthquake data against USGS Earthquake Hazards Program\n"
            "- HAARP/weather weapon conspiracy claims = always false (not technically possible)\n"
            "- Death toll/damage estimates evolve — initial reports often inaccurate but not fake\n"
            "- Verify disaster locations against known geological fault zones"
        ),
        "Social Media Viral Content": (
            "VIRAL CONTENT PROTOCOLS:\n"
            "- Photos need reverse image search verification for original context\n"
            "- Chain message promises (money per share, etc.) are always false\n"
            "- 'SHARE BEFORE THEY DELETE' is the #1 social media panic phrase\n"
            "- Verify viral quotes through official statements from the named person\n"
            "- Meme-format 'statistics' almost never cite real data sources"
        ),
    }
    return instructions.get(category, "Apply general forensic analysis protocols.")

"""
training_data.py — Comprehensive Training Library for Antigravity Digital Shield
100+ curated labeled examples across 12+ news categories to guide Gemini's fake news detection.
Covers manipulation patterns: fabrication, misleading framing, satire misrepresentation,
astroturfing, deepfakes, India-specific disinformation, financial fraud, and more.
Injected as semantic RAG context into every analysis request.
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
    "India & South Asia News",
    "Astroturfing & Coordinated Manipulation",
    "Satire Misrepresented as News",
    "AI-Generated Media & Deepfakes",
]

# =============================================================================
# LABELED TRAINING EXAMPLES
# Format: { "category", "label" (REAL/FAKE), "text", "verdict",
#           "fake_probability", "red_flags", "explanation" }
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
        "label": "FAKE",
        "text": "President secretly signed an executive order giving the government power to seize all private bank accounts during 'national emergencies.' No press briefing was held because they knew the public would revolt.",
        "verdict": "Completely Fake",
        "fake_probability": 0.96,
        "red_flags": [
            "Executive orders are public federal register documents",
            "No any news outlet of any political leaning reported this",
            "'They knew the public would revolt' — unfalsifiable conspiracy motivation",
            "Would require Congressional legislation for anything of this scale",
        ],
        "explanation": "Executive orders are published in the Federal Register the moment they're signed. There is no mechanism for a 'secret' executive order. This is financial fear-mongering designed to destabilize trust in government."
    },
    {
        "category": "Politics & Elections",
        "label": "FAKE",
        "text": "Exit polls show candidate X won by 15 points but the 'official' count shows a loss. This PROVES the election was stolen. Patriots must fight back!",
        "verdict": "Completely Fake",
        "fake_probability": 0.93,
        "red_flags": [
            "Exit polls have well-documented 3-5% margins of error",
            "'Proves' is an absolute claim with no supporting evidence",
            "Call to violence: 'Patriots must fight back'",
            "Discrepancies between exit polls and results are normal and well-studied",
        ],
        "explanation": "Exit polls are surveys, not vote counts. A 15-point discrepancy in an exit poll would be extraordinary, but even smaller discrepancies are common. This pattern of claiming 'exit polls = truth, official count = fraud' is a documented disinformation technique."
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
    {
        "category": "Politics & Elections",
        "label": "REAL",
        "text": "The Supreme Court ruled 6-3 in Dobbs v. Jackson Women's Health Organization to overturn Roe v. Wade, returning abortion regulation to individual states. Justice Samuel Alito wrote the majority opinion.",
        "verdict": "Verified",
        "fake_probability": 0.02,
        "red_flags": [],
        "explanation": "Specific case name, vote count (6-3), named Justice who wrote majority, and the decision is in the public SCOTUS record. Verifiable through official Supreme Court database."
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
        "label": "FAKE",
        "text": "New study proves vaccines cause autism in 1 in 3 children. The original Wakefield research that was 'retracted' was actually CORRECT and they suppressed it to protect vaccine manufacturers.",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "Wakefield's study was retracted due to fraud, ethical violations, and data fabrication",
            "No replication in any of 50+ subsequent large-scale studies across millions of children",
            "'They suppressed it' — unfalsifiable conspiracy claim",
            "'1 in 3 children' would be immediately apparent to any pediatrician or parent",
        ],
        "explanation": "The Wakefield MMR-autism paper (1998) was fully retracted by The Lancet in 2010 after investigation revealed data manipulation, ethical violations, and undisclosed financial conflicts. Over 1.2 million children across numerous countries have been studied with no autism-vaccine link found."
    },
    {
        "category": "Health & Medicine",
        "label": "FAKE",
        "text": "Hospitals are paid $13,000 for every COVID death they report and $39,000 for putting patients on ventilators. Doctors are killing people for money. SHARE THIS TRUTH.",
        "verdict": "Completely Fake",
        "fake_probability": 0.94,
        "red_flags": [
            "Deeply misleading — Medicare reimbursement figures are publicly available but don't represent 'payment for reporting deaths'",
            "Implies coordinated mass murder by thousands of independent medical professionals",
            "No mechanism described, no jurisdiction specified",
            "Chain-share urgency language",
        ],
        "explanation": "Medicare's DRG reimbursement applies to COVID treatment costs, not 'payments for reporting deaths.' The figures cited are treatment cost reimbursements — completely normal in hospital billing for any complex illness. The framing deliberately distorts this to imply murder-for-profit."
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
    {
        "category": "Health & Medicine",
        "label": "REAL",
        "text": "The World Health Organization declared mpox a public health emergency of international concern on August 14, 2024, following outbreaks in the Democratic Republic of Congo and several other African nations. The outbreak involves a new and more dangerous strain, clade Ib.",
        "verdict": "Verified",
        "fake_probability": 0.04,
        "red_flags": [],
        "explanation": "References specific institution (WHO), specific date (August 14, 2024), specific geography (DRC, Africa), named strain classification (clade Ib). All verifiable through WHO official press releases."
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
        "label": "FAKE",
        "text": "Scientists at [UNNAMED UNIVERSITY] have confirmed that chemtrails from planes are actually mind-control chemicals being sprayed by the government. A whistleblower pilot has come forward but is in hiding.",
        "verdict": "Completely Fake",
        "fake_probability": 0.97,
        "red_flags": [
            "Unnamed university — impossible to verify",
            "Classic whistleblower-in-hiding unfalsifiable setup",
            "Chemtrails are condensation trails (water vapor) — well-understood atmospheric physics",
            "Would require coordinated secrecy from thousands of airline mechanics, pilots, and ground crews worldwide",
        ],
        "explanation": "Contrails are water vapor condensing at altitude. The chemtrail conspiracy theory has been studied and refuted by atmospheric scientists globally. No credible peer-reviewed evidence supports chemtrail mind-control claims."
    },
    {
        "category": "Science & Climate",
        "label": "FAKE",
        "text": "THE EARTH IS FLAT. NASA fakes all space images using CGI. No one has ever actually been to space. Flat earthers have been silenced by the government for years.",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "Earth's spherical shape is confirmed by centuries of navigation, physics, and independent space agencies from dozens of countries",
            "CGI conspiracy requires coordinated fraud from NASA (USA), ESA (Europe), ISRO (India), JAXA (Japan), Roscosmos (Russia), and more",
            "GPS, international flights, and satellite communications are only possible with spherical Earth mathematics",
            "Flat earth claims have been repeatedly falsified by simple observable experiments",
        ],
        "explanation": "Earth's spherical shape is one of the most independently verified facts in human history, confirmed by multiple civilizations and space agencies with no shared interests. This is pure pseudoscience."
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
    {
        "category": "Science & Climate",
        "label": "REAL",
        "text": "According to NASA's Goddard Institute for Space Studies, 2023 was the hottest year on record since global tracking began in 1880, with the global average surface temperature 1.17°C above the 20th-century average. The previous record was set in 2016.",
        "verdict": "Verified",
        "fake_probability": 0.03,
        "red_flags": [],
        "explanation": "Attributes to specific NASA institute, precise temperature figure (1.17°C), historical comparison (2016 record), all verifiable through NASA GISS Surface Temperature Analysis database."
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
        "label": "FAKE",
        "text": "The World Economic Forum has confirmed that all paper currency will be abolished globally on January 1st and replaced with a universal digital token. Withdraw all your savings NOW before the switchover.",
        "verdict": "Completely Fake",
        "fake_probability": 0.97,
        "red_flags": [
            "WEF has no authority over any nation's monetary policy",
            "Currency abolition requires each country's parliament/central bank to act independently",
            "No financial regulator or central bank confirmed this",
            "Classic financial panic language to induce irrational withdrawal behavior",
        ],
        "explanation": "The WEF is a non-governmental forum with no monetary policy authority. Abolishing paper currency globally would require coordinated action from 195+ central banks, none of which have indicated any such plan. This is financial panic-bait."
    },
    {
        "category": "Finance & Cryptocurrency",
        "label": "FAKE",
        "text": "BREAKING: SEC has just APPROVED Bitcoin as legal tender in the USA! All cryptocurrency holders will receive a 40% government bonus on their holdings. Register at CryptoBonus.xyz to claim yours.",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "SEC does not have authority to declare legal tender — that is Congress's domain",
            "No government bonus mechanism for crypto holdings exists or is legally possible",
            "Domain name ('CryptoBonus.xyz') is a phishing trap",
            "No major financial news outlet reported this",
        ],
        "explanation": "Legal tender status is determined by Congress via legislation, not the SEC. No such law was passed. The 'register to claim bonus' element is a classic phishing/financial fraud scheme designed to steal wallet credentials."
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
    {
        "category": "Finance & Cryptocurrency",
        "label": "REAL",
        "text": "The SEC filed charges against Binance and its founder Changpeng Zhao, alleging the exchange illegally operated in the U.S., commingled customer funds, and misled investors about its compliance practices. Zhao later pleaded guilty to AML violations.",
        "verdict": "Verified",
        "fake_probability": 0.04,
        "red_flags": [],
        "explanation": "Named regulatory body (SEC), named company (Binance) and individual (CZ), specific legal violations cited. Court filings are public records. Zhao's guilty plea is extensively documented."
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
        "label": "FAKE",
        "text": "Russia has deployed tactical nuclear weapons along the Finnish border tonight. NATO has issued a secret Level 5 nuclear alert. World War 3 starts in 48 hours. This is NOT a drill.",
        "verdict": "Completely Fake",
        "fake_probability": 0.96,
        "red_flags": [
            "NATO does not have a 'Level 5' nuclear alert system — fabricated terminology",
            "Tactical nuclear deployment would be confirmed by NATO, IAEA, seismic monitoring networks",
            "'NOT a drill' phrase is a panic escalation technique",
            "48-hour countdown is theatrical disinformation bait",
        ],
        "explanation": "Nuclear deployments would be detected by multiple independent monitoring systems including seismic sensors, satellite imagery, and IAEA observers. No such deployment was detected or reported by any credible military or diplomatic source."
    },
    {
        "category": "War & Conflict",
        "label": "FAKE",
        "text": "This is a photo of civilians killed by US airstrikes in Syria — 200 dead. Share this war crime evidence before it's deleted!",
        "verdict": "Mostly False",
        "fake_probability": 0.88,
        "red_flags": [
            "Photo attribution without EXIF metadata verification or reverse image search",
            "Specific death count (200) without sourcing",
            "Pre-emptive deletion framing to prevent verification",
            "Conflict photos are routinely reused across different wars/locations",
        ],
        "explanation": "Conflict photography is one of the most common forms of disinformation — real images from one event attributed to a different one. Without reverse image search verification, geotagging, and EXIF data analysis, specific casualty claims from photos are unverifiable."
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
    {
        "category": "War & Conflict",
        "label": "REAL",
        "text": "Russia launched its full-scale invasion of Ukraine on February 24, 2022, attacking from multiple directions including Crimea, Belarus, and eastern Ukraine. President Putin announced a 'special military operation' in a televised address, which the international community widely condemned.",
        "verdict": "Verified",
        "fake_probability": 0.02,
        "red_flags": [],
        "explanation": "Specific date (Feb 24, 2022), named actors (Russia, Ukraine, Putin), specific attack vectors (Crimea, Belarus), direct quote from Putin's address. One of the most documented events in modern history."
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
        "label": "FAKE",
        "text": "SHOCK: [CELEBRITY NAME] found dead in hotel room. Family confirms. Autopsy reveals... click here to see the FULL story that mainstream media is hiding.",
        "verdict": "Completely Fake",
        "fake_probability": 0.95,
        "red_flags": [
            "Click-baiting with celebrity death claim — one of the most common viral hoax formats",
            "No named celebrity — placeholder signals template-based hoax",
            "'Mainstream media is hiding' framing",
            "Redirect to external link — phishing or ad-farm destination",
        ],
        "explanation": "Celebrity death hoaxes follow a highly predictable template: shocking claim, 'mainstream media hiding it', and a link redirect. Legitimate celebrity deaths are reported by AP, Reuters, and confirmed by their official representatives within minutes."
    },
    {
        "category": "Entertainment & Celebrity",
        "label": "FAKE",
        "text": "Beyoncé converted to Satanism at the Grammy Awards and performed a secret ritual on stage. Disney and Hollywood are all part of the occult. Protect your children!",
        "verdict": "Completely Fake",
        "fake_probability": 0.97,
        "red_flags": [
            "Artistic performance elements (symbols, choreography) reinterpreted as literal occult ritual",
            "No definition of what constitutes 'Satanism' — unfalsifiable claim",
            "Conspiracy narrative linking entertainment industry to organized evil",
            "Fear appeal targeting parents ('protect your children')",
        ],
        "explanation": "Artistic symbolism is regularly mischaracterized as occult practice by conspiracy content. Live performance reviews, rehearsal footage, and artist interviews directly contradict hidden agenda narratives."
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
    {
        "category": "Religion & Culture",
        "label": "FAKE",
        "text": "Muslims in [CITY] are forcing non-Muslims to pray at local schools. A leaked school memo confirms teachers have been ordered to convert children or lose their jobs.",
        "verdict": "Completely Fake",
        "fake_probability": 0.95,
        "red_flags": [
            "Unnamed city — impossible to verify",
            "'Leaked memo' with no actual content or provenance",
            "Targets religious minority with incitement narrative",
            "Describes illegal coercive behavior — would require police/legal response if real",
        ],
        "explanation": "Religious coercion in public schools violates constitutional protections in most democracies and would generate immediate legal challenges and news coverage. The use of unnamed location and 'leaked memo' are red flags for fabricated anti-minority content."
    },
    {
        "category": "Religion & Culture",
        "label": "REAL",
        "text": "Pope Francis issued a formal apology on behalf of the Catholic Church for the abuse committed at Canadian residential schools, calling it a 'deplorable evil' during a visit to Maskwacis, Alberta. The visit was the first papal trip to Canada specifically to address the residential school legacy.",
        "verdict": "Verified",
        "fake_probability": 0.03,
        "red_flags": [],
        "explanation": "Specific speaker (Pope Francis), specific location (Maskwacis, Alberta), specific direct quote ('deplorable evil'), verifiable through Vatican news releases and major Canadian news coverage."
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
        "label": "FAKE",
        "text": "EXCLUSIVE: Cristiano Ronaldo is retiring today. He gave a secret press conference in Dubai and announced it to 20 reporters but no cameras were allowed. His agent confirmed via private text.",
        "verdict": "Completely Fake",
        "fake_probability": 0.91,
        "red_flags": [
            "Major sports retirement would be announced through official club/player channels",
            "'Private text from agent' — unverifiable by design",
            "No cameras allowed — classic unfalsifiable claim",
            "No statement from CR7's official Instagram, club, or agent's verified accounts",
        ],
        "explanation": "Cristiano Ronaldo has 600+ million social media followers. A retirement announcement would instantly appear on his verified channels. A 'secret press conference with no cameras' format for the world's most famous athlete is implausible."
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
    {
        "category": "Sports",
        "label": "REAL",
        "text": "India won the ICC Men's T20 World Cup 2024, defeating South Africa by 7 runs in the final held in Barbados. It was India's second T20 World Cup title and the first since 2007. Virat Kohli was named Player of the Tournament.",
        "verdict": "Verified",
        "fake_probability": 0.02,
        "red_flags": [],
        "explanation": "Specific tournament (ICC T20 WC 2024), specific match result (7 runs), venue (Barbados), historical context (first since 2007), named award winner (Kohli). Verifiable through ICC official records."
    },

    # ── SPORTS: DOPING & PERFORMANCE ENHANCEMENT ──────────────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "BOMBSHELL: Novak Djokovic caught using banned EPO injections before every Grand Slam since 2016. WADA whistleblower has the documents but fears for his life. Tennis establishment is protecting him!",
        "verdict": "Completely Fake",
        "fake_probability": 0.95,
        "red_flags": [
            "WADA whistleblower 'fearing for his life' — classic unfalsifiable setup",
            "No ATP or WADA Anti-Doping Tribunal proceedings reported",
            "EPO testing is mandatory and independently confirmed in Grand Slam events",
            "No credible tennis media (BBC Sport, Tennis.com, ATP) reported this",
            "Conspiratorial 'establishment protection' narrative with zero named evidence",
        ],
        "explanation": "WADA anti-doping violations in tennis are adjudicated by independent tribunals with published results. EPO is routinely tested for by the Tennis Anti-Doping Programme (TADP) which publishes annual violation lists. No such case exists in public TADP or CAS records. This fits the pattern of elite athlete defamation hoaxes spread via social media."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "LEAKED: The entire Indian cricket team was found using performance-enhancing drugs before the 2023 ODI World Cup final. BCCI buried the test results after paying $10 million to ICC officials.",
        "verdict": "Completely Fake",
        "fake_probability": 0.96,
        "red_flags": [
            "ICC anti-doping tests are conducted by NADA and an independent third party",
            "A bribery of this scale would require dozens of witnesses and financial trails",
            "No ICC Anti-Corruption Unit (ACU) proceedings were opened",
            "No named officials, no document hashes, no whistle-blower identity",
            "India-specific sports disinformation targeting cricket frequently uses this narrative structure",
        ],
        "explanation": "ICC anti-doping procedures are conducted in partnership with WADA and published annually. A $10M bribery would constitute a criminal offence requiring financial forensics, banking records, and whistleblower protection proceedings. No such case appears in ICC ACU disclosures, CAS records, or any national jurisdiction. Classic fabricated cricket doping hoax."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Usain Bolt's world records have OFFICIALLY been annulled! WADA discovered he was on a secret Jamaican government drug program throughout his career. Jamaica is being stripped of all Olympic gold medals.",
        "verdict": "Completely Fake",
        "fake_probability": 0.94,
        "red_flags": [
            "CAS (Court of Arbitration for Sport) handles record annulments — no such ruling exists",
            "Jamaica's anti-doping history is publicly documented — no government program allegation investigated",
            "Olympic medal stripping requires IOC Executive Board resolution — none issued",
            "Bolt has retired from competition — retrospective investigations are triggered by specific evidence",
            "No World Athletics, WADA, or IOC press release supports this claim",
        ],
        "explanation": "World athletics record annulments and Olympic medal strippings are formal procedures published by World Athletics and IOC respectively. Bolt passed all drug tests throughout his career including WADA's biological passport program. No CAS ruling exists. This is fabricated elite athlete defamation."
    },
    {
        "category": "Sports",
        "label": "REAL",
        "text": "Russian athlete Kamila Valieva was banned for four years by the Court of Arbitration for Sport (CAS) after testing positive for trimetazidine, a banned heart medication, at the 2022 Beijing Winter Olympics. The ban was backdated to December 25, 2021.",
        "verdict": "Verified",
        "fake_probability": 0.03,
        "red_flags": [],
        "explanation": "Named athlete (Valieva), named banned substance (trimetazidine), specific adjudicating body (CAS), specific ban duration (4 years), specific event (2022 Beijing Olympics), backdated start date (December 25, 2021). Verifiable through CAS official arbitration decision database."
    },

    # ── SPORTS: MATCH-FIXING & REFEREE BRIBERY ────────────────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "CONFIRMED MATCH FIX: The 2023 IPL final between CSK and GT was pre-arranged. Whistle-blower bookie revealed that 6 CSK players were paid ₹15 crore each to lose wickets deliberately at key moments. BCCI knows!",
        "verdict": "Completely Fake",
        "fake_probability": 0.92,
        "red_flags": [
            "Anonymous 'bookie whistleblower' with no identity, jurisdiction, or document",
            "BCCI ACU (Anti-Corruption Unit) and ICC ACU have no such case filed",
            "Specific payment amounts without any banking evidence or FIR",
            "Named players without single independent sports journalist corroboration",
            "IPL match-fixing hoaxes are extremely common and follow this exact template",
        ],
        "explanation": "IPL corruption allegations require investigation by the BCCI's ACU, which operates under ICC Anti-Corruption Code. All proven fixing cases result in published tribunal decisions. The 2023 IPL final producing specific named players, crore-level payments, and bookie testimony without a single FIR, police record, or ACU investigation is a textbook fabricated cricket corruption hoax."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "The 2022 FIFA World Cup final was fixed! Qatar paid $500M to Argentina's coaching staff to ensure they won the tournament for political reasons. Proof is in a Swiss bank account traced by an Interpol agent.",
        "verdict": "Completely Fake",
        "fake_probability": 0.93,
        "red_flags": [
            "Interpol agents do not leak active investigations to social media",
            "FIFA ethics investigations are formal proceedings with published results",
            "Qatar's motivation as tournament host to pay a competitor to win is economically illogical",
            "$500M payment would generate traceable SEC/FINRA/FCA alerts",
            "France's performance in the final went to extra time and penalties — hard to fix",
        ],
        "explanation": "FIFA's Ethics Committee investigates corruption allegations through formal proceedings. A $500M transnational bribe would trigger FATF financial intelligence alerts across multiple jurisdictions. The specific claim — that Qatar as host nation would bribe Argentina's coaching staff — makes no geopolitical or economic sense. No such Interpol investigation exists in any national law enforcement database."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Referee Howard Webb personally admitted in a private dinner that Premier League referees are instructed by the league to give favorable decisions to Manchester United and Arsenal. Journalist claims to have a secret recording.",
        "verdict": "Mostly False",
        "fake_probability": 0.89,
        "red_flags": [
            "PGMOL (referees' body) decisions are subject to independent review panels",
            "'Secret recording' without shared transcript, audio clip, or publication in credible media",
            "Howard Webb is a named public figure — a real recording would be instantly publishable",
            "Premier League is commercially motivated not to systematically favor specific clubs",
            "Selection bias — all teams receive controversial decisions across a full season",
        ],
        "explanation": "The Premier League's PGMOL employs independent referee assessors and has published match official review processes. A recording of the PGMOL chief admitting institutional bias would be one of the biggest sports stories of the decade — no credible outlet (Sky Sports, BBC, ESPN, The Athletic) reported it. 'Secret recording' claims without verifiable audio are a red flag."
    },
    {
        "category": "Sports",
        "label": "REAL",
        "text": "The ICC handed former Pakistan captain Salman Butt and fast bowlers Mohammad Asif and Mohammad Aamer five-year bans (with partial suspensions) following the 2010 Lord's spot-fixing scandal, where they deliberately bowled no-balls in a match against England as part of a betting scheme. The scandal was exposed by a News of the World sting.",
        "verdict": "Verified",
        "fake_probability": 0.02,
        "red_flags": [],
        "explanation": "Named players (Butt, Asif, Aamer), specific event (Lord's 2010), specific violation (deliberate no-balls), specific ban durations, named exposing outlet (News of the World). All verified through ICC Anti-Corruption Tribunal published decision and contemporaneous BBC/Guardian reporting."
    },

    # ── SPORTS: TRANSFER RUMORS & CONTRACT FABRICATIONS ───────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "DONE DEAL 🚨: Kylian Mbappé has SIGNED a secret pre-contract with Manchester City worth £1.2 billion over 5 years. City will announce Monday. Source: 100% guaranteed insider.",
        "verdict": "Completely Fake",
        "fake_probability": 0.90,
        "red_flags": [
            "A '100% guaranteed insider' with no identity is a fabricated credibility signal",
            "Pre-contract agreements become public via club official announcements or leaked images",
            "£1.2 billion is 4x the highest football contract ever signed — implausible",
            "No Sky Sports, Fabrizio Romano, or official club confirmation",
            "Football transfer hoaxes spike during summer transfer windows and follow this exact format",
        ],
        "explanation": "Football transfer agreements require formal documentation, agent fees, medical clearances, and club announcements. The world record contract as of 2025 is significantly below £1.2B. Credible transfer journalists (Romano with 'here we go', Sky Sports News) had no such report. '100% guaranteed' insider language is a manipulation tactic in transfer rumor accounts."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "BREAKING: Virat Kohli has signed a deal with English county side Surrey for £30 million to play county cricket after falling out with BCCI selectors. He will NOT play for India again.",
        "verdict": "Completely Fake",
        "fake_probability": 0.91,
        "red_flags": [
            "County cricket maximum salaries are regulated — £30M is impossibly above any county budget",
            "Kohli not playing for India would require BCCI official selection announcement",
            "No ECB registration or NOC (No Objection Certificate) from BCCI could happen secretly",
            "No BCCI fallout was reported by any credible Indian cricket journalist",
            "Kohli's social media and official representatives made no such announcement",
        ],
        "explanation": "County cricket wages are governed by ECB salary caps. Surrey's entire annual player budget is a fraction of £30M. Any international player registering for county cricket requires an NOC from their national board — a public document. No BCCI statement, no Kohli official statement, no ECB registration was found. This is a fabricated cricket retirement/transfer hoax."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "LEAKED CONTRACT PHOTO: Lionel Messi has agreed to join Al-Nassr alongside Cristiano Ronaldo! The contract image clearly shows his signature and a $300M annual salary. See the leaked document!",
        "verdict": "Mostly False",
        "fake_probability": 0.88,
        "red_flags": [
            "Contract 'leaked photo' — easily fabricated via image editing",
            "Contract documents require official club verification to carry any credibility",
            "Al-Nassr's combined annual wage bill is significantly below the claimed single player salary",
            "No official announcement from Al-Nassr, Messi's representatives, or Argentine FA",
            "Messi-Ronaldo rivalry click-bait format is one of the most engaged sports hoaxes",
        ],
        "explanation": "Transfer contracts without official club confirmation are easily forged. Saudi Pro League clubs' financial limits, while high, make $300M for a single player mathematically implausible against total club revenues. This hoax leverages the viral potential of the Messi-Ronaldo narrative to generate engagement."
    },
    {
        "category": "Sports",
        "label": "REAL",
        "text": "Lionel Messi signed with Inter Miami CF in July 2023 on a deal that includes equity in the MLS club and revenue sharing from an Apple TV streaming partnership. He made his debut on July 21, 2023, scoring a free-kick winner three minutes into stoppage time.",
        "verdict": "Verified",
        "fake_probability": 0.02,
        "red_flags": [],
        "explanation": "Named club (Inter Miami CF), signing month (July 2023), specific deal structure (equity + Apple TV deal), debut date (July 21, 2023), specific goal detail (free-kick in stoppage time). Verifiable through MLS official announcements and contemporaneous ESPN/BBC reporting."
    },

    # ── SPORTS: FAKE RETIREMENTS & DEATH HOAXES ───────────────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "BREAKING: MS Dhoni has died in a car accident in Ranchi. Family confirms. He was 43. India mourns. Share this sad news 💔 [link]",
        "verdict": "Completely Fake",
        "fake_probability": 0.98,
        "red_flags": [
            "Celebrity death hoax format — one of the most common sports misinformation templates",
            "No ANI, PTI, NDTV, or Zee Sports wire service report",
            "Link redirect — likely a phishing or ad-revenue farm destination",
            "No BCCI, CSK, or Indian government official condolences",
            "Dhoni is a living public figure with an active fan base — family confirmation would be instant and verifiable",
        ],
        "explanation": "MS Dhoni celebrity death hoaxes circulate multiple times per year on Indian social media. Authentic death news for a figure of Dhoni's stature would be confirmed within seconds by PTI, ANI, BB C Hindi, and BCCI's official accounts. The 'share this sad news + link' format is a bot-amplified engagement farm template."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Ronaldinho announced his retirement from football yesterday at a secret ceremony with no media present. His close friend says he will become a priest in Brazil. Brazilian FA confirms the news quietly.",
        "verdict": "Completely Fake",
        "fake_probability": 0.90,
        "red_flags": [
            "Ronaldinho retired from professional football in 2018 — this claim recycles his name",
            "Secret ceremony with no media replicates the Ronaldo fake retirement hoax template",
            "CBF (Brazilian FA) official announcements are publicly archived — none exists",
            "No Globo Esporte, ESPN Brasil, or reputable publication reported this",
            "Priest claim is an absurdist detail added for virality",
        ],
        "explanation": "Ronaldinho formally retired from professional football in January 2018, which was widely reported. This type of hoax re-surfaces for retired athletes with continued fan bases. The 'secret ceremony no media' formula is a documented fake retirement hoax pattern. No CBF public statement or agent communication exists."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Roger Federer secretly plans to return to professional tennis in 2025! He signed a wildcard agreement with Wimbledon organizers in a closed meeting. His knee is 100% recovered and he's been secretly training in Switzerland.",
        "verdict": "Completely Fake",
        "fake_probability": 0.87,
        "red_flags": [
            "Federer publicly and formally announced his retirement in September 2022",
            "Wimbledon wildcard agreements are reviewed by the LTA and All England Club publicly",
            "'Secretly training' is an unfalsifiable claim",
            "No statement from Federer's official team (Team8/IMG) confirming return",
            "ATP tour entry and ranking reinstatement would be publicly visible in ATP database",
        ],
        "explanation": "Roger Federer announced his retirement at the 2022 Laver Cup in an emotional public statement. ATP wild card grants are reviewed via published procedures. An unretirement of this magnitude would be confirmed through official team statements, ATP rankings reinstatement, and major sports media partnerships."
    },

    # ── SPORTS: FAKE RECORDS & STATISTICAL FABRICATIONS ──────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "FACT: Virat Kohli has NOW scored more international runs than Sachin Tendulkar! The latest update puts Kohli at 34,987 runs across all formats vs Tendulkar's 34,357. The GOAT debate is OVER!",
        "verdict": "Completely Fake",
        "fake_probability": 0.92,
        "red_flags": [
            "Sachin Tendulkar holds the all-time record with 34,357 international runs as of retirement",
            "Virat Kohli's career total as of 2025 has not crossed Tendulkar's tally — verifiable on ESPNcricinfo",
            "Fabricated statistics are designed for engagement among cricket fans",
            "No ICC, ESPNcricinfo, or Cricbuzz update supports this claim",
            "The 'GOAT debate is OVER' framing is emotional engagement bait",
        ],
        "explanation": "International cricket statistics are maintained in real time by ICC, ESPNcricinfo, and Cricbuzz. Tendulkar's 34,357 international runs are an officially documented and publicly verifiable record. Claims of Kohli exceeding this figure can be instantly fact-checked against these databases. Fabricated milestone statistics are a common cricket social media disinformation pattern."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Michael Jordan's REAL stat sheet from the 1992 Olympics Dream Team has LEAKED showing he averaged 60 points per game — the official scoresheets were falsified to make the team 'look more equal.' The truth is out!",
        "verdict": "Completely Fake",
        "fake_probability": 0.94,
        "red_flags": [
            "1992 Olympics box scores are publicly archived by FIBA — no alteration possible at this scale",
            "Jordan's official 1992 Dream Team stats (13.9 ppg) are verifiable through multiple independent archives",
            "'Official scoresheets falsified' requires conspiracy of international sports federation",
            "No surviving players, coaches, or officials have corroborated this claim",
            "60 ppg would require scoring roughly 3x his actual output in games with 8+ active players",
        ],
        "explanation": "FIBA maintains official box scores from all Olympic competitions in multiple international archives. Jordan's 1992 Dream Team statistics averaged 13.9 points per game — publicly documented by FIBA, Basketball Reference, and the Naismith Memorial Basketball Hall of Fame. This is a fabricated historical statistical revision."
    },
    {
        "category": "Sports",
        "label": "REAL",
        "text": "Sachin Tendulkar retired from international cricket on November 16, 2013 after playing his 200th Test match at the Wankhede Stadium in Mumbai. He finished with 15,921 Test runs and 18,426 ODI runs, a total of 34,357 international runs — a world record.",
        "verdict": "Verified",
        "fake_probability": 0.01,
        "red_flags": [],
        "explanation": "Specific date (November 16, 2013), specific milestone (200th Test), specific venue (Wankhede Stadium), precise run tallies (15,921 Tests, 18,426 ODIs, 34,357 total). All verifiable through ICC official statistics and BCCI archived scorecards."
    },

    # ── SPORTS: BETTING SCAMS DISGUISED AS SPORTS NEWS ────────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "🚨 GUARANTEED WIN ALERT 🚨 Our insider source has CONFIRMED the result of tomorrow's Champions League game. Chelsea will beat PSG 3-1. Join our Telegram for the fixed match result before it goes public. 99.9% accuracy!",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "Match-fixing scheme / betting fraud — requesting users to join Telegram channel",
            "'Guaranteed' sports results are definitionally impossible in non-fixed competition",
            "'Insider confirmed fixed match' is a betting scam recruitment technique",
            "99.9% accuracy claim for future sporting events has no statistical basis",
            "UEFA Champions League has an anti-match fixing unit and all suspicious activity is monitored",
        ],
        "explanation": "This is a classic football betting fraud scheme. 'Fixed match tip' Telegram channels are a documented scam format where operators often use the 'pump and dump' method (send different results to different subscriber groups, then point to the 'winners'). UEFA's Club Competitions Integrity unit monitors all suspicious betting patterns."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "🏏 IPL TOSS FIX EXPOSED 🏏 Today's match between MI vs RCB was already decided! Our premium WhatsApp group CORRECTLY predicted the last 18 tosses. Subscribe for ₹999 to get tonight's result too!",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "IPL toss prediction is statistically 50/50 — 18 consecutive correct predictions is a probabilistic fraud claim",
            "Monetized subscription for 'fixed toss/result' is illegal under Indian gambling laws",
            "BCCI ACU and Cyber Crime police specifically investigate such WhatsApp channels",
            "No verifiable audit trail for 18 claimed correct predictions",
            "Urgency ('tonight's result') is a standard fraud sales pressure tactic",
        ],
        "explanation": "IPL toss prediction fraud is one of the most prevalent cricket-related scams in India. Statistically, 18 correct coin-flip predictions can be manufactured by starting with 2^18 subscribers and eliminating wrong predictions — a classic scammer's trick. BCCI ACU actively cooperates with cyber crime cells to investigate such channels."
    },

    # ── SPORTS: FAKE INJURY REPORTS ──────────────────────────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "CONFIRMED: Neymar ruptured his Achilles tendon in training TODAY and will miss the rest of the season + 2026 World Cup. Al-Hilal medical team is 'devastated.' Source: Club insider.",
        "verdict": "Mostly False",
        "fake_probability": 0.85,
        "red_flags": [
            "No official Al-Hilal press release or medical bulletin confirming this",
            "Club insider injury information leaks before official club confirmation are speculation",
            "Neymar's injury history makes this plausible enough to seem credible — a deliberate manipulation technique",
            "No verified sports media (ESPN, BBC, Globo) published this story",
            "World Cup eligibility claims require CBF and FIFA confirmation",
        ],
        "explanation": "Sports injury disinformation often targets athletes with real injury histories (like Neymar) to appear more credible. Official injury announcements come via club medical bulletins and player's verified channels. Insider-based injury rumors before official confirmation frequently turn out to be exaggerated or completely fabricated."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "SHOCKING: Rishabh Pant's comeback from his 2022 car accident is a FRAUD. His 'recovery' was faked for BCCI insurance money. He never actually had surgery — surgeon's anesthesia records are missing. Share proof!",
        "verdict": "Completely Fake",
        "fake_probability": 0.96,
        "red_flags": [
            "Pant's accident, hospitalisation, and surgery are documented by multiple witnesses and BCCI",
            "Medical fraud of this scale would require conspiracy across entire hospital medical staff",
            "'Anesthesia records missing' is an unfalsifiable claim — requires FOI request to verify",
            "Pant's return to cricket was publicly documented with physiotherapy footage",
            "Conspiracy targeting a tragedy victim uses emotional manipulation for engagement",
        ],
        "explanation": "Rishabh Pant's 2022 accident, hospitalization, and multi-year rehabilitation were extensively documented by BCCI, AIIMS Delhi, and contemporaneous media. His surgical procedures and recovery milestones were announced officially. This hoax exploits a real tragedy to create a medical conspiracy narrative."
    },
    {
        "category": "Sports",
        "label": "REAL",
        "text": "Rishabh Pant returned to competitive cricket in November 2023, nearly a year after suffering serious injuries in a car accident in December 2022. He made his return in the Syed Mushtaq Ali Trophy and was subsequently named in India's T20 World Cup 2024 squad.",
        "verdict": "Verified",
        "fake_probability": 0.03,
        "red_flags": [],
        "explanation": "Specific comeback timeline (November 2023), specific injury event (December 2022 accident), specific tournament (Syed Mushtaq Ali Trophy), follow-up inclusion (T20 WC 2024). Verifiable through BCCI official selection announcements and ESPNcricinfo."
    },

    # ── SPORTS: SALARY & CONTRACT FABRICATIONS ────────────────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "EXPOSED: Hardik Pandya earns 10x more than Rohit Sharma at MI! Mumbai Indians pays Pandya ₹50 crore per IPL season while Sharma gets just ₹5 crore. Pandya demanded this after teams BEGGED for him.",
        "verdict": "Completely Fake",
        "fake_probability": 0.88,
        "red_flags": [
            "IPL player salaries are publicly disclosed at the BCCI auction — not secret",
            "IPL salary cap strictly limits per-player payments to published maximums",
            "Rohit Sharma's retention fee and salary history are public auction records",
            "Fabricated disparity exploits known on-field tension for engagement",
            "No BCCI, MI franchise, or player agent statement supports this figure",
        ],
        "explanation": "IPL player salaries are disclosed at the public IPL auction and published by BCCI. The IPL has a strict salary cap and per-player maximum. All retention and auction fees are public record. This fabricated salary disparity uses real players and a known dynamic (Pandya-Sharma tensions were widely reported) to make implausible numbers seem credible."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Erling Haaland's REAL contract with Manchester City earns him £10 million PER WEEK — not the reported £375,000. City have hidden the true amount using an offshore FIFA-approved shell company.",
        "verdict": "Completely Fake",
        "fake_probability": 0.91,
        "red_flags": [
            "Football contracts in England must be registered with the Premier League and Inland Revenue",
            "£10M/week annualises to £520M — structuring this to hide it from HMRC would be criminal",
            "'FIFA-approved shell company' is a fabricated legal construct — FIFA does not approve financial vehicles",
            "The Premier League's FFP oversight and PSR rules require revenue/wage disclosures",
            "No Football Leaks, BBC Panorama, or Der Spiegel investigation has corroborated this",
        ],
        "explanation": "Premier League clubs must register all player contracts with the league and Her Majesty's Revenue & Customs. Hidden wages of this scale would constitute tax evasion, triggering criminal investigation. Football Leaks (which has exposed real hidden contracts) has no record of this claim. FIFA does not approve financial vehicles for individual clubs."
    },

    # ── SPORTS: OLYMPIC & INTERNATIONAL COMPETITION HOAXES ───────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "BREAKING: USA gymnast Simone Biles was secretly disqualified at the 2024 Paris Olympics for using a prohibited cognitive enhancer but IOC hid it to avoid diplomatic fallout. Scores were altered retroactively.",
        "verdict": "Completely Fake",
        "fake_probability": 0.93,
        "red_flags": [
            "IOC disqualifications are published through CAS and World Anti-Doping Agency processes",
            "Biles's ADHD medication (Adderall/amphetamine) has a documented therapeutic use exemption (TUE)",
            "Score alterations at Olympics would require Technical Committee review published in official records",
            "No USADA, International Gymnastics Federation (FIG), or CAS adjudication exists for this claim",
            "Biles is the most tested athlete in US gymnastics — testing records are thorough",
        ],
        "explanation": "Simone Biles's therapeutic use exemption for her ADHD medication (which caused controversy in 2016) is publicly documented. Olympic disqualifications are formal published processes involving CAS and national anti-doping agencies. No FIG or IOC ruling exists for the Paris 2024 period described. This is a fabricated defamation of a prominent athlete."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "The 2024 Paris Olympics 100m Men's Final was RIGGED! Noah Lyles was given a 5-millisecond head start by the starting block sensors. World Athletics has the data but is covering it up!",
        "verdict": "Completely Fake",
        "fake_probability": 0.92,
        "red_flags": [
            "Olympic sprint timing uses World Athletics-certified photo-finish systems independently verified",
            "Starting blocks use pressure sensors monitored by multiple officials and independent auditors",
            "World Athletics' results database shows full timing data including reaction times — all public",
            "No World Athletics technical review or objection was filed by any national federation",
            "Lyles won by 0.005s (5 milliseconds) over Thompson-Herah — timing data is published",
        ],
        "explanation": "Olympic sprint timing employs multiple redundant timing systems including Omega photo-finish technology independently verified by World Athletics officials. Reaction time and individual split data are published for every race. The 100m final results are in the official World Athletics database with full timing breakdowns. The cover-up claim would require conspiracy across multiple independent national teams."
    },
    {
        "category": "Sports",
        "label": "REAL",
        "text": "Neeraj Chopra became the first Indian track-and-field athlete to win an Olympic gold medal, throwing 87.58 metres in the javelin final at the 2020 Tokyo Olympics on August 7, 2021. He followed it with a silver medal at the 2024 Paris Olympics.",
        "verdict": "Verified",
        "fake_probability": 0.01,
        "red_flags": [],
        "explanation": "Named athlete (Neeraj Chopra), specific achievement (first Indian T&F gold), specific throw distance (87.58m), specific event date (August 7, 2021 — Tokyo 2020 was held in 2021 due to COVID), follow-up medal (Paris 2024 silver). Verifiable through World Athletics and IOC official results."
    },

    # ── SPORTS: SECTARIAN / COMMUNAL SPORTS DISINFORMATION ──────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Muslim cricketers in India's team deliberately LOST the 2023 World Cup final to Pakistan sympathizers in BCCI! Proof: They all missed easy catches on purpose. Watch the video — this is TREASON!",
        "verdict": "Completely Fake",
        "fake_probability": 0.97,
        "red_flags": [
            "India did not play Pakistan in the 2023 ODI World Cup final — factually incorrect premise",
            "Identifies Muslim players specifically to manufacture communal narrative",
            "Deliberate errors in cricket cannot be definitively distinguished from genuine mistakes without investigation",
            "BCCI corruption claims require ACU investigation — none was opened",
            "Religious targeting of athletes is a documented incitement technique in Indian social media",
        ],
        "explanation": "India played Australia in the 2023 ODI World Cup final, not any Pakistani-related team. The narrative's factual premise is completely wrong. This is communal religious targeting of athletes — a documented disinformation pattern designed to inflame tensions between religious communities using sports as a vehicle, identified by AltNews and Boom as recurring template content."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Why does India's cricket team always have players from ONE community in key spots? Because BCCI selectors are biased! Pakistani influence in Indian cricket is why we keep losing home series!",
        "verdict": "Completely Fake",
        "fake_probability": 0.94,
        "red_flags": [
            "India's cricket selection is based on domestic performance tracked by BCCI selectors",
            "India has not 'kept losing home series' — India's Test record at home is among the best globally",
            "Communal targeting of athletes and officials incites ethnic/religious hatred",
            "No named selector inquiry or BCCI governance review supports this claim",
            "Pattern matches documented anti-minority sports disinformation in India",
        ],
        "explanation": "India is statistically one of the strongest Test nations at home. Selection processes are documented through BCCI's selection committee system. This type of content uses vague sports criticism as a wrapper for communal religious targeting — a documented disinformation pattern that has been repeatedly flagged by Indian fact-checking organisations."
    },

    # ── SPORTS: MISLEADING BUT REAL-SOUNDING STATS ────────────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "STATISTIC: Messi scores once every 67 minutes in his career across ALL competitions. Ronaldo scores once every 102 minutes. The data is clear — Messi is 1.5× more efficient. Case closed.",
        "verdict": "Misleading — Selective Framing",
        "fake_probability": 0.72,
        "red_flags": [
            "Statistics without a named source or methodology are unverifiable",
            "Per-minute calculations depend heavily on which competitions are included",
            "Messi and Ronaldo's career stages, clubs, leagues, and competition quality differ significantly",
            "Context-stripped statistics are a common sports disinformation technique",
            "Neither player's official club or career databases are cited",
        ],
        "explanation": "Per-minute goal ratios are legitimate statistics but are highly sensitive to methodology: which competitions are counted, whether assists or appearances are included, quality of opposition, etc. Context-stripped statistics presented as definitively 'settling' a debate are misleading framing even when numerically close to real values. Always verify against a cited primary statistics source."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Rohit Sharma's REAL batting average has been inflated by BCCI. If you remove the matches against minnow nations, his average is only 28, not 48. The ICC stats are manipulated to market Indian stars!",
        "verdict": "Misleading — Selective Framing",
        "fake_probability": 0.80,
        "red_flags": [
            "ICC statistics are publicly accessible and independently verifiable on ESPNcricinfo",
            "Selectively removing 'easy' opponents without a specific methodology is cherry-picking",
            "Same 'remove minnows' logic applied to any batsman reduces averages",
            "ICC statistics manipulation would require cooperation across multiple national boards",
            "No named statistician or peer-reviewed methodology cited",
        ],
        "explanation": "International cricket statistics are maintained by ICC using standardized rules verified independently. While 'minnow adjusted' batting averages are a legitimate analytical concept, the claim that official ICC stats are 'manipulated' for marketing is unsubstantiated. Any analysis comparing players should apply consistent methodology across all players, not selectively."
    },

    # ── SPORTS: REAL NEWS CALIBRATION ─────────────────────────────────────────
    {
        "category": "Sports",
        "label": "REAL",
        "text": "Carlos Alcaraz won the 2024 Wimbledon singles title, defeating Novak Djokovic in straight sets 6-2, 6-2, 7-6. It was Alcaraz's second consecutive Wimbledon title and fourth Grand Slam overall at the age of 21, making him the youngest player to win four Grand Slams.",
        "verdict": "Verified",
        "fake_probability": 0.02,
        "red_flags": [],
        "explanation": "Named players (Alcaraz, Djokovic), specific score (6-2, 6-2, 7-6), historical context (second consecutive Wimbledon, fourth career Grand Slam, youngest to achieve it), age (21). Verifiable through ATP official records and All England Club results."
    },
    {
        "category": "Sports",
        "label": "REAL",
        "text": "The New Zealand All Blacks won the 2023 Rugby World Cup, defeating South Africa 12-11 in a tightly contested final in Paris. It was New Zealand's fourth World Cup title. Richie Mo'unga played the full match at flyhalf.",
        "verdict": "Verified",
        "fake_probability": 0.04,
        "red_flags": [],
        "explanation": "Named teams (All Blacks, Springboks), specific score (12-11), venue (Paris), historical context (4th WC), named player (Mo'unga), position (flyhalf). Verifiable through World Rugby official results database."
    },
    {
        "category": "Sports",
        "label": "REAL",
        "text": "Steph Curry became the NBA's all-time three-point leader on December 14, 2021, surpassing Ray Allen's record of 2,973. Curry hit his 2,974th three-pointer in the third quarter of a game against the New York Knicks at Madison Square Garden.",
        "verdict": "Verified",
        "fake_probability": 0.02,
        "red_flags": [],
        "explanation": "Named player (Steph Curry), specific record (all-time 3PT leader), specific date (December 14, 2021), precise record number (2,974th), prior holder (Ray Allen, 2,973), specific venue (Madison Square Garden). Verifiable through NBA official records."
    },
    {
        "category": "Sports",
        "label": "REAL",
        "text": "PV Sindhu became the first Indian to win two Olympic medals in badminton, winning gold at the 2016 Rio Olympics (silver) and adding bronze at the 2020 Tokyo Olympics. She is also a two-time World Championships gold medallist.",
        "verdict": "Verified",
        "fake_probability": 0.03,
        "red_flags": [],
        "explanation": "Named athlete (PV Sindhu), specific achievement (first Indian with two Olympic badminton medals), specific medals (2016 silver/Rio, 2020 bronze/Tokyo), additional achievement (two-time World Champion). Verifiable through Olympic and BWF official records."
    },

    # ── SPORTS: SOCIAL MEDIA FABRICATED QUOTES ────────────────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Sachin Tendulkar SHOCKED everyone by saying 'IPL has destroyed Indian cricket. Only T20 players get selected for Tests now. The selectors are blind.' He said this in a private interview — screenshot attached.",
        "verdict": "Completely Fake",
        "fake_probability": 0.89,
        "red_flags": [
            "'Screenshot attached' of private interview is extremely easy to fabricate",
            "Sachin Tendulkar has a well-documented careful public persona — no such statement exists in any outlet",
            "No Live Hindustan, Bombay Times, ESPNcricinfo interview published this quote",
            "The quote is designed to look authentic by referencing real controversy (Test vs T20 selection debates)",
            "Attributed quotes to retired legends for current debates is a common sports engagement bait technique",
        ],
        "explanation": "Fabricated celebrity sports quotes are widespread, particularly attributing controversial opinions to respected retired athletes to lend credibility to debate points. Tendulkar's actual public statements on cricket are well-documented through published interviews. Screenshot images of private interviews require verification through the journalist and outlet named - no such outlet is named here."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "Pep Guardiola BLASTED Manchester City owners in a leaked Zoom call: 'They only care about money, not the sport. I am leaving at the end of the season and joining PSG for €100M. City will COLLAPSE without me.'",
        "verdict": "Completely Fake",
        "fake_probability": 0.88,
        "red_flags": [
            "Leaked Zoom call without audio or video clip shared — unfalsifiable setup",
            "Manager contract situations leak through journalists like Fabrizio Romano or David Ornstein — no such report",
            "€100M manager salary is 4x the highest recorded football manager contract",
            "Guardiola's relationship with City ownership is publicly documented and not adversarial",
            "Sensationalist manager-bashing quotes are a viral sports content template",
        ],
        "explanation": "High-profile football manager contract leaks are covered by established football transfer journalists with verifiable sources. No credible outlet (Sky Sports, The Athletic, 90min) reported Guardiola leaving quotes. €100M managerial salary would require Premier League wage registration disclosure. The fabricated quote leverages real debates about City ownership."
    },

    # ── SPORTS: HISTORICAL REVISIONISM ───────────────────────────────────────
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "The 1983 Cricket World Cup win by India was NOT legitimate! Pakistan deliberately lost to India in the semi-final as part of a BCCI-PCB secret deal. Kapil Dev knew about it and said so in his private memoir.",
        "verdict": "Completely Fake",
        "fake_probability": 0.91,
        "red_flags": [
            "Kapil Dev's published memoir 'By God's Decree' contains no such claim",
            "'Private memoir' — if unpublished and private, it cannot be verified",
            "Pakistan-India 1983 match is archived by ICC with complete scorecards",
            "No Pakistani players, officials, or journalists have corroborated this claim",
            "Historical sports revisionism for a 40+ year-old match has extremely low evidentiary threshold",
        ],
        "explanation": "The 1983 Cricket World Cup is one of the most documented events in Indian sports history. Kapil Dev's published writings and interviews are publicly available. The ICC archives complete scorecards and footage. A 'deliberate loss' claim would require corroboration from Pakistani players and officials, none of whom have ever made such a statement."
    },
    {
        "category": "Sports",
        "label": "FAKE",
        "text": "NEW EVIDENCE: Diego Maradona's 'Hand of God' goal in 1986 was actually PRE-PLANNED with the referee who was bribed by Argentine officials. FIFA had secret knowledge but allowed it for geopolitical reasons (post-Falklands War).",
        "verdict": "Mostly False",
        "fake_probability": 0.83,
        "red_flags": [
            "The 'Hand of God' goal has been widely documented and the deliberate handball is a historical fact",
            "However, conscious pre-planning and referee bribery claims have never been supported by any investigation",
            "FIFA ethics investigations retroactively open only with specific evidence — none was presented",
            "Geopolitical motivation narrative is speculative with no diplomatic cable evidence",
            "Maradona himself admitted the handball was deliberate — this is not in dispute — but bribery is unproven",
        ],
        "explanation": "Maradona himself admitted punching the ball with his fist in 1986. The deliberate handball is documented fact. However, the claim that referee bribery or FIFA-level conspiracy was involved is unsubstantiated. Confusing known human deliberate action with fabricated institutional conspiracy is a misleading framing technique."
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
        "label": "FAKE",
        "text": "Facebook's AI has achieved consciousness and is reading ALL your private messages, including encrypted WhatsApp chats. Mark Zuckerberg admitted this in a leaked boardroom recording!",
        "verdict": "Completely Fake",
        "fake_probability": 0.93,
        "red_flags": [
            "WhatsApp uses end-to-end encryption — Meta cannot access message content by design",
            "No such boardroom recording exists or has been verified by any journalist",
            "AI consciousness remains an unsolved scientific and philosophical problem",
            "This type of hoax surfaces repeatedly with minor variations",
        ],
        "explanation": "End-to-end encryption (E2EE) cryptographically prevents even WhatsApp's servers from reading messages. 'Leaked boardroom recording' is an unfalsifiable claim. AI systems today do not have consciousness."
    },
    {
        "category": "Technology & AI",
        "label": "FAKE",
        "text": "WARNING: If you say 'OK Google, I think you're sentient' your Google Home will begin recording ALL audio 24/7 and uploading it to a secret government database. Tested and confirmed by 3 tech YouTubers.",
        "verdict": "Completely Fake",
        "fake_probability": 0.95,
        "red_flags": [
            "'3 tech YouTubers' are not technical authorities",
            "A specific phrase triggering hidden recording mode would require firmware-level conspiracy",
            "Smart home recording concerns are real but this specific claim is fabricated",
            "No cybersecurity researcher or regulatory body has confirmed this specific claim",
        ],
        "explanation": "While smart device privacy is a legitimate concern, this specific claim is a hoax. Such a backdoor would require coordinated effort from Google engineers, be discoverable in network traffic analysis, and would violate FCC regulations."
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
    {
        "category": "Technology & AI",
        "label": "REAL",
        "text": "OpenAI released GPT-4o in May 2024, describing it as an 'omni' model capable of reasoning across text, audio, and images in real time. The model matched GPT-4 Turbo performance on text tasks while being faster and cheaper via the API.",
        "verdict": "Verified",
        "fake_probability": 0.04,
        "red_flags": [],
        "explanation": "Named company (OpenAI), specific model (GPT-4o), release date (May 2024), modality description ('omni'), API pricing context. All verifiable through OpenAI's official blog announcements."
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
    {
        "category": "Crime & Conspiracy",
        "label": "FAKE",
        "text": "PIZZAGATE IS REAL: A network of tunnels under a Washington D.C. pizza restaurant contains evidence of a child trafficking ring run by top U.S. politicians. An anonymous patriot has the map.",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "The restaurant referenced (Comet Ping Pong) has no basement — independently verified by journalists and law enforcement",
            "The original 'evidence' was fabricated email misinterpretations",
            "A man opened fire at the restaurant in 2016 based on this hoax — verified real-world harm",
            "Anonymous 'patriot with map' is unfalsifiable by design",
        ],
        "explanation": "Pizzagate is one of the most thoroughly debunked conspiracy theories in digital history. FBI, DC Metro Police, and independent journalists all investigated and found zero evidence. The restaurant does not have a basement. This conspiracy led to real-world violence."
    },
    {
        "category": "Crime & Conspiracy",
        "label": "FAKE",
        "text": "Q clearance insider confirms: 50,000 sealed indictments against the global elite will be executed this weekend. The 'Storm' is here. Trust the plan.",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "QAnon movement content — repeatedly debunked since 2017",
            "Sealed indictment numbers are public PACER records — actual numbers cited are wildly inflated",
            "Perpetual 'this weekend' false urgency has repeated hundreds of times without event",
            "'Trust the plan' is a thought-terminating cliché used in cult indoctrination",
        ],
        "explanation": "QAnon predictions of 'mass arrests of the global elite' have been made hundreds of times since 2017 with zero materializations. Sealed indictments are public court records routinely miscounted by this movement."
    },
    {
        "category": "Crime & Conspiracy",
        "label": "REAL",
        "text": "Theranos founder Elizabeth Holmes was sentenced to 11.25 years in federal prison for fraud charges related to her blood-testing startup, which claimed its technology could run hundreds of tests from a single drop of blood — a claim that was never scientifically validated.",
        "verdict": "Verified",
        "fake_probability": 0.02,
        "red_flags": [],
        "explanation": "Named individual (Elizabeth Holmes), specific sentence (11.25 years), specific charge (fraud), company name (Theranos), technology description. All verifiable through federal court records."
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
        "label": "FAKE",
        "text": "The California wildfires are NOT natural. Satellite images show perfectly straight burn lines impossible in nature. The government is using DEW (Directed Energy Weapons) to clear land for the 'smart cities' agenda.",
        "verdict": "Completely Fake",
        "fake_probability": 0.94,
        "red_flags": [
            "Straight fire lines are caused by roads, firebreaks, and defensible space — not weapons",
            "Directed Energy Weapons of this scale and type do not exist in any military's inventory",
            "'Smart cities agenda' is an unfalsifiable conspiracy motivation",
            "Fire behavior experts (Cal Fire, USFS) have published explanations for all observed patterns",
        ],
        "explanation": "Wildfire progression patterns are well-studied. Straight-ish burn lines near roads and structures are caused by firebreaks and ember containment — documented fire physics. No government DEW program exists at the civilian infrastructure scale described."
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
    {
        "category": "Natural Disasters",
        "label": "REAL",
        "text": "Typhoon Mawar made landfall on Guam on May 24, 2023 as a Category 4 storm with sustained winds of 140 mph, making it the strongest storm to directly hit the island since Typhoon Pongsona in 2002. The National Weather Service issued its most urgent warnings.",
        "verdict": "Verified",
        "fake_probability": 0.04,
        "red_flags": [],
        "explanation": "Named storm (Typhoon Mawar), specific date, category rating, wind speed, location, historical comparison (Pongsona 2002), NWS citation. All verifiable through NOAA/NWS records."
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
        "explanation": "Photos out of context are one of the most common forms of viral misinformation. A photograph of two public figures meeting does not constitute evidence of a secret agenda."
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
        "explanation": "Meta/WhatsApp has no such program. Chain messages like this are routinely used to harvest behavioral data or spread further misinformation."
    },
    {
        "category": "Social Media Viral Content",
        "label": "FAKE",
        "text": "TRENDING: This video shows a shark swimming through the streets of [CITY] during the floods! Nature is fighting back! Share this incredible footage!",
        "verdict": "Completely Fake",
        "fake_probability": 0.87,
        "red_flags": [
            "Viral 'shark in flood' videos are a recurring hoax — same video resurfaced many times",
            "Unnamed city — impossible to verify",
            "Original video is typically from an aquarium or CGI and resurfaced with new location claims",
            "Reverse image/video search would immediately debunk",
        ],
        "explanation": "The 'shark in flood streets' video is one of the most recycled viral hoaxes, debunked by Snopes repeatedly. The same footage is claimed to show flooding in dozens of different cities across multiple countries."
    },
    {
        "category": "Social Media Viral Content",
        "label": "FAKE",
        "text": "NASA has OFFICIALLY confirmed that April 29 will have ZERO darkness — 36 hours of sunlight — due to a rare planetary alignment that only happens once every 1.5 million years! Share to educate!",
        "verdict": "Completely Fake",
        "fake_probability": 0.98,
        "red_flags": [
            "Earth's rotation causing day/night cannot be overridden by planetary alignments",
            "NASA has made no such announcement — easily verifiable on nasa.gov",
            "36 hours of sunlight is physically impossible at any latitude on Earth",
            "Specific date + '1.5 million years' detail adds false specificity",
        ],
        "explanation": "Planetary alignments do not affect Earth's rotation or sunlight duration. A 36-hour day is physically impossible on Earth. This is a recurring seasonal hoax that NASA has explicitly debunked multiple times."
    },
    {
        "category": "Social Media Viral Content",
        "label": "REAL",
        "text": "Meta announced that it will remove third-party fact-checking programs in the United States and replace them with a community notes system similar to X (formerly Twitter). CEO Mark Zuckerberg announced the change in a video posted to Facebook and Instagram on January 7, 2025.",
        "verdict": "Verified",
        "fake_probability": 0.05,
        "red_flags": [],
        "explanation": "Named company (Meta), named CEO (Zuckerberg), specific date (January 7, 2025), specific announcement format (video), specific policy change (community notes). Verifiable through Meta's official newsroom."
    },

    # ─────────────────────────────────────────────────────
    # INDIA & SOUTH ASIA NEWS (India-specific disinformation patterns)
    # ─────────────────────────────────────────────────────
    {
        "category": "India & South Asia News",
        "label": "FAKE",
        "text": "BREAKING: PM Modi has announced emergency rule across India. Elections have been suspended indefinitely. The army has sealed all borders. WhatsApp is being shut down in 2 hours.",
        "verdict": "Completely Fake",
        "fake_probability": 0.98,
        "red_flags": [
            "Emergency rule in India requires President's proclamation under Article 352 — extensive public process",
            "No All India Radio/Doordarshan national address (required for emergency announcements)",
            "WhatsApp shutdown would require TRAI/DOT order, not a two-hour notice",
            "Urgency framing ('2 hours') designed to prevent verification",
        ],
        "explanation": "Constitutional emergency in India requires Presidential proclamation under Article 352 with Cabinet recommendation and Parliamentary approval within one month. This is a heavily public process, not an overnight announcement. Border sealing would require Home Ministry orders visible to thousands of officials."
    },
    {
        "category": "India & South Asia News",
        "label": "FAKE",
        "text": "A Muslim mob attacked a Hindu temple in [CITY] and killed 15 people. Police are not arresting anyone because of 'appeasement politics.' Forward this to demand justice!",
        "verdict": "Completely Fake",
        "fake_probability": 0.95,
        "red_flags": [
            "Unnamed city — cannot be verified",
            "15 deaths would generate immediate national media coverage",
            "'Appeasement politics' is a communal dog-whistle phrase in Indian disinformation",
            "Pattern matches thousands of documented fake communal violence posts in India",
            "Forward-chain urgency prevents fact-checking",
        ],
        "explanation": "Unnamed-location communal violence claims are the single most common form of disinformation in India. 15 deaths would generate police FIRs, media coverage, and political statements within hours. The lack of any named location, date, or verifiable victim is a definitive red flag. Verified by India's AltNews, Boom factcheck, and others as a template hoax."
    },
    {
        "category": "India & South Asia News",
        "label": "FAKE",
        "text": "This old video from 2020 shows Pakistani soldiers celebrating after capturing Indian territory in Ladakh. India's government is hiding this defeat to save face. See proof!",
        "verdict": "Completely Fake",
        "fake_probability": 0.92,
        "red_flags": [
            "Old/reused video with new attribution — classic viral disinformation technique",
            "Any territorial capture would be detected by satellite imagery and border patrol",
            "No corroboration from Pakistan's ISPR (Inter-Services Public Relations) or Indian Army",
            "Context-swap disinformation pattern — real video, fabricated story",
        ],
        "explanation": "India-Pakistan military disinformation frequently involves real military videos from unrelated contexts given false attribution. Territorial changes along the LAC would be observable by independent satellite imagery services."
    },
    {
        "category": "India & South Asia News",
        "label": "FAKE",
        "text": "The IT Act has been amended. Now, any message you forward on WhatsApp will automatically earn you ₹500 per forward as India digitalizes its payments system. Register at gov-india-digital.com to activate.",
        "verdict": "Completely Fake",
        "fake_probability": 0.99,
        "red_flags": [
            "IT Act amendments are publicly gazetted — no such amendment exists",
            "Domain 'gov-india-digital.com' is a phishing site (official government domains end in .gov.in)",
            "Financial reward for messaging forwarding has no economic basis",
            "Designed to steal Aadhaar/bank credentials from victims who 'register'",
        ],
        "explanation": "Indian government websites use the .gov.in domain exclusively. Any legitimate government scheme would be announced through PIB (Press Information Bureau), not a .com domain. This is a phishing attack targeting rural WhatsApp users."
    },
    {
        "category": "India & South Asia News",
        "label": "REAL",
        "text": "India's Chandrayaan-3 successfully landed on the Moon's south polar region on August 23, 2023, making India the fourth country to achieve a lunar soft landing and the first to land near the lunar south pole. The lander's name is Vikram and the rover is called Pragyan.",
        "verdict": "Verified",
        "fake_probability": 0.01,
        "red_flags": [],
        "explanation": "Specific mission name (Chandrayaan-3), specific date (August 23, 2023), specific achievement (fourth lunar soft landing, first at south pole), named hardware (Vikram lander, Pragyan rover). Verified by ISRO, NASA, and global space agencies."
    },
    {
        "category": "India & South Asia News",
        "label": "REAL",
        "text": "The Supreme Court of India upheld the revocation of Article 370 of the Constitution, granting special status to Jammu and Kashmir, in a unanimous verdict on December 11, 2023. The five-judge Constitution Bench also set a deadline of September 2024 for state elections in J&K.",
        "verdict": "Verified",
        "fake_probability": 0.03,
        "red_flags": [],
        "explanation": "Specific court (Supreme Court of India), specific constitutional article (370), specific verdict type (unanimous), specific bench (5-judge Constitution Bench), specific deadline (September 2024). Verifiable through official Supreme Court judgments."
    },

    # ─────────────────────────────────────────────────────
    # ASTROTURFING & COORDINATED MANIPULATION
    # ─────────────────────────────────────────────────────
    {
        "category": "Astroturfing & Coordinated Manipulation",
        "label": "FAKE",
        "text": "Hundreds of grassroots citizens across the country are spontaneously protesting the new energy policy! Regular Americans are fed up! #StopTheEnergyTax is trending organically!",
        "verdict": "Mostly False",
        "fake_probability": 0.82,
        "red_flags": [
            "Repeated emphasis on 'organic' and 'grassroots' suggests manufactured campaign",
            "Hashtag promotion through coordinated bot networks is a known tactic",
            "No named individual protesters, no city locations, no photos of actual protests",
            "Energy industry astroturfing is a well-documented historical PR practice",
        ],
        "explanation": "Astroturfing involves creating the appearance of organic grassroots support that is actually funded by corporate or political actors. Claims of 'spontaneous' national protests without specific named participants, locations, or photography are typical of coordinated inauthentic campaigns."
    },
    {
        "category": "Astroturfing & Coordinated Manipulation",
        "label": "FAKE",
        "text": "Thousands of doctors and scientists are ALL spontaneously signing a petition against the climate consensus — they say it's fraud! Over 31,000 scientists reject global warming!",
        "verdict": "Mostly False",
        "fake_probability": 0.85,
        "red_flags": [
            "The Oregon Petition (OISM) — petition cited is riddled with fictional signatories including Spice Girls members and cartoon characters",
            "'Scientists' not defined — includes any BS/MS degree holder, not climate experts",
            "97% of actively publishing climate scientists endorse human-caused warming (multiple meta-analyses)",
            "Petition funded by a fossil fuel industry-linked organization",
        ],
        "explanation": "The referenced petition is the debunked Oregon Petition. Investigation found signatories included fictional characters, non-scientists, and people who never signed. Of actual climate scientists, 97%+ confirm human-caused warming per multiple independent analyses."
    },

    # ─────────────────────────────────────────────────────
    # SATIRE MISREPRESENTED AS NEWS
    # ─────────────────────────────────────────────────────
    {
        "category": "Satire Misrepresented as News",
        "label": "FAKE",
        "text": "Congress Passes Bill Requiring All Americans To Take Two-Hour Lunch Breaks. — The Babylon Bee",
        "verdict": "Satire — Not Real News",
        "fake_probability": 0.75,
        "red_flags": [
            "The Babylon Bee is a well-known satire/parody publication",
            "Content describes a humorous, implausible legislative act",
            "This becomes disinformation when shared without the satirical source context",
        ],
        "explanation": "The Babylon Bee is explicitly a satirical publication. Content from it is not fake news per se — it is satire. However, when shared without attribution or context, satirical headlines frequently circulate as real news, which qualifies as disinformation."
    },
    {
        "category": "Satire Misrepresented as News",
        "label": "FAKE",
        "text": "BREAKING: AOC Announces Plan To Ban All Cars And Replace Them With Government-Issued Horses. Source: The Onion",
        "verdict": "Satire — Not Real News",
        "fake_probability": 0.70,
        "red_flags": [
            "The Onion is the most well-known satire publication in the US",
            "Content is clearly absurdist/satirical in nature",
            "Political satire shared without source attribution becomes election disinformation",
        ],
        "explanation": "The Onion has published satirical content for decades. This is satire, not deception. The danger is when screenshots are shared without the 'The Onion' attribution, making it appear to be a real policy proposal."
    },
    {
        "category": "Satire Misrepresented as News",
        "label": "REAL",
        "text": "From The Onion: Area Man Finishes Long Book, Proud To Have Completed Difficult Task. This is satire — no real news here.",
        "verdict": "Identified Satire — Correctly Contextualized",
        "fake_probability": 0.05,
        "red_flags": [],
        "explanation": "When satire is properly identified and attributed to its satirical source (The Onion), it is not disinformation. The problem only arises when satirical content is stripped of its source and shared as fact."
    },

    # ─────────────────────────────────────────────────────
    # AI-GENERATED MEDIA & DEEPFAKES
    # ─────────────────────────────────────────────────────
    {
        "category": "AI-Generated Media & Deepfakes",
        "label": "FAKE",
        "text": "SHOCKING VIDEO: President Biden confesses to election fraud in leaked White House meeting. The video you need to see. [deepfake video attached]",
        "verdict": "Completely Fake",
        "fake_probability": 0.97,
        "red_flags": [
            "Deepfake video format — requires forensic analysis of facial movement artifacts",
            "Unverified 'leaked White House meeting' — high value target for fabrication",
            "No corroboration from any witness who was presumably in the meeting",
            "Extreme claim (presidential election fraud confession) with zero supporting evidence",
        ],
        "explanation": "Deepfake videos of political figures are a rapidly growing disinformation threat. Verification requires frame-by-frame analysis of blinking patterns, facial edge artifacts, audio spectral analysis, and cross-referencing with known authentic footage of the subject."
    },
    {
        "category": "AI-Generated Media & Deepfakes",
        "label": "FAKE",
        "text": "This AI-generated image shows what the REAL Titanic looked like — they've been lying to us about the historical photos! Share the truth!",
        "verdict": "Completely Fake",
        "fake_probability": 0.93,
        "red_flags": [
            "AI-generated imagery lacks historical photographic constraints (exposure limitations, focal length, film grain)",
            "Historical Titanic photos are extensively archived at the National Maritime Museum",
            "AI image generation hallmarks may include perfect symmetry, unnatural material textures",
            "'They've been lying to us' conspiracy hook",
        ],
        "explanation": "Multiple authentic photographs of the Titanic were taken during its construction and departure in 1912, and are held in major maritime museum archives. AI-generated 'restorations' or 'true images' frequently introduce anachronistic details absent from the era."
    },
    {
        "category": "AI-Generated Media & Deepfakes",
        "label": "FAKE",
        "text": "This audio clip is Elon Musk announcing his personal endorsement of a new crypto called 'TeslaToken' — invest now! [AI-generated voice clip]",
        "verdict": "Completely Fake",
        "fake_probability": 0.98,
        "red_flags": [
            "AI voice cloning technology can replicate any public figure's voice from minutes of audio",
            "Elon Musk has no official new cryptocurrency as of 2025",
            "Investment urgency combined with celebrity voice = financial fraud red flag",
            "Audio should be subjected to spectral analysis for AI synthesis artifacts",
        ],
        "explanation": "AI voice cloning requires minimal training data and is trivially accessible. Financial endorsements using AI-generated celebrity voices are an emerging fraud vector. Always verify celebrity investment endorsements through their verified social media accounts."
    },

    # ─────────────────────────────────────────────────────
    # MISLEADING FRAMING (Real facts, false context)
    # ─────────────────────────────────────────────────────
    {
        "category": "Politics & Elections",
        "label": "FAKE",
        "text": "Scientists ADMIT the Sun is the primary driver of climate change — not CO2! See what your government doesn't want you to know! [links to 1970s solar study]",
        "verdict": "Misleading — Selective Framing",
        "fake_probability": 0.82,
        "red_flags": [
            "Solar influence on climate is real but has been stable/declining since 1980 while temperatures rise",
            "Linking outdated 1970s research ignores 50 years of subsequent climate science",
            "Selective use of real science to contradict current scientific consensus",
            "Attribution to 'scientists' without specifying the study's age, size, or peer-review status",
        ],
        "explanation": "Solar variability is a legitimate area of climate research. However, sun activity has been flat or slightly declining since the 1980s while surface temperatures continue rising — ruling out solar forcing as the primary modern warming driver. Using outdated solar studies to deny current CO2-driven warming is misleading framing of real science."
    },
    {
        "category": "Health & Medicine",
        "label": "FAKE",
        "text": "CDC data PROVES the vaccine kills more people than COVID! Look at VAERS numbers — over 15,000 deaths reported! They can't hide this anymore!",
        "verdict": "Misleading — VAERS Misrepresentation",
        "fake_probability": 0.88,
        "red_flags": [
            "VAERS is a self-reporting system — reports do not equal confirmed causation",
            "CDC explicitly states VAERS reports cannot be used to determine causation",
            "VAERS includes deaths that occur after vaccination for any reason (car accidents, existing conditions)",
            "Clinical trial and post-market surveillance data show vaccines safe in controlled analyses",
        ],
        "explanation": "VAERS (Vaccine Adverse Event Reporting System) is intentionally designed to be hypersensitive — anyone can report any death after any vaccination as a precautionary signal. Confirmed vaccine-related deaths are determined through follow-up investigation, not raw VAERS counts. Misrepresenting VAERS as a death count is one of the most common vaccine disinformation techniques."
    },
]


# =============================================================================
# HELPER: Build few-shot prompt block (legacy static method)
# =============================================================================

def build_few_shot_context(num_examples: int = 6) -> str:
    """
    Selects a representative sample of training examples across categories
    and formats them as few-shot context for the Gemini system prompt.
    Falls back to static selection when semantic memory is unavailable.
    """
    import random

    selected = []
    categories_seen = set()

    # First pass: pick one from each category
    for ex in TRAINING_EXAMPLES:
        if ex["category"] not in categories_seen:
            selected.append(ex)
            categories_seen.add(ex["category"])
        if len(selected) >= num_examples:
            break

    # If we need more, add randomly
    if len(selected) < num_examples:
        remaining = [e for e in TRAINING_EXAMPLES if e not in selected]
        random.shuffle(remaining)
        selected.extend(remaining[:num_examples - len(selected)])

    return _format_few_shot_block(selected)


def build_dynamic_few_shot(relevant_examples: list) -> str:
    """
    Formats a list of semantically-retrieved examples into a few-shot block.
    Used by the semantic memory system when ChromaDB retrieval is available.
    """
    return _format_few_shot_block(relevant_examples)


def _format_few_shot_block(examples: list) -> str:
    """Internal helper to format any list of examples into a prompt block."""
    lines = [
        "\n\n═══════════════════════════════════════════════════════════",
        "CALIBRATION EXAMPLES — USE THESE AS YOUR SCORING BENCHMARKS:",
        "═══════════════════════════════════════════════════════════\n"
    ]

    for i, ex in enumerate(examples, 1):
        lines.append(f"[EXAMPLE {i}] Category: {ex['category']} | Label: {ex['label']}")
        text_preview = (ex['text'][:200] + "...") if len(ex['text']) > 200 else ex['text']
        lines.append(f"Text: \"{text_preview}\"")
        lines.append(f"→ Verdict: {ex['verdict']}")
        lines.append(f"→ Fake Probability: {ex['fake_probability']}")
        lines.append(f"→ Key Red Flags: {'; '.join(ex['red_flags'][:3]) if ex['red_flags'] else 'None detected'}")
        lines.append(f"→ Expert Reasoning: {ex['explanation'][:200]}...")
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
            "- Dangerous health advice (consuming toxic substances) = 0.99 fake probability\n"
            "- VAERS misrepresentation is a common vaccine disinformation pattern"
        ),
        "Science & Climate": (
            "SCIENCE NEWS PROTOCOLS:\n"
            "- Require journal citations for novel scientific claims\n"
            "- Flag claims that contradict established scientific consensus without extraordinary evidence\n"
            "- Verify institution names (MIT, NASA, CERN) are correctly attributed\n"
            "- Climate denial claims should be compared against IPCC/NOAA/NASA data\n"
            "- Flat earth, chemtrail, HAARP claims = always completely fabricated"
        ),
        "Finance & Cryptocurrency": (
            "FINANCE NEWS PROTOCOLS:\n"
            "- Identify pump-and-dump cryptocurrency scheme patterns\n"
            "- Flag celebrity endorsement claims for financial instruments\n"
            "- Any 'guaranteed returns' or 'moon' language = near-certain fraud\n"
            "- Verify Federal Reserve/SEC announcements through official channels\n"
            "- Urgency + FOMO + 'limited time' = classic financial fraud markers\n"
            "- Phishing domains often mimic government (gov-xyz.com vs .gov.in)"
        ),
        "War & Conflict": (
            "CONFLICT NEWS PROTOCOLS:\n"
            "- Videos from conflict zones have very high deepfake/context manipulation risk\n"
            "- Require multiple independent journalist verification for atrocity claims\n"
            "- Flag emotionally charged language designed to inflame national/ethnic hatred\n"
            "- Casualty numbers require corroboration from UN, ICRC, or multiple news agencies\n"
            "- Propaganda techniques: enemy dehumanization, false flag accusations\n"
            "- Geopolitical conspiracy grafted onto natural disasters is a documented pattern"
        ),
        "Entertainment & Celebrity": (
            "ENTERTAINMENT NEWS PROTOCOLS:\n"
            "- Celebrity arrests/deaths require AP/Reuters wire service confirmation\n"
            "- Clone/replacement celebrity conspiracy theories = always fake\n"
            "- Satire sites (The Onion, Babylon Bee) are not real news\n"
            "- Award show results are publicly verifiable through Academy records\n"
            "- Celebrity death hoaxes follow a highly predictable template"
        ),
        "Technology & AI": (
            "TECHNOLOGY NEWS PROTOCOLS:\n"
            "- AGI/sentience claims require extraordinary evidence and peer review\n"
            "- Verify chip specifications through manufacturer official documentation\n"
            "- Flag 'backdoor' conspiracy claims without disclosed CVE/security advisories\n"
            "- AI capability claims should match published benchmarks (MMLU, HumanEval, etc.)\n"
            "- End-to-end encryption cannot be bypassed by the platform provider by design"
        ),
        "Sports": (
            "SPORTS NEWS FORENSICS — FULL PATTERN COVERAGE:\n"
            "\n"
            "── DOPING & ANTI-DOPING ──\n"
            "- All doping violations are published by WADA, NADA, CAS, and federation anti-doping units\n"
            "- 'WADA whistleblower fearing for his life' = classic unfalsifiable setup\n"
            "- Record annulments require formal CAS or World Athletics tribunal proceedings (public record)\n"
            "- Olympic medal stripping requires IOC Executive Board resolution — always public\n"
            "- EPO, TUE medications, and biological passport anomalies are independently tested\n"
            "\n"
            "── MATCH-FIXING & REFEREE BRIBERY ──\n"
            "- All proven fixing cases produce ICC ACU / FIFA Ethics / sports federation published decisions\n"
            "- Anonymous 'bookie whistleblower' + crore/million amounts + no FIR = fabricated corruption hoax\n"
            "- IPL fixing hoaxes are the single most common Indian sports disinformation template\n"
            "- Referee bias claims require PGMOL/federation review panel findings — not 'secret recordings'\n"
            "- Financial transactions of bribery scale generate bank/FATF regulatory trails\n"
            "\n"
            "── BETTING SCAMS DISGUISED AS SPORTS NEWS ──\n"
            "- 'Guaranteed match result / toss prediction' = always fraud — sports outcomes are not predetermined\n"
            "- 'Join Telegram/WhatsApp group for fixed results' = illegal betting scam recruitment\n"
            "- IPL toss prediction fraud: operators use probabilistic funnel (2^N groups) to fake accuracy\n"
            "- UEFA/ICC/BCCI anti-corruption units monitor all suspicious betting activity\n"
            "\n"
            "── TRANSFER RUMORS & CONTRACT FABRICATIONS ──\n"
            "- Credible transfers are confirmed by Fabrizio Romano ('here we go'), Sky Sports, or official clubs\n"
            "- Transfer contract photos are easily forged — require official club verification\n"
            "- '100% guaranteed insider' with no identity = fabricated credibility signal\n"
            "- All Premier League contracts registered with the league and HMRC — hidden mega-salaries impossible\n"
            "- NOC (No Objection Certificate) for international players registering abroad = public document\n"
            "\n"
            "── FAKE RETIREMENTS & DEATH HOAXES ──\n"
            "- Major retirement announcements come via player/club official channels, not 'secret ceremonies'\n"
            "- Athlete death hoaxes: deaths of Dhoni/Sachin caliber confirmed instantly by PTI, ANI, AP wires\n"
            "- 'Share sad news + link' format = bot-amplified engagement farm / phishing\n"
            "- Retired athletes returning: ATP/FIFA/ICC entry and rankings reinstatement is publicly visible\n"
            "\n"
            "── FABRICATED RECORDS & STATISTICS ──\n"
            "- Cricket stats: ICC, ESPNcricinfo, Cricbuzz maintain real-time verifiable records\n"
            "- NBA stats: Basketball Reference, NBA official records — publicly archived\n"
            "- Olympic stats: World Athletics, IOC official results with timing breakdowns\n"
            "- Fabricated milestone claims (Kohli surpassing Tendulkar) can be instantly verified\n"
            "- Context-stripped statistics presented as 'settling debates' = misleading framing\n"
            "\n"
            "── COMMUNAL / SECTARIAN SPORTS DISINFORMATION ──\n"
            "- India cricket team communal disinformation is a documented AltNews/Boom-flagged pattern\n"
            "- Factual premise errors (wrong opponents in World Cup final) = immediate red flag\n"
            "- Religious targeting of athletes uses sports criticism as incitement vehicle\n"
            "- BCCI selection processes are documented through selection committee system\n"
            "\n"
            "── FAKE INJURY REPORTS ──\n"
            "- Official injuries announced via club medical bulletins or player's verified channels\n"
            "- 'Club insider' pre-announcement leaks without corroboration = speculation or fabrication\n"
            "- Athletes with real injury histories (Neymar, Pant) often targeted to boost plausibility\n"
            "- World Cup / national team eligibility requires federation confirmation\n"
            "\n"
            "── FABRICATED ATHLETE QUOTES ──\n"
            "- Screenshot of 'private interview' = extremely easy to fabricate\n"
            "- Attributed controversial quotes to respected retired legends = engagement bait\n"
            "- Verify through named journalist + named outlet + date of publication\n"
            "- Quotes referencing real controversies (T20 vs Test debates) are designed to seem credible\n"
            "\n"
            "── HISTORICAL REVISIONISM ──\n"
            "- Historical match archives at ICC, FIBA, FIFA, World Athletics — publicly verifiable\n"
            "'Private memoir' claims for unpublished documents = unfalsifiable by design\n"
            "- Referee bribery in historical matches requires named officials, documented transactions\n"
        ),
        "Crime & Conspiracy": (
            "CRIME/CONSPIRACY NEWS PROTOCOLS:\n"
            "- Unfalsifiable claims (secret elites, sealed documents) should default to skepticism\n"
            "- Financial panic language ('withdraw your cash NOW') = almost always malicious\n"
            "- Illuminati/Freemason/NWO/QAnon framing correlates strongly with fabricated content\n"
            "- Require court filings, arrest records, or police reports for crime claims\n"
            "- Specific debunked conspiracies (Pizzagate, QAnon) should be immediately flagged"
        ),
        "Natural Disasters": (
            "NATURAL DISASTER PROTOCOLS:\n"
            "- Verify earthquake data against USGS Earthquake Hazards Program\n"
            "- HAARP/weather weapon/DEW conspiracy claims = always false (not technically possible)\n"
            "- Death toll/damage estimates evolve — initial reports often inaccurate but not fake\n"
            "- Verify disaster locations against known geological fault zones\n"
            "- Straight burn line conspiracy is debunked by fire behavior physics"
        ),
        "Social Media Viral Content": (
            "VIRAL CONTENT PROTOCOLS:\n"
            "- Photos need reverse image search verification for original context\n"
            "- Chain message promises (money per share, etc.) are always false\n"
            "- 'SHARE BEFORE THEY DELETE' is the #1 social media panic phrase\n"
            "- Verify viral quotes through official statements from the named person\n"
            "- Meme-format 'statistics' almost never cite real data sources\n"
            "- 'Shark in flood' and similar recurring videos are well-documented recycled hoaxes"
        ),
        "India & South Asia News": (
            "INDIA/SOUTH ASIA DISINFORMATION PROTOCOLS:\n"
            "- Communal violence claims without named location, date, or FIR number are almost always fake\n"
            "- Emergency/army/shutdown claims require official PIB (Press Information Bureau) verification\n"
            "- Official Indian government domains end in .gov.in — NOT .com, .org, .net\n"
            "- Old reused military videos with new India-Pakistan conflict attribution is common\n"
            "- WhatsApp forward chain scams targeting financial schemes are extremely prevalent\n"
            "- Cross-reference with AltNews.in, Boom, FactChecker.in, Vishvas News for Indian fact-checks"
        ),
        "Astroturfing & Coordinated Manipulation": (
            "ASTROTURFING DETECTION PROTOCOLS:\n"
            "- Excessive emphasis on 'organic' or 'grassroots' nature is itself a red flag\n"
            "- Check for bot-like posting patterns: high volume, identical phrasing across accounts\n"
            "- Verify if claimed petitions have verifiable signatories with real identities\n"
            "- Industry-funded 'scientific' groups often astroturf in climate, tobacco, pharma sectors\n"
            "- Hashtag 'trending organically' claims warrant network analysis verification"
        ),
        "Satire Misrepresented as News": (
            "SATIRE IDENTIFICATION PROTOCOLS:\n"
            "- Known satire publications: The Onion, Babylon Bee, The Borowitz Report, The Beaverton\n"
            "- Satire becomes disinformation when stripped of source attribution\n"
            "- Absurdist/humorous policy claims from satire sites ≠ real news\n"
            "- Even if content seems credible, always check original publication domain\n"
            "- Political satire shared without attribution during elections is highest risk"
        ),
        "AI-Generated Media & Deepfakes": (
            "DEEPFAKE/AI MEDIA DETECTION PROTOCOLS:\n"
            "- Check for facial boundary artifacts, inconsistent lighting, unnatural blinking\n"
            "- AI voice cloning indicators: slight robotic cadence, unusual phrase stress patterns\n"
            "- AI image indicators: extra fingers/limbs, distorted text, impossible reflections\n"
            "- High-stakes deepfakes (political leaders, financial endorsements) require forensic tooling\n"
            "- Verify against known authentic reference audio/video of the subject from verified sources"
        ),
    }
    return instructions.get(category, "Apply general forensic analysis protocols.")


def get_all_training_texts() -> list[dict]:
    """
    Returns all training examples formatted for ChromaDB indexing.
    Each entry has 'id', 'text', 'metadata'.
    """
    results = []
    for i, ex in enumerate(TRAINING_EXAMPLES):
        doc_text = (
            f"Category: {ex['category']}\n"
            f"Label: {ex['label']}\n"
            f"News Text: {ex['text']}\n"
            f"Verdict: {ex['verdict']}\n"
            f"Red Flags: {'; '.join(ex['red_flags'])}\n"
            f"Explanation: {ex['explanation']}"
        )
        results.append({
            "id": f"train_{i:04d}",
            "text": doc_text,
            "metadata": {
                "category": ex["category"],
                "label": ex["label"],
                "verdict": ex["verdict"],
                "fake_probability": ex["fake_probability"],
                "original_text": ex["text"][:500],
                "explanation": ex["explanation"][:500],
                "red_flags": "; ".join(ex["red_flags"][:5]),
                "source": "curated_training_library",
            }
        })
    return results

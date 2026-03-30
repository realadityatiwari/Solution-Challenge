import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { fileURLToPath } from "url";

// Get __dirname dynamically in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Look for .env in the parent directory (root directory)
const envPath = path.resolve(__dirname, "../.env");

console.log("ENV PATH:", envPath);
console.log("Exists:", fs.existsSync(envPath));

if (!fs.existsSync(envPath)) {
    console.error("ERROR: Could not find .env file. Please ensure it exists in the root directory.");
    process.exit(1);
}

// Load environment variables using dotenv
dotenv.config({ path: envPath });

const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
    console.error("ERROR: GEMINI_API_KEY is missing from the .env file.");
    process.exit(1);
}

// Initialize Gemini Generative AI
const genAI = new GoogleGenerativeAI(apiKey);
const model = genAI.getGenerativeModel({ model: "gemini-pro" });

/**
 * Thoroughly detect fake news using the Gemini API.
 * @param {string} newsContent The text to analyze for fake news characteristics.
 */
async function detectFakeNewsThoroughly(newsContent) {
    try {
        console.log("Listing available models...");
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`);
        const data = await response.json();
        const models = data.models.map(m => m.name);
        console.log("AVAILABLE MODELS:", models);
        
        let targetModel = "models/gemini-1.5-flash";
        if (models.includes("models/gemini-2.5-flash")) targetModel = "models/gemini-2.5-flash";
        else if (models.includes("models/gemini-1.5-pro")) targetModel = "models/gemini-1.5-pro";
        else targetModel = models.find(m => m.includes("gemini")) || targetModel;
        
        console.log(`Using model: ${targetModel}`);
        
        const dynamicModel = genAI.getGenerativeModel({ model: targetModel.replace("models/", "") });

        const systemPrompt = `You are a highly advanced AI system designed for extreme rigor in detecting fake news, misinformation, disinformation, and propaganda.
Your objective is to thoroughly analyze the provided text and determine its authenticity as factual news.

Please provide a detailed report with the following structure:
1. **Authenticity Verdict:** (A quick single-word/phrase summary).
2. **Confidence Score:** (0-100%).
3. **Key Claims Analysis:** (Break down the major claims).
4. **Red Flags:** (Identify sensationalism, etc).
5. **Contextual Gaps:** (What is missing).

Analyze this news content:
"${newsContent}"
`;

        console.log("Analyzing the news snippet for authenticity. Please wait...\n");
        const result = await dynamicModel.generateContent(systemPrompt);
        const genResponse = await result.response;
        console.log("=== FAKE NEWS DETECTION REPORT ===");
        console.log(genResponse.text());
        console.log("==================================");
    } catch (err) {
        fs.writeFileSync("error.json", JSON.stringify(err, Object.getOwnPropertyNames(err), 2));
        console.error("Generative AI Error. Checked error.json for details.");
    }
}

// Sample News snippet
const sampleNews = "ALERT: Scientists just discovered that breathing pure oxygen reduces lifespan by exactly 25.5 years due to extremely rapid cellular oxidation! The government has been hiding this and pumping extra nitrogen into the air to save us.";

detectFakeNewsThoroughly(sampleNews);
require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const multer = require('multer');
const crypto = require('crypto');
const fs = require('fs');
const { imageHash } = require('image-hash');
const cors = require('cors');
const { GoogleGenAI } = require('@google/genai');

const Asset = require('./models/Asset');

const app = express();
app.use(cors());
app.use(express.json());

let aiClient = null;
try {
  if (process.env.GOOGLE_API_KEY) {
      aiClient = new GoogleGenAI({ apiKey: process.env.GOOGLE_API_KEY });
  }
} catch(e) {
  console.log("Could not initialize Google GenAI", e);
}

const getGeminiAnalysis = async (filePath, mimeType, fingerprintResult) => {
    if (!aiClient) return { error: "Google API Key Missing" };

    try {
        const fileBase64 = fs.readFileSync(filePath).toString('base64');
        const flag = fingerprintResult.match_found ? 'possible unauthorized reuse' : 'original upload';
        const sourceMeta = fingerprintResult.matched_asset ? fingerprintResult.matched_asset.source : 'unknown';

        const promptText = `Analyze this image. A mathematical fingerprinting system has flagged it as "${flag}".
Similarity Score: ${fingerprintResult.similarity_score}%
Matched Asset Source: ${sourceMeta}

Instructions:
1. Examine the image visually to detect the presence of any watermarks, logos, or alterations.
2. Combine this visual evidence with the mathematical similarity score to determine classification.
3. Respond ONLY in valid JSON matching this exact schema:
{
  "watermark_detected": boolean,
  "watermark_description": "string (or empty)",
  "ai_classification": "authentic | manipulated | fake | unauthorized_reuse",
  "reasoning": "Explain why based on fingerprint data and visual evidence.",
  "final_verdict": "A decisive, single-sentence final verdict string."
}`;

        const response = await aiClient.models.generateContent({
             model: 'gemini-1.5-flash',
             contents: [
                { inlineData: { data: fileBase64, mimeType } },
                promptText
             ],
             config: {
                 responseMimeType: 'application/json',
                 temperature: 0.2
             }
        });
        
        return JSON.parse(response.text);
    } catch(err) {
        console.error("Gemini AI error:", err);
        return { error: err.message };
    }
};

const upload = multer({ dest: 'uploads/' });

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/fingerprint_db')
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));

// Helper: Calculate SHA-256
const calculateSHA256 = (filePath) => {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(filePath);
    stream.on('data', data => hash.update(data));
    stream.on('end', () => resolve(hash.digest('hex')));
    stream.on('error', err => reject(err));
  });
};

// Helper: Calculate perceptual hash
const calculatePHash = (filePath) => {
  return new Promise((resolve, reject) => {
    // 16 creates a fairly dense hash string. 'true' forces binary output natively
    imageHash(filePath, 16, true, (error, data) => {
      if (error) reject(error);
      else resolve(data);
    });
  });
};

// Helper: Calculate Hamming distance
const calculateHammingDistance = (hash1, hash2) => {
    if (!hash1 || !hash2 || hash1.length !== hash2.length) return 999;
    
    let diff = 0;
    for (let i = 0; i < hash1.length; i++) {
        if (hash1[i] !== hash2[i]) diff++;
    }
    return diff;
};

// POST /upload - Store new asset
app.post('/upload', upload.single('file'), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file uploaded' });
  const source = req.body.source || 'unverified';

  try {
    const sha256_hash = await calculateSHA256(req.file.path);
    let perceptual_hash = null;

    if (req.file.mimetype.startsWith('image/')) {
        try {
            perceptual_hash = await calculatePHash(req.file.path);
        } catch(e) {
            console.error("pHash error:", e);
        }
    }

    const newAsset = new Asset({
      original_file_name: req.file.originalname,
      sha256_hash,
      perceptual_hash,
      source
    });

    await newAsset.save();

    res.json({
      message: 'File processed and saved successfully',
      asset: newAsset
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error processing file' });
  } finally {
    if (fs.existsSync(req.file.path)) fs.unlinkSync(req.file.path);
  }
});

// POST /check - Compare file against database
app.post('/check', upload.single('file'), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file uploaded' });

  try {
    const sha256_hash = await calculateSHA256(req.file.path);
    
    // Check for exact match via SHA-256
    const exactMatch = await Asset.findOne({ sha256_hash });
    if (exactMatch) {
      const checkResults = {
        match_found: true,
        similarity_score: 100,
        type: 'exact',
        matched_asset: exactMatch
      };
      const aiAnalysis = await getGeminiAnalysis(req.file.path, req.file.mimetype, checkResults);
      return res.json({
          fingerprint_result: checkResults,
          ai_analysis: aiAnalysis,
          final_verdict: aiAnalysis.final_verdict || "Exact Match Documented."
      });
    }

    // Do perceptual comparison if image
    let checkResults = {
        match_found: false,
        similarity_score: 0,
        type: 'new',
        matched_asset: null
    };

    if (req.file.mimetype.startsWith('image/')) {
        let incoming_phash = null;
        try {
            incoming_phash = await calculatePHash(req.file.path);
        } catch(e) {
            console.error("pHash check error:", e);
        }

        if (incoming_phash) {
            let bestMatch = null;
            let minDistance = 999;

            const cursor = Asset.find({ perceptual_hash: { $exists: true, $ne: null } }).cursor();
            
            for await (const asset of cursor) {
                const distance = calculateHammingDistance(incoming_phash, asset.perceptual_hash);
                if (distance < minDistance) {
                    minDistance = distance;
                    bestMatch = asset;
                }
                if (minDistance === 0) break;
            }

            if (bestMatch) {
                let classification = "new";
                if (minDistance <= 5) classification = "exact";
                else if (minDistance <= 15) classification = "modified";
                
                const similarity_score = Math.max(0, ((incoming_phash.length - minDistance) / incoming_phash.length) * 100);

                if (classification !== "new") {
                   checkResults = {
                       match_found: true,
                       similarity_score: similarity_score,
                       type: classification,
                       matched_asset: bestMatch
                   };
                }
            }
        }
    }

    const aiAnalysis = await getGeminiAnalysis(req.file.path, req.file.mimetype, checkResults);

    return res.json({
        fingerprint_result: checkResults,
        ai_analysis: aiAnalysis,
        final_verdict: aiAnalysis.final_verdict || "No definitive AI verdict."
    });
    
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error checking file' });
  } finally {
    if (fs.existsSync(req.file.path)) fs.unlinkSync(req.file.path);
  }
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Node.js Fingerprint Service running on port ${PORT}`);
});

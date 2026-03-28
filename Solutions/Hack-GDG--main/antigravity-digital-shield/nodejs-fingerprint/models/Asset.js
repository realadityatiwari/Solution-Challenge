const mongoose = require('mongoose');

const AssetSchema = new mongoose.Schema({
  original_file_name: { type: String, required: true },
  sha256_hash: { type: String, required: true, index: true },
  perceptual_hash: { type: String }, // Store as binary string from image-hash
  upload_timestamp: { type: Date, default: Date.now },
  source: { type: String, enum: ['official', 'unverified'], default: 'unverified' }
});

module.exports = mongoose.model('Asset', AssetSchema);

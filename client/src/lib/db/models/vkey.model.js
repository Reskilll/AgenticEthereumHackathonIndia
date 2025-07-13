import mongoose, { Schema } from "mongoose";

const VerificationKeySchema = new Schema({
  circuitName: { type: String, required: true, unique: true }, // "age-verification"
  key: { type: Object, required: true }, // the actual verification key JSON
  updatedAt: { type: Date, default: Date.now },
})

const VerificationKeyModel = mongoose.models.VerificationKey || mongoose.model("VerificationKey", VerificationKeySchema, "vkeys");

export default VerificationKeyModel;

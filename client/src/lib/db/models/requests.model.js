import mongoose, { Schema } from "mongoose";

const ObjectId = Schema.Types.ObjectId;

const RequestSchema = new Schema({
    sessionId: { type: String, required: true, unique: true },
    user: { type: ObjectId, ref: "User", required: true },
    proofType: [String],
    requestedFields: [String],
    requestTime: { type: Date, default: Date.now },
    status: { type: String, default: "Pending" }, // "Pending", "Completed", "Revoked", "Rejected"
    timerEnd: Date,
    proofStatus: { type: String, default: "awaited" },
});

const RequestModel = mongoose.models.Request || mongoose.model("Request", RequestSchema, "requests");

export default RequestModel;
# Agentic Ethereum Hackathon India

# 🛠 ZK-AI BharatID: A Privacy-First Identity & Behavior Intelligence Stack for Cross-Industry Public Infrastructure - [ZUGZWANG]

Welcome to our submission for the *Agentic Ethereum Hackathon* by Reskilll & Geodework! This repository includes our project code, documentation, and related assets.

---

## 📌 Problem Statement

We addressed the challenge: *India’s centralized identity systems like Digilocker lack user-controlled consent, privacy-preserving proofs, and are vulnerable to replay or location spoofing attacks. There’s no dynamic session validation or AI-driven data utilization of public records while keeping identity decentralized.*

India’s current public service infrastructure (e.g., Digilocker, job portals, e-health records) relies on centralized Web2 systems to manage user identity, age, location, and session data. These systems suffer from:

1. Centralized Control: Users have little control over what data is shared or how it’s used. Consent is vague, non-session-specific, and often not cryptographically auditable.
2. No Fine-Grained Privacy: Sharing full Aadhaar or location exposes sensitive personal data. No zk-proof mechanism exists to allow partial, verifiable disclosure (e.g., “above 18” without sharing DOB).
3. Replay & GPS Spoofing Attacks: Service providers can’t cryptographically verify if the location or age data was valid at the time of access — risking fraud and impersonation.
4. Static Sessions: Web2 systems lack dynamic session proofing, making them vulnerable to unauthorized reuse or false-positive data checks.
5. No Intelligence Layer: Authorities or regulators have no AI-driven interface to monitor or detect misuse, suspicious session patterns, or validate claims at scale.
6. Sectoral Isolation: Current identity systems aren’t easily reusable across jobs, healthcare, education, or finance — each sector maintains siloed verification processes

---

## 💡 Our Solution

*Project Name:* ZK-AI BharatID: A Privacy-First Identity & Behavior Intelligence Stack for Cross-Industry Public Infrastructure 
We propose a Web3-based identity and location verification system using zk-SNARKs and session-based consent. Each user action is timestamped and tied to a dynamic verifiable credential (VC) without revealing sensitive information. A parallel ML model flags anomalies like spoofed GPS or repeated logins. An AI agent interfaces with government dashboards to summarize behavior across sectors—employment, health, mobility, and finance—enabling real-time, privacy-preserving insights for cross-industry policy intelligence and misuse prevention.

---

## 🧱 Tech Stack

- 🖥 Frontend: React / Next.js / HTML
- ⚙ Backend: Python / Flask / Node.js
- 🧠 AI: Gemini
- 🔗 Blockchain: Ethereum / Solidity / HardHat
- 🔍 DB/Storage: MongoDB / IPFS
- 🚀 Hosting: Vercel

---

## 📽 Demo

- 🎥 *Video Link*: Dynamic age & location zk proof: https://drive.google.com/file/d/144mr0pDCersiGGzOrAZwBRI6Y_OIlyg2/view?usp=sharing
AI Agent: https://drive.google.com/file/d/1OZg9I2Xr_LTN7ShUE56mkgP4ugXXxavI/view?usp=sharing

---

## 📂 Repository Structure

```bash
├── client/           # Frontend code
├── web/            # AI Agent/ Backend code
├── contracts/          # Smart contracts
├── README.md           # A detailed description of your project
├── PPT Ai Agentic Eth - Zugzwang.pptx

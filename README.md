# Agentic Ethereum Hackathon India

# 🛠 EduRaksha Agent - [GenZenius]

Welcome to our submission for the *Agentic Ethereum Hackathon* by Reskilll & Geodework! This repository includes our project code, documentation, and related assets.

---

## 📌 Problem Statement

We addressed the challenge: *“[Scholarship scmas]”*  
Current verification systems are plagued by privacy concerns, rampant fraud, and the inefficiencies of manual validation. These challenges lead to delays, inaccuracies, and a lack of trust in the system. It is essential to address these issues to ensure secure and reliable verification for all students.

---

## 💡 Our Solution

*Project Name:* [EduRaksha Agent]  
- *Decentralized Verification*: Authorities issue signed digital credentials (e.g., caste, income, marks) stored in students’ Self-Sovereign Identity (SSI) wallets.
- *Privacy via ZKPs*: Students prove eligibility (e.g., “income < ₹1,00,000”) using Zero-Knowledge Proofs (ZKPs) without revealing sensitive data.
- *Blockchain Trust*: Ethereum with ENS verifies issuer trust; smart contracts ensure tamper-proof, automated validation.
- *Multilingual AI Chatbot*: LLAMA-powered AI supports regional languages (e.g., Hindi, Tamil), using NLP to guide non-technical users via text or voice.
- *Benefits*: Protects privacy, prevents fraud, reduces verification delays, and enhances accessibility for diverse linguistic groups.
- *Tech Stack*: Ethereum, Polygon ID, Stomo Connect, Solidity, Hardhat, React, Ollama, and multilingual NLP models (e.g., XLM-RoBERTa).
- *Future Impact*: Scalable globally, promotes education equity, and sets a standard for secure, inclusive verification.

---

## 🧱 Tech Stack

- 🖥 Frontend: [React]
- ⚙ Backend: [Node.js]
- 🧠 AI: [Llama 3]
- 🔗 Blockchain: [Ethereum / Solidity]
- 🔍 DB/Storage: [IPFS]
- 🚀 Hosting: [Vercel]

---

## 📽 Demo

- 🎥 *Video Link*: [https://drive.google.com/file/d/1CIMFqYvX5fZw8t4Zfh6GOhI8GtdTlwQX/view?usp=drivesdk]
- [https://github.com/Rishal14/EduRaksha-Agent]


---

## 📂 Repository Structure

```bash
.
GenZenius/
├── frontend-next/
│   ├── backend/
│   │   ├── DEPLOYMENT.md
│   │   ├── didkit-service.js
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   ├── env.example
│   │   ├── healthcheck.js
│   │   ├── index.js
│   │   ├── jest.config.js
│   │   ├── middleware/
│   │   │   ├── errorHandler.js
│   │   │   └── validation.js
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── README.md
│   │   └── test/
│   │       ├── api.test.js
│   │       └── setup.js
│   ├── components.json
│   ├── contracts/
│   │   ├── CredentialRegistry.sol
│   │   ├── EduRakshaVerifier.sol
│   │   ├── EnhancedCredentialRegistry.sol
│   │   ├── ENSVerifier.sol
│   │   ├── IssuerTrust.sol
│   │   ├── Lock.sol
│   │   └── SemaphoreVerifier.sol
│   ├── eslint.config.mjs
│   ├── GOOGLE_API_SETUP.md
│   ├── LOGIN_SETUP.md
│   ├── next.config.ts
│   ├── OLLAMA_SETUP.md
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── public/
│   │   ├── file.svg
│   │   ├── globe.svg
│   │   ├── next.svg
│   │   ├── vercel.svg
│   │   └── window.svg
│   ├── README.md
│   ├── scripts/
│   │   └── test-translation.js
│   ├── src/
│   │   ├── app/
│   │   │   ├── ai-test/
│   │   │   │   └── page.tsx
│   │   │   ├── api/
│   │   │   │   ├── auth/
│   │   │   │   │   └── [...nextauth]/
│   │   │   │   │       └── route.ts
│   │   │   │   ├── issuer-info/
│   │   │   │   │   └── route.ts
│   │   │   │   ├── scholarships/
│   │   │   │   │   └── route.ts
│   │   │   │   ├── translate/
│   │   │   │   │   └── route.ts
│   │   │   │   └── vertex-ai/
│   │   │   │       └── route.ts
│   │   │   ├── auth/
│   │   │   │   └── signin/
│   │   │   │       └── page.tsx
│   │   │   ├── blockchain-test/
│   │   │   ├── chat/
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── didkit-demo/
│   │   │   │   └── page.tsx
│   │   │   ├── favicon.ico
│   │   │   ├── globals.css
│   │   │   ├── income-test/
│   │   │   │   └── page.tsx
│   │   │   ├── issuer/
│   │   │   │   └── page.tsx
│   │   │   ├── layout.tsx
│   │   │   ├── ocr-test/
│   │   │   │   └── page.tsx
│   │   │   ├── page.tsx
│   │   │   ├── scholarship/
│   │   │   │   ├── application/
│   │   │   │   │   └── [id]/
│   │   │   │   │       └── page.tsx
│   │   │   │   ├── dashboard/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── scholarship-enhanced/
│   │   │   │   └── page.tsx
│   │   │   ├── ssi-wallet/
│   │   │   │   └── page.tsx
│   │   │   ├── translation-test/
│   │   │   │   └── page.tsx
│   │   │   ├── verifier/
│   │   │   │   └── page.tsx
│   │   │   ├── verify/
│   │   │   │   └── page.tsx
│   │   │   ├── wallet/
│   │   │   │   └── page.tsx
│   │   │   └── zkp-generator/
│   │   │       └── page.tsx
│   │   ├── components/
│   │   │   ├── AgentChat.tsx
│   │   │   ├── AuthButtons.tsx
│   │   │   ├── Navbar.tsx
│   │   │   ├── Providers.tsx
│   │   │   ├── ui/
│   │   │   │   ├── avatar.tsx
│   │   │   │   ├── badge.tsx
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── dropdown-menu.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── label.tsx
│   │   │   │   ├── progress.tsx
│   │   │   │   ├── select.tsx
│   │   │   │   ├── separator.tsx
│   │   │   │   ├── tabs.tsx
│   │   │   │   └── textarea.tsx
│   │   │   └── VCCard.tsx
│   │   ├── lib/
│   │   │   ├── ai-assistant.ts
│   │   │   ├── blockchain-config.ts
│   │   │   ├── blockchain-service.ts
│   │   │   ├── certificate-processor.ts
│   │   │   ├── didkit-service.ts
│   │   │   ├── ollama-config.ts
│   │   │   ├── scholarship-scraper.ts
│   │   │   ├── ssi-wallet.ts
│   │   │   ├── translation-service.ts
│   │   │   ├── use-blockchain.ts
│   │   │   ├── utils.ts
│   │   │   ├── vc-utils.ts
│   │   │   ├── vertex-ai-assistant.ts
│   │   │   ├── vertex-ai-service.ts
│   │   │   └── zkp-generator.ts
│   │   └── pages/
│   │       └── api/
│   │           └── auth/
│   ├── TRANSLATION_SETUP.md
│   └── tsconfig.json
└── README.md



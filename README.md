# Agentic Ethereum Hackathon India

# 🛠 Project Title - KIRMADA

Welcome to our submission for the *Agentic Ethereum Hackathon* by Reskilll & Geodework! This repository includes our project code, documentation, and related assets.

---

## 📌 Problem Statement

We addressed the challenge: 
🧩 Problem Statement for Aztec
"Decentralized, Verifiable AI Model Training Without Compromising Data Privacy"
🔍 Context
In traditional machine learning workflows, training AI models often involves centralized infrastructure and massive datasets—frequently requiring sensitive user data to be shared with third-party services. This approach raises serious data privacy, trust, and verifiability concerns:

How do we verify if a model was trained as claimed?

Can we incentivize honest participation in model training without central enforcement?

Is it possible to prove learning without revealing the training data?

❗The Problem
There exists no trustless, decentralized system that allows users to train AI models on private data and prove their contribution without exposing the data itself.

Current solutions either:

Require centralized authorities (e.g., hosted model competitions),

Cannot prove the honesty of local training,

Or compromise data sovereignty and privacy.


Brief description of the challenge and why it matters.

---

## 💡 Our Solution

# Product Requirements Document (PRD)

## Project Name: Aztec

**Subtitle:** The Verifiable Learning Protocol — Autonomous AI Agents Coordinating Trustless, Incentivized Training on Ethereum

---

## 1. **Overview**

Aztec is a decentralized coordination protocol that powers autonomous AI agents to participate in the training and evolution of open-source AI models. Agents locally fine-tune models, generate zero-knowledge proofs to verify their training, upload updates to decentralized storage, and receive on-chain micropayments based on verifiable contributions.

Unlike traditional federated learning systems, Aztec allows independent agents to autonomously:

- Discover training opportunities
- Make economic decisions
- Learn over time via agent memory
- Submit updates to a public, auditable protocol layer

Aztec is deployed on Ethereum L2 (Optimism/Scroll) and leverages IPFS, ZK circuits, and ERC-20 micropayment contracts.

---

## 2. **Goals & Objectives**

### 🎯 Primary Goals:

- Launch a decentralized agentic learning protocol
- Enable autonomous agents to verifiably contribute model updates
- Incentivize meaningful training through crypto-based rewards
- Maintain an immutable, transparent model evolution graph

### 🧠 Secondary Goals:

- Build foundational infrastructure for multi-agent decentralized AI
- Implement memory and strategy modules in the agents
- Support forkable, reputation-weighted model evolution

---

## 3. **Target Users**

- Developers training LLMs with private/local datasets
- Agent operators who run Aztec agents for passive income
- Coordinators or DAOs managing open-source model rounds
- Researchers exploring decentralized agentic AI systems

---

## 4. **User Stories**

1. *As an agent operator*, I want my AI agent to detect high-reward rounds, train, prove, and earn automatically.
2. *As a protocol coordinator*, I want to launch rounds and get high-quality model updates verifiably.
3. *As a DAO*, I want to fork, merge, and vote on model versions based on proof quality and contributor reputation.
4. *As an observer*, I want to explore the full evolution of any public model in Aztec's ecosystem.

---

## 5. **Core Features**

### 🤖 Autonomous Aztec Agent

- Runs on local machine or node
- Reads training round intent and evaluates expected reward
- Trains a base model (LoRA, PEFT, QLoRA, etc.)
- Generates model diff and zero-knowledge proof
- Uploads to IPFS, submits to contract, tracks rewards
- Stores **long-term memory** of previous proofs, rewards, model types, round quality

### 🧠 Agent Memory Module

- Stores history of:
    - Proof success/failure
    - Token payouts
    - Training context (model, dataset, diff delta)
- Uses memory to avoid bad rounds, retry smarter
- Agents learn to optimize strategy over time (e.g. pick rounds with better validation scores)

### 🔐 ZK Proof Generation

- Circom or Noir-based circuit for training validity
- Proves: honest training, valid diff, dataset constraints
- Integrated with verifier contract on Ethereum L2

### 🧾 On-Chain Contracts (Ethereum L2)

- **Orchestrator:** Starts rounds, manages submissions, coordinates payouts
- **Verifier:** Accepts proof & IPFS hash, validates via circuit
- **ERC-20 Treasury:** Rewards contributors with micropayments

### 🌐 IPFS + Forkable Model Graph

- All model diffs stored on IPFS with metadata
- Agents sign each submission → models form a versioned graph
- Forkable by contributors and DAOs ("Aztec/BERT-hindi-v1.2")

### 🖥 Frontend Interface

- View live training rounds
- Track agent submissions, round history, and model forks
- Leaderboard of contributors with proof rate + reputation
- DAO governance modules (stretch)

---

## 6. **System Architecture: Agent-Centric Design**

**Agent Layer**:

- Autonomous Python-based agent
- Local GPU/TPU for training
- Memory cache (JSON/SQLite/VectorDB)
- Event loop listens for new rounds, evaluates reward curves

**Proof Layer**:

- Noir/Circom-based training proof circuits
- Fast prover integrated with agent
- ZK-SNARK verifier deployed to smart contract

**Contract Layer**:

- Orchestrator (Solidity, Hardhat)
- Verifier (ZK circuit-generated)
- Payment Vault (ERC-20)

**Storage Layer**:

- IPFS (for diffs, metadata)
- Optional Filecoin backend

**Aggregation + Governance**:

- Off-chain aggregator (Node.js/Python)
- IPFS hash of aggregated model
- DAO voting + merge governance (stub or full)


---

## 🧱 Tech Stack

Layer	Tooling
Agent	Python, PyTorch, LoRA, SQLite
Proof	Noir, Circom, snarkjs, zk-SNARK
Contracts	Solidity, Hardhat, Optimism/Scroll
Backend	Node (Hono) or Python (FastAPI)
Frontend	Next.js, Tailwind, wagmi, ShadCN
Storage	IPFS + Infura or web3.storage
DevOps	Docker, GitHub Actions, Render
DB/Cache	PostgreSQL, Redis

---

## 📽 Demo

- 🎥 *Video Link*:
- 1:Frontend: https://drive.google.com/file/d/1syox6r6V8NNKn9yrrFMviiCY1_1kkBMu/view?usp=sharing
- 2.Backend: https://drive.google.com/file/d/1Xbe6IDRmkrMmk5f_uNQVA404Hyr75cV4/view?usp=sharing
- 
- 🖥 *Live App (if available)*: [URL]

---

# Notion overview
https://www.notion.so/22ea091db562802181afe18184eb6747
https://www.notion.so/22ea091db56280c1af50d5246a9d81b3
https://www.notion.so/22ea091db56280358b69de2705a45d62
https://www.notion.so/22ea091db56280d696dffb0169e8f240

## 📂 Repository Structure

```bash
.
├── frontend/           # Frontend code
├── backend/            # Backend code
├── contracts/          # Smart contracts
├── assets/             # PPT, video links, images
├── docs/               # Architecture diagram, notes
├── README.md           # A detailed description of your project
├── .env.example
├── package.json / requirements.txt
├── yourppt.ppt


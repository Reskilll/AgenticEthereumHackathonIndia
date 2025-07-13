# Agentic Ethereum Hackathon India

# Smart Contract Audit MCP Server - Team AgenticHacker

Welcome to our submission for the *Agentic Ethereum Hackathon* by Reskilll & Geodework! This repository includes our project code, documentation, and related assets.

---

## 📌 Problem Statement

We addressed the challenge: *"Building AI-Powered Tools for Ethereum Development"*  

**The Problem**: Smart contract security audits are time-consuming, expensive, and require specialized expertise. Traditional audit processes take weeks or months, creating bottlenecks in DeFi development and leaving projects vulnerable to exploits.

**Why it matters**: Over $3 billion has been lost to smart contract vulnerabilities in 2023 alone. Most projects can't afford professional audits, leading to unsafe deployments and user fund losses.

---

## 💡 Our Solution

**Project Name**: Smart Contract Audit MCP Server  

**The Solution**: An AI-powered Model Context Protocol (MCP) server that transforms any coding agent (Cursor, Claude, etc.) into a professional smart contract auditor. Instead of building another audit tool, we provide the missing infrastructure that makes existing AI agents audit-capable.

**Key Innovation**: 
- Converts complex security audits into conversational workflows
- Integrates battle-tested tools (Slither, Foundry) with AI intelligence
- Provides systematic audit methodologies as reusable prompts
- Enables proof-of-concept exploit generation for vulnerability validation

**Target Users**: DeFi developers, security researchers, audit firms, and hackathon participants who need rapid, professional-grade security analysis.

---

## 🧱 Tech Stack

- 🖥 **Frontend**: Terminal-based MCP server interface
- ⚙ **Backend**: Python with FastMCP framework
- 🧠 **AI**: OpenAI GPT-4 for intelligent contract analysis
- 🔗 **Blockchain**: Ethereum, Arbitrum, Base, Polygon (via Etherscan APIs)
- 🔍 **Security Tools**: Slither (static analysis), Foundry (fuzzing), Anvil (exploit testing)
- 🚀 **Integration**: Model Context Protocol for seamless AI agent integration

---

## 📽 Demo

- 🎥 **Video Demo**: [Coming Soon]  
- 🖥 **Live Integration**: Works with any MCP-compatible coding agent (Cursor, Claude Desktop)
- 📊 **Sample Audit**: Demonstrates auditing real DeFi protocols with AI assistance

---

## 🚀 Key Features

### 1. **Automated Contract Fetching**
- Download verified contracts from any supported blockchain
- Unified API for Ethereum, Arbitrum, Base, Polygon networks
- Automatic multi-file contract reconstruction

### 2. **AI-Powered Analysis**
- Generate detailed project indexes with token counting
- Exclude irrelevant library code automatically
- Prioritize contracts by risk and complexity

### 3. **Professional Audit Tools**
- Slither integration with 70+ security detectors
- Foundry fuzzing with customizable parameters
- Dependency graph generation for attack surface mapping

### 4. **Proof-of-Concept Generation**
- Anvil fork setup for exploit development
- Foundry test templates for vulnerability demonstration
- Step-by-step exploit tutorials

### 5. **Systematic Methodologies**
- Bootstrap prompts for contract prioritization
- Vulnerability scan templates for systematic review
- Dependency analysis for complex protocol interactions

---

## 📂 Repository Structure

```bash
AgenticEthereumHackathonIndia/
├── frontend/                    # MCP client examples
├── backend/                     # Core MCP server implementation
│   ├── audit_mcp_server.py     # Main MCP server
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment configuration
├── contracts/                   # Sample contracts for testing
│   └── noya-JUL-2025-audit-scope/  # Real audit target
├── assets/                      # Demo materials
│   ├── demo-video.mp4          # Video demonstration
│   ├── architecture.png        # System architecture
│   └── hackathon-presentation.ppt
├── docs/                        # Technical documentation
│   ├── API.md                  # MCP tool documentation
│   ├── TUTORIAL.md             # Step-by-step usage guide
│   └── ARCHITECTURE.md         # System design
├── README.md                    # This file
└── .env.example                # Environment setup template
```

---

## 🎯 Impact & Value

### For Developers:
- **10x faster audits**: From days to minutes with AI assistance
- **Cost reduction**: No need for expensive manual audit services
- **Learning tool**: Understand vulnerabilities through systematic analysis

### For Security:
- **Proactive defense**: Catch vulnerabilities before deployment
- **Standardized process**: Systematic audit methodologies
- **Exploit validation**: Prove vulnerabilities with working POCs

### For Ethereum Ecosystem:
- **Reduced exploit risks**: Better security tooling for all developers
- **Faster innovation**: Remove security bottlenecks in DeFi development
- **Educational impact**: Democratize security audit knowledge

---

## 🏆 Hackathon Achievements

- **Innovation**: First MCP server dedicated to smart contract security
- **Practical utility**: Solves real pain points in DeFi development
- **AI integration**: Seamlessly combines static analysis with intelligent review
- **Open source**: Extensible platform for the security community

---

## 🚀 Getting Started

1. **Clone the repository**:
```bash
git clone git@github.com:gabinfay/AgenticEthereumHackathonIndia.git
cd AgenticEthereumHackathonIndia
```

2. **Install dependencies**:
```bash
cd backend
pip install -r requirements.txt
foundryup  # Install Foundry
pip install slither-analyzer
```

3. **Configure environment**:
```bash
cp .env.example .env
# Add your OPENAI_API_KEY and ETHERSCAN_API_KEY
```

4. **Run the MCP server**:
```bash
python audit_mcp_server.py
```

5. **Integrate with Cursor**: Follow the MCP configuration guide in the main README

---

## 🔮 Future Roadmap

- **Multi-tool integration**: Add Mythril, Manticore, Echidna support
- **Advanced AI models**: Fine-tuned models for security analysis
- **Web interface**: Browser-based audit dashboard
- **Automated reporting**: Generate professional audit reports
- **Community database**: Shared vulnerability patterns and fixes

---

## 👥 Team

**Team AgenticHacker**
- **Gabin Fay**: Full-stack developer, security researcher, MCP architecture
- **Focus**: Building AI-powered security tools for the Ethereum ecosystem

---

## 🙏 Acknowledgments

- **Reskilll & Geodework** for organizing the Agentic Ethereum Hackathon
- **OpenAI** for providing the AI infrastructure
- **Crytic/Trail of Bits** for Slither static analysis
- **Foundry** team for the fuzzing and testing framework
- **Model Context Protocol** for enabling seamless AI agent integration

---

*Built with ❤️ for the Ethereum security community*


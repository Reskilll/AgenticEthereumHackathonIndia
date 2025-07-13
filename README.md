# Agentic Ethereum Hackathon India

# 🛠 CivicChain - [Team Goose]

Welcome to our submission for the *Agentic Ethereum Hackathon* by Reskilll & Geodework! This repository includes our project code, documentation, and related assets.

---

## 📌 Problem Statement

We addressed the challenge: *"Building Transparent and Accountable Governance Systems"*  

Traditional grievance management systems lack transparency, accountability, and often suffer from spam complaints and inefficient tracking. Citizens struggle to hold government accountable for addressing their concerns, while administrators lack comprehensive analytics to prioritize and manage grievances effectively.

---

## 💡 Our Solution

*Project Name:* **CivicChain - Transparent Civic Governance Platform**  

CivicChain is a modern React-based civic governance platform that leverages Zero-Knowledge Proof (ZKP) technology for mandatory Aadhaar verification. Our solution ensures transparent grievance management while preserving user privacy, prevents spam through ZKP authentication, and provides comprehensive analytics for both citizens and administrators to track government accountability in real-time.

**Key Features:**
- 🔐 Privacy-preserving Aadhaar ZKP verification
- 📊 National public leaderboard for state-wise performance
- 🎯 AI-powered grievance categorization and insights
- 📈 Real-time analytics and comprehensive dashboards
- 🏛️ Transparent government accountability tracking

---

## 🧱 Tech Stack

- 🖥 **Frontend**: React 18, Vite, TailwindCSS, Framer Motion
- ⚙ **Backend**: Node.js, Express.js, Vercel Serverless Functions
- 🧠 **AI**: OpenAI GPT-4, LangChain for grievance analysis and insights
- 🔗 **Blockchain/ZKP**: Anon Aadhaar ZKP (@anon-aadhaar/core, @anon-aadhaar/react)
- 🔍 **Database**: MongoDB Atlas (cloud-hosted)
- 📊 **Data Visualization**: D3.js, Recharts
- 🔐 **Authentication**: JWT, bcrypt, Zero-Knowledge Proofs
- 🚀 **Hosting**: Vercel (Frontend + Serverless Backend)

---

## 📽 Demo

- 🎥 *Video Demo*: [youtube link](https://youtu.be/ClQnGPiqh8s?si=tav_rW4JaBhmH-9f)
- 🖥 *Live App*: [https://civic-chain.vercel.app](https://civic-chain.vercel.app)
- Github Repo: https://github.com/BishalJena/civic-chain
---

## 📂 Repository Structure

```bash
.
├── api/                    # Vercel serverless functions
│   └── index.js           # Main API endpoint
├── backend/               # Local development server
│   ├── server.js          # Express server
│   └── package.json       # Backend dependencies
├── src/                   # React frontend source
│   ├── components/        # Reusable UI components
│   │   ├── auth/         # Authentication components
│   │   └── ui/           # Base UI components
│   ├── pages/            # Application pages
│   │   ├── admin-authentication-portal/
│   │   ├── citizen-dashboard-grievance-filing/
│   │   ├── comprehensive-admin-dashboard/
│   │   ├── national-public-leaderboard/
│   │   └── state-specific-performance-dashboard/
│   ├── contexts/         # React context providers
│   ├── utils/            # Utility functions & AI services
│   └── styles/           # Global styles
├── scripts/              # Database setup and population
├── public/               # Static assets
├── build/                # Production build output
├── .env                  # Environment variables
├── vercel.json           # Vercel deployment config
├── package.json          # Frontend dependencies
├── tailwind.config.js    # TailwindCSS configuration
├── vite.config.mjs       # Vite build configuration
└── README.md             # Project documentation
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- MongoDB Atlas account
- OpenAI API key
- Vercel account (for deployment)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/BishalJena/civic-chain.git
cd civic-chain
```

2. **Install dependencies**
```bash
npm install
```

3. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your MongoDB URI, OpenAI API key, and JWT secret
```

4. **Start development server**
```bash
npm run dev
```

5. **Access the application**
- Frontend: http://localhost:4028
- API: http://localhost:3001 (if running backend separately)

### Production Deployment

Deploy to Vercel with one command:
```bash
vercel --prod
```

---

## 🔐 Security & Privacy Features

- **Zero-Knowledge Proof Authentication**: Mandatory Aadhaar verification without exposing personal data
- **JWT-based Security**: Secure session management
- **Input Validation**: Comprehensive form validation and sanitization
- **CORS Protection**: Configured for secure cross-origin requests
- **Environment Security**: Sensitive data stored in environment variables

---

## 🏗️ Architecture

CivicChain follows a modern serverless architecture:

1. **Frontend**: React SPA hosted on Vercel with static generation
2. **Backend**: Node.js serverless functions on Vercel
3. **Database**: MongoDB Atlas for scalable data storage
4. **Authentication**: Hybrid approach with ZKP + JWT
5. **AI Integration**: OpenAI API for intelligent grievance analysis

---

## 🎯 Key Innovations

1. **Privacy-First Approach**: ZKP ensures citizens can file grievances without compromising personal data
2. **AI-Powered Insights**: Automated categorization and priority assignment for grievances
3. **Transparent Accountability**: Public leaderboards create pressure for government responsiveness
4. **Real-time Analytics**: Live dashboards for both citizens and administrators
5. **Spam Prevention**: ZKP verification eliminates fake/spam complaints

---

## 🔮 Future Roadmap

- [ ] Multi-language support
- [ ] Smart contracts for automated government response tracking
- [ ] Mobile app development (React Native)
- [ ] Integration with government APIs

---

## 👥 Team

**Team CodeCrafters**
- **Bishal Jena** - Full Stack Developer & Project Lead
- [Add other team members]

---

## 📄 License

This project is developed for the Agentic Ethereum Hackathon India.

---

## 🙏 Acknowledgments

- Reskilll & Geodework for organizing the hackathon
- Anon Aadhaar team for ZKP infrastructure
- OpenAI for AI capabilities
- Vercel for hosting and serverless infrastructure

---

*Built with ❤️ for transparent governance and citizen empowerment*

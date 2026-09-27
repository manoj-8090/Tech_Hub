# TechHub: Universal Multi-Source Knowledge & Consensus Answer Engine

TechHub is an intelligent multi-source knowledge engine, consensus verification platform, and real-world answer selector designed to answer and analyze **ANY question**—spanning **Science, Health & Medicine, Business & Finance, History, Daily Life, and Technology & Programming**. Instead of relying on a single query source or an unverified AI output, TechHub queries top global platforms simultaneously (**ChatGPT (GPT-4o), Google Gemini AI, Wikipedia, Web Search, YouTube, Reddit, Stack Overflow, MDN Web Docs, GeeksforGeeks, GitHub, and Dev.to**), extracts answers, computes confidence and reliability scores, executes a **Consensus Detection** algorithm, and automatically promotes the **#1 Most Relevant Real-World Answer**.

---

## 🌟 Key Features

1. **Universal Question & Polyglot Code Intelligence**: Works seamlessly for any domain:
   - **Polyglot Code Generation (Any Programming Language)**: Request any algorithm, script, data structure, web server, or utility in **Rust, Go, C++, Java, Python, JavaScript, TypeScript, C#, C, Kotlin, Swift, PHP, Ruby, SQL, Bash, Dart, HTML/CSS**, and get complete, runnable code with interactive one-click "📋 Copy Code" buttons and time/space complexity analysis.
   - **Science & Nature**: Explains physics, chemistry, astronomy, biology (e.g., Rayleigh scattering, photosynthesis, gravity).
   - **Finance & Economics**: Provides financial formulas, real-world examples, and economic principles (e.g., compound interest, inflation hedging).
   - **Health & Wellness**: Evidence-based medical and lifestyle science (e.g., daily hydration metrics, sleep architecture).
   - **History & World Events**: Chronological accounts, causal frameworks (M-A-I-N), and treaty consequences.
2. **Parallel Multi-Source Retrieval with Dynamic Routing**:
   - **Universal Sources (Queried for every question)**: ChatGPT (GPT-4o), Google Gemini AI, Wikipedia (with live summary extracts), Google / Web Search, YouTube, Reddit.
   - **Technical Sources (Queried when programming/code is involved)**: Stack Overflow, MDN Web Docs, GeeksforGeeks, GitHub, Dev.to.
3. **📎 Direct File & Code Upload**: Users can click the **📎 paperclip icon on the left side of the search bar** to upload code or text documents (`.py`, `.js`, `.ts`, `.java`, `.cpp`, `.css`, `.json`, `.txt`, etc.) up to 500 KB for direct analysis and optimization.
4. **🏆 #1 Real-World Answer Spotlight**: Multi-factor scoring promotes the single best real-world answer to a featured gold-bordered card, complete with a domain-tailored justification explaining why it was selected.
5. **Consensus Detection Algorithm**: Evaluates source agreement vs. minority/divergent perspectives, generating an actionable consensus summary.
6. **Interactive Polyglot Code Blocks**: Clean IDE dark container with language badge, code syntax formatting, and a one-click copy button (`📋 Copy Code`) with active green state transitions (`✓ Copied!`).
7. **JWT Authentication & SQLite Persistence**: Full account management with encrypted sessions, search history tracking, and one-click answer bookmarking.
8. **Modern Responsive Design**: Dark/light theme toggle, custom confidence meters, dynamic source filter chips, and code copy tools.

---

## 🏗️ Project Architecture

```
C:\Users\manoj\Desktop\Final_project\
├── backend/
│   ├── app.py                     # Flask entry point & static file server
│   ├── config.py                  # Environment & secret configuration
│   ├── database.py                # SQLite connection manager & schema initializer
│   ├── models.py                  # User, SearchHistory, SavedAnswer data models
│   ├── auth.py                    # JWT authentication & password hashing
│   ├── services/
│   │   ├── search_service.py      # Parallel multi-source aggregator (8 sources)
│   │   └── consensus_service.py   # Consensus detection & trust scoring
│   ├── routes/
│   │   ├── auth_routes.py         # Register, Login, Profile endpoints
│   │   └── search_routes.py       # Search, Related, History, Saved endpoints
│   ├── requirements.txt           # Python package dependencies
│   ├── .env                       # Local environment variables
│   └── .env.example               # Environment template
├── frontend/
│   ├── index.html                 # Public landing page
│   ├── dashboard.html             # User search interface
│   ├── results.html               # Dual-panel analytics & consensus results
│   ├── history.html               # Search history timeline
│   ├── saved.html                 # Bookmarked solutions
│   ├── profile.html               # Account profile
│   ├── login.html                 # Sign-in page
│   ├── register.html              # Registration page
│   ├── style.css                  # CSS theme & layout system
│   └── script.js                  # Frontend application logic
├── start_server.py                # Python launcher
├── run.bat                        # Windows one-click batch runner
└── README.md                      # Documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ installed ([python.org](https://www.python.org/))

### 1. One-Click Launch (Windows)
Double-click `run.bat` in the project root. It will install dependencies and launch the server at `http://localhost:5000`.

### 2. Manual Terminal Launch
```bash
# 1. Navigate to project root
cd C:\Users\manoj\Desktop\Final_project

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Start the application
python start_server.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

## 📡 REST API Reference

| Endpoint | Method | Auth | Description |
| :--- | :---: | :---: | :--- |
| `POST /api/auth/register` | `POST` | None | Create new developer account (`name`, `email`, `password`) |
| `POST /api/auth/login` | `POST` | None | Authenticate and obtain JWT token |
| `GET /api/profile` | `GET` | Bearer | Retrieve logged-in user profile details |
| `POST /api/search` | `POST` | Optional | Parallel multi-source search + consensus detection |
| `POST /api/related` | `POST` | None | Retrieve dynamically generated related questions |
| `POST /api/history/save` | `POST` | Bearer | Bookmark an answer to user account |
| `GET /api/saved` | `GET` | Bearer | List all saved answers |
| `GET /api/history` | `GET` | Bearer | Retrieve search history timeline |
| `GET /health` | `GET` | None | Service health status |

---

## ⚙️ How Consensus Detection Works

1. **Domain Trust Weights**: Every source domain is assigned a baseline trust score:
   - Stack Overflow: $9/10$ (peer-reviewed, score-weighted)
   - Gemini AI: $9/10$ (state-of-the-art LLM code synthesis)
   - Wikipedia / GitHub: $8/10$ (official reference / active repositories)
   - Reddit / Dev.to / Google / YouTube: $6-7/10$ (community discussions & tutorials)
2. **Confidence Computation**: Each result item is evaluated based on vote score, verification status, and relevance to produce a confidence rating ($0.0 - 1.0$).
3. **Clustering & Classification**: The system groups sources with high confidence ($\ge 80\%$) into the **Consensus Group** and secondary/exploratory platforms into the **Minority Group**.
4. **Synthesis Narrative**: An intelligent narrative explains the core technical standard and contrasts it with deprecated or alternative community patterns.

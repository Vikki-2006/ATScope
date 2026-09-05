
    
# AI Resume Analyzer - SaaS Platform

A production-grade, commercial-quality **AI Resume Analyzer and ATS Optimization** platform built with Python, FastAPI, SQLAlchemy, Jinja2, Tailwind CSS, Alpine.js, Chart.js, spaCy, and scikit-learn.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v3-38BDF8)

---

## Key Features

- **Modern SaaS Aesthetics**: Designed with glassmorphism, glowing gradients, dark mode persistence, and micro-interactions inspired by Notion, Linear, Vercel, and Stripe.
- **ATS Multi-Dimensional Scoring Engine**:
  - Overall Resume Score
  - ATS Compatibility Rating (/100)
  - Formatting Quality & Structure Audit
  - Readability Index (Flesch Reading Ease & Action Verbs Density)
  - Keyword Density & Match Score
  - Skill Coverage Matrix
  - Experience Impact & Achievement Metrics
  - Education Completeness
  - Project Portfolio Score
- **Job Description Matcher**:
  - Paste any target job description.
  - TF-IDF Cosine Vector similarity calculation using `scikit-learn`.
  - Live breakdown of Matched Skills, Missing Target Skills, Recommended Skill Additions, and Keyword Gaps.
- **Actionable AI Recommendations**:
  - Professional summary rewrites.
  - Experience bullet point optimization using the XYZ accomplishment formula.
  - Action verb replacements and formatting fixes.
- **Executive Report Generation**:
  - One-click downloadable **PDF Audit Reports** generated via `ReportLab`.
  - Downloadable **CSV Analysis Logs**.
- **Security & Authentication**:
  - JWT Token Authentication via HttpOnly cookies and Bearer headers.
  - Password Hashing using `bcrypt`.
  - Rate limiting, CSRF protection, file size/type validation.

---

## Tech Stack

### Backend
- **Python 3.12+**
- **FastAPI**: Modern, fast web framework for building APIs and rendering views.
- **SQLAlchemy**: ORM for robust database interaction.
- **Alembic**: Database migrations management.
- **SQLite / PostgreSQL**: Compatible out-of-the-box with SQLite, postgresql configurable via `DATABASE_URL`.

### Frontend
- **Jinja2**: Server-side HTML template rendering.
- **Tailwind CSS**: Custom utility styling with glassmorphic panels and responsive cards.
- **Alpine.js**: Reactive frontend component logic, file upload dropzone, toast notifications, theme switching.
- **Chart.js**: Dynamic score gauges, category bar charts, and candidate radar profiles.

### AI / NLP & Parsing
- **spaCy & scikit-learn**: Vector text matching, TF-IDF cosine similarity, keyword frequency analysis.
- **pdfplumber & python-docx**: Multi-format document parsing and text extraction.
- **ReportLab**: Executive PDF report generation.

---
## 🚀 Live Demo

<p align="center">
  <a href="https://atscope-analyzer.vercel.app/" target="_blank">
    <img src="https://img.shields.io/badge/%20Live%20Demo-Visit%20ATSCope-00C853?style=for-the-badge" alt="Live Demo">
  </a>
</p>

<p align="center">
  <b>Try ATScope AI Resume Analyzer online</b>
</p>

---
## System Architecture

```
                       +-----------------------------------+
                       |      Browser UI (Tailwind CSS     |
                       |      Alpine.js + Chart.js)        |
                       +-----------------+-----------------+
                                         |
                                HTTP / JSON / Cookies
                                         |
                                         v
                       +-----------------+-----------------+
                       |         FastAPI Server            |
                       |  (Jinja2 Views + REST API v1)     |
                       +--------+-----------------+--------+
                                |                 |
            +-------------------+                 +-------------------+
            |                                                         |
            v                                                         v
+-----------+-----------+                                 +-----------+-----------+
|    AI / NLP Services   |                                 |   SQLAlchemy ORM &    |
| - Resume Parser       |                                 |   Alembic Migrations  |
| - ATS Analyzer        |                                 | (User, Resume,    |
| - Job Matcher (TF-IDF)|                                 |  AnalysisHistory) |
| - ReportLab PDF Gen   |                                 +-----------+-----------+
+-----------------------+                                             |
                                                                      v
                                                              +---------------+
                                                              |  SQLite / DB  |
                                                              +---------------+
```

---

## Folder Structure

```
Resume Analyser/
├── alembic/                      # Database migration scripts
│   ├── versions/                 # Revision scripts
│   └── env.py                    # Alembic configuration environment
├── app/
│   ├── api/                      # REST API Endpoint Routers
│   │   └── v1/
│   │       ├── auth.py           # Authentication routes (/login, /register, /logout, /me)
│   │       ├── resumes.py        # Resume upload, fetch, list, delete
│   │       ├── analysis.py       # ATS run, Job Matcher, PDF/CSV report exports
│   │       └── user.py           # Settings, password change, account deletion
│   ├── core/                     # Application Core Configuration
│   │   ├── config.py             # Settings, Pydantic ConfigDict, upload limits
│   │   ├── database.py           # SQLAlchemy Engine and SessionLocal
│   │   ├── security.py           # bcrypt password hashing & JWT encoding
│   │   └── deps.py               # Auth dependency injection
│   ├── models/                   # SQLAlchemy DB Models
│   │   ├── user.py               # User and UserSettings models
│   │   ├── resume.py             # Resume model
│   │   └── analysis.py           # AnalysisHistory model
│   ├── schemas/                  # Pydantic Schemas for Request/Response validation
│   │   ├── user.py
│   │   ├── resume.py
│   │   └── analysis.py
│   ├── services/                 # Business Logic & NLP Engine
│   │   ├── parser.py             # PDF/DOCX parsing & Regex field extractor
│   │   ├── ats_analyzer.py       # 8-point ATS scoring engine
│   │   ├── job_matcher.py        # TF-IDF cosine similarity & skill gap analyzer
│   │   ├── ai_suggester.py       # Actionable suggestion generator
│   │   └── report_generator.py   # ReportLab PDF & CSV report export
│   ├── static/                   # Static Frontend Assets
│   │   ├── css/styles.css        # Glassmorphism & custom utility styles
│   │   ├── js/app.js             # Alpine.js stores & components
│   │   └── js/charts.js          # Chart.js visualization initializers
│   ├── templates/                # Jinja2 HTML Templates
│   │   ├── layouts/base.html     # Master HTML layout
│   │   ├── components/           # Navbar, Footer, Toast components
│   │   ├── auth/                 # Login, Register, Forgot Password, Profile
│   │   ├── landing.html          # Modern SaaS homepage
│   │   ├── dashboard.html        # Interactive Candidate Dashboard
│   │   ├── upload.html           # Drag & Drop File Uploader
│   │   ├── job_match.html        # Split-pane Job Description Matcher
│   │   ├── analysis_detail.html  # Comprehensive Audit & Recommendations Page
│   │   ├── history.html          # Filterable Analysis Log Table
│   │   └── settings.html         # User settings & Theme switcher
│   └── views/                    # Jinja2 View Controllers
│       ├── landing.py
│       ├── auth.py
│       ├── dashboard.py
│       ├── resume.py
│       ├── history.py
│       └── settings.py
├── tests/                        # Automated Pytest Suite
│   └── test_api.py
├── alembic.ini                   # Alembic configuration file
├── main.py                       # FastAPI application entrypoint
├── requirements.txt              # Dependency specifications
└── README.md                     # Project documentation
```

---

## Installation & Setup

### 1. Clone & Navigate to Project
```bash
cd "c:/Users/VIKKI/Documents/Project/Resume Analyser"
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
alembic upgrade head
```

### 5. Start Application Server
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open your browser at `http://127.0.0.1:8000` to access the application.

---

## API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register new user account |
| `POST` | `/api/v1/auth/login` | Authenticate user & issue JWT cookie |
| `POST` | `/api/v1/auth/logout` | Clear auth token cookie |
| `GET` | `/api/v1/auth/me` | Fetch current user details |
| `POST` | `/api/v1/resumes/upload` | Upload & parse PDF/DOCX resume |
| `GET` | `/api/v1/resumes` | List user uploaded resumes |
| `DELETE` | `/api/v1/resumes/{id}` | Delete uploaded resume |
| `POST` | `/api/v1/analysis/run` | Execute ATS analysis & Job Match |
| `GET` | `/api/v1/analysis/history` | List previous analysis records |
| `GET` | `/api/v1/analysis/{id}/report/pdf` | Download executive PDF report |
| `GET` | `/api/v1/analysis/{id}/report/csv` | Export analysis CSV data |
| `PUT` | `/api/v1/user/settings` | Update user settings (theme, threshold) |
| `POST` | `/api/v1/user/change-password` | Change user password |
| `DELETE` | `/api/v1/user/delete-account` | Delete user account & data |

---

## Running Automated Tests

Execute the pytest suite to verify application routing, parsing, ATS scoring, and PDF generation:

```bash
python -m pytest
```

---

## Screenshots Section

- **Landing Page**: Modern hero, feature cards, pricing grid, FAQ accordion, and dark mode theme.
- **Dashboard**: ATS Pass Rate ring, metric performance bar charts, upload quick actions, and recent audit logs.
- **Upload Dropzone**: Drag-and-drop file uploader supporting PDF and DOCX with instant file validation.
- **Job Description Matcher**: Dual-pane comparison interface showing live TF-IDF vector text similarity and skill matrix coverage.
- **Detailed Audit Report**: Score cards, candidate radar profile, matched vs missing skill pills, bullet point rewrite recommendations, and executive PDF exports.

---

## Future Improvements

1. **Cover Letter Generator**: AI-driven tailored cover letter creation based on target job description.
2. **Interview Question Simulator**: Mock technical interview question generator derived from resume experience.
3. **Multi-Language Parsing**: Support for Spanish, French, and German resume parsing.

---

## License

Distributed under the MIT License. See `LICENSE` for details.

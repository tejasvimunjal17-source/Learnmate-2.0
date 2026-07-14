# 🧭 AI Career Learning Pathway

An agentic, AI-powered career learning platform built with **Python + Streamlit**,
using **IBM watsonx.ai** and **IBM Granite** foundation models to generate
fully personalized learning roadmaps, skill-gap analyses, course &
certification recommendations, and downloadable PDF reports — wrapped in a
premium, responsive, dark/light-mode UI.

![status](https://img.shields.io/badge/status-production--ready-7C5CFF)
![python](https://img.shields.io/badge/python-3.10%2B-22D3B0)
![license](https://img.shields.io/badge/license-MIT-black)

---

## ✨ Features

- **Student Profile Form** — name, career goal, current level, study hours/week,
  preferred domain, learning preference, existing skills, with full input validation.
- **AI Career Mentor** — a fully customizable agent persona (see `agent_instructions.py`)
  powered by IBM Granite models on watsonx.ai.
- **AI Roadmap Generator** — weekly milestones with key skills, mini-projects,
  practice tasks, and recommended courses.
- **Skill-Gap Analysis** — current vs. required skill levels, prioritized, with
  an interactive readiness gauge and gap chart.
- **Course Recommendation Dashboard** — courses mapped to each week of the roadmap.
- **Certification Suggestions** — reputable, domain-relevant certifications.
- **Progress Tracker** — check off completed weeks; dashboard updates live.
- **Interactive Dashboards** — Plotly-powered charts (readiness gauge, skill-gap
  bars, cumulative study-hour projection, progress donut).
- **Downloadable PDF Reports** — a polished, professional roadmap PDF (ReportLab).
- **Premium UI** — glassmorphism cards, gradient accents, smooth animations,
  dark/light mode toggle, fully responsive (desktop/tablet/mobile).
- **Offline Fallback** — if watsonx.ai isn't configured/reachable, the app still
  works end-to-end using a deterministic offline roadmap generator.
- **Secure by design** — all credentials loaded from environment variables /
  Streamlit secrets, never hard-coded or logged.

---

## 🏗️ Architecture

```
ai_career_pathway/
├── app.py                     # Streamlit entrypoint & page router
├── config.py                  # Secure env/secrets loader (watsonx.ai config)
├── agent_instructions.py      # 🔧 Customize agent persona/tone/rules here
├── requirements.txt
├── .env.example                # Template for local credentials
├── .streamlit/
│   └── config.toml            # Streamlit theme
├── backend/
│   ├── watsonx_client.py      # IBM watsonx.ai REST client (IAM auth, retries)
│   ├── roadmap_engine.py      # Prompt building, JSON parsing, offline fallback
│   ├── skill_gap.py           # Skill-gap normalization & scoring
│   ├── pdf_report.py          # PDF report generation (ReportLab)
│   └── logger_setup.py        # Centralized logging
├── frontend/
│   ├── styles.py              # Design system / custom CSS (dark & light)
│   ├── components.py          # Reusable UI components
│   └── charts.py              # Themed Plotly chart builders
└── utils/
    └── validators.py          # Form input validation
```

**Design principles:** modular separation of concerns (backend vs. frontend
vs. config), reusable components, typed dataclasses for the domain model,
defensive error handling at every network boundary, and a graceful offline
fallback so the app is always demonstrable.

---

## 🚀 Quick Start (Local)

### 1. Clone & install

```bash
git clone https://github.com/<your-username>/ai-career-learning-pathway.git
cd ai-career-learning-pathway
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure your credentials

```bash
cp .env.example .env
```

Edit `.env` and fill in your IBM watsonx.ai details:

```dotenv
WATSONX_API_KEY=your_ibm_cloud_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct
WATSONX_API_VERSION=2024-05-01
APP_ENV=development
```

> Where to find these:
> - **API Key**: [IBM Cloud → Manage → Access (IAM) → API Keys](https://cloud.ibm.com/iam/apikeys)
> - **Project ID**: watsonx.ai → your Project → *Manage* tab
> - **Region URL**: matches the region your watsonx.ai project lives in
> - **Model ID**: any Granite (or other) foundation model available in your project

### 3. Run the app

```bash
streamlit run app.py
```

Visit `http://localhost:8501`.

> **No watsonx.ai credentials yet?** The app still runs — it automatically
> falls back to an offline demo roadmap generator so you can explore the
> full UI immediately.

---

## 🔧 Customizing the AI Agent

Open **`agent_instructions.py`**. Every aspect of the agent's behavior is a
plain Python string/dict you can edit directly:

| Section | Purpose |
|---|---|
| `PERSONA` | Who the agent is |
| `TEACHING_STYLE` | How it explains concepts |
| `TONE` | Emotional register of its writing |
| `ROADMAP_STYLE` | Structure/format of generated roadmaps |
| `DOMAIN_SPECIALIZATION` | Per-domain emphasis (add new domains here) |
| `SAFETY_RULES` | Hard constraints the agent must always follow |
| `BEGINNER_GUIDANCE` | Extra scaffolding for beginner students |
| `OUTPUT_SCHEMA_HINT` | The JSON contract the model must return |

No other file needs to change to retune the mentor's behavior.

---

## 🔐 Security Notes

- Secrets are **only** read from environment variables / `.env` (local) or
  Streamlit `secrets.toml` (cloud) — never hard-coded, never logged.
- `.env` is git-ignored by default; only `.env.example` (with placeholders)
  is committed.
- IAM tokens are cached in-memory and refreshed automatically before expiry.
- All external API calls are wrapped in typed exceptions and retried with
  exponential backoff on transient network errors.

---

## ☁️ Deployment

### Deploy to Streamlit Community Cloud

1. Push this repository to GitHub (see below).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo, branch, and set **Main file path** to `app.py`.
4. Under **Advanced settings → Secrets**, paste:
   ```toml
   WATSONX_API_KEY = "your_ibm_cloud_api_key_here"
   WATSONX_PROJECT_ID = "your_watsonx_project_id_here"
   WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
   WATSONX_MODEL_ID = "ibm/granite-3-8b-instruct"
   WATSONX_API_VERSION = "2024-05-01"
   APP_ENV = "production"
   ```
5. Click **Deploy**. Streamlit Cloud installs `requirements.txt` automatically.

### Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: AI Career Learning Pathway"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-career-learning-pathway.git
git push -u origin main
```

> `.env` is git-ignored — double-check it never gets committed. Only
> `.env.example` should be in version control.

### Alternative: IBM Cloud Code Engine / Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t ai-career-pathway .
docker run -p 8501:8501 --env-file .env ai-career-pathway
```

---

## 🧪 Tech Stack

- **Frontend/App**: Streamlit, streamlit-option-menu, custom CSS design system
- **AI**: IBM watsonx.ai REST API, IBM Granite foundation models
- **Charts**: Plotly
- **PDF Generation**: ReportLab
- **Validation/Config**: python-dotenv, dataclasses
- **Resilience**: tenacity (retries), structured logging

---

## 📄 License

MIT — free to use, modify, and deploy for personal or commercial projects.

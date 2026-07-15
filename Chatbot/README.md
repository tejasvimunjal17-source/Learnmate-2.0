# 🎓 LearnMate AI Assistant

A standalone Streamlit application whose **only purpose** is to host and
display the **IBM watsonx Orchestrate** chatbot inside a premium, modern,
fully responsive UI.

> This app is intentionally separate from the main **LearnMate AI Career
> Learning Pathway** application. It contains no login/registration, no
> sidebar, and no business logic — it is a pure chatbot host page.

---

## ✨ Features

- Full-screen IBM watsonx Orchestrate chatbot via `streamlit.components.v1.html()`
- Gradient background with soft radial glow accents
- Glassmorphism hero, chat, and footer cards
- Hover animations on all cards/badges
- CSS-only loading spinner while the chatbot widget boots
- Streamlit's default menu, header, footer, and sidebar are hidden
- Fully responsive: mobile, tablet, and desktop
- Zero external CSS/JS files — everything is inline in `app.py`
- Zero extra Python dependencies — `streamlit` only

---

## 📁 Project Structure

```
learnmate-ai-assistant/
│
├── app.py                     # Main Streamlit application (UI + chatbot embed)
├── requirements.txt           # Python dependencies (streamlit only)
├── README.md                  # This file
│
└── .streamlit/
    └── config.toml            # Streamlit theme + server configuration
```

Place the files on disk exactly in this layout — `config.toml` **must**
live inside a folder literally named `.streamlit` at the project root,
sitting next to `app.py`. Streamlit auto-detects this folder; no extra
configuration is required.

```
your-repo/
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

---

## ▶️ Run Locally

```bash
# 1. Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install the single dependency
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## ☁️ Deploying to Streamlit Community Cloud

1. **Push the project to GitHub**
   - Create a new GitHub repository (public or private).
   - Push the folder exactly as structured above, including the
     `.streamlit/config.toml` file — make sure `.streamlit` is committed
     (some `.gitignore` templates hide dot-folders by accident).

   ```bash
   git init
   git add .
   git commit -m "Initial commit: LearnMate AI Assistant"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```

2. **Create the app on Streamlit Community Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io) and sign in
     with GitHub.
   - Click **"New app"**.
   - Select your repository, the branch (`main`), and the entry-point
     file: `app.py`.

3. **Deploy**
   - Click **"Deploy"**. Streamlit Cloud will:
     - Read `requirements.txt` and install `streamlit`.
     - Apply the theme/server settings from `.streamlit/config.toml`.
     - Launch `app.py`.
   - The build takes a minute or two; you'll get a public URL like
     `https://<your-app-name>.streamlit.app`.

4. **Verify the chatbot loads**
   - Open the deployed URL.
   - Confirm the hero section renders, the loading spinner briefly
     appears, and the IBM watsonx Orchestrate chat widget loads beneath
     the header.
   - Test on desktop, tablet width, and mobile width (or your browser's
     device toolbar) to confirm responsiveness.

5. **Updating the app**
   - Any `git push` to the connected branch triggers an automatic
     redeploy on Streamlit Community Cloud — no manual steps needed.

---

## 🔒 Notes on the watsonx Orchestrate Embed

The `wxOConfiguration` object inside `app.py` (orchestration ID, host
URL, CRN, agent ID, and agent environment ID) is embedded **exactly as
provided** and should not be edited unless IBM issues you a new
configuration. The `wxoLoader.js` script tag is the standard IBM
watsonx Orchestrate loader required for the widget to initialize and is
loaded from IBM's CDN (`res.cdn.watson-orchestrate.ibm.com`) inside the
sandboxed HTML component — it does not touch the rest of your Streamlit
app.

---

## © License / Credit

© 2026 LearnMate AI — Powered by IBM watsonx Orchestrate

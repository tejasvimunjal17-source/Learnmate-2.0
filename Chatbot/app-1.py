"""
================================================================================
 LearnMate AI Assistant
 --------------------------------------------------------------------------
 A standalone Streamlit application whose ONLY purpose is to host and
 display the IBM watsonx Orchestrate chatbot widget inside a premium,
 modern, fully responsive UI.

 This app is intentionally decoupled from the main "LearnMate AI Career
 Learning Pathway" application. It contains NO business logic, NO login /
 registration, and NO sidebar — it is a pure chatbot host page.

 Author : Senior Python / Streamlit / watsonx Orchestrate Engineering Team
 Stack  : Python + Streamlit only (no Flask, no React, no Node.js)
================================================================================
"""

# --------------------------------------------------------------------------
# 1. IMPORTS
# --------------------------------------------------------------------------
import streamlit as st
import streamlit.components.v1 as components


# --------------------------------------------------------------------------
# 2. PAGE CONFIGURATION
#    - Wide layout so the chatbot can occupy almost the entire screen
#    - Sidebar is force-collapsed (and hidden entirely via CSS below) since
#      requirements explicitly forbid a sidebar
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="LearnMate AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------------------------------
# 3. CUSTOM CSS
#    Everything is injected inline via st.markdown — no external .css files,
#    per the requirements. This block handles:
#      - Hiding Streamlit's default chrome (menu, header, footer, toolbar)
#      - Hiding the (unused) sidebar entirely
#      - Gradient background for the whole app
#      - Glassmorphism styling for the hero + footer cards
#      - Hover animations
#      - Loading spinner animation
#      - Full responsiveness across mobile / tablet / desktop
# --------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* ---------- Hide native Streamlit chrome ---------- */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden; height: 0; position: fixed;}
    div[data-testid="stDecoration"] {display: none;}
    div[data-testid="stStatusWidget"] {display: none;}
    #stDecoration {display: none;}

    /* ---------- Hide the sidebar completely (no sidebar per spec) ---------- */
    section[data-testid="stSidebar"] {display: none !important;}
    div[data-testid="collapsedControl"] {display: none !important;}

    /* ---------- Remove default Streamlit padding so content fills screen ---------- */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100% !important;
    }

    /* ---------- Global gradient background ---------- */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
        background-size: cover;
    }

    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at 20% 20%, rgba(124, 58, 237, 0.25), transparent 40%),
                    radial-gradient(circle at 80% 0%, rgba(56, 189, 248, 0.20), transparent 40%),
                    radial-gradient(circle at 50% 100%, rgba(236, 72, 153, 0.15), transparent 40%);
        pointer-events: none;
        z-index: 0;
    }

    /* ---------- Global font ---------- */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ---------- Hero / Glassmorphism card ---------- */
    .hero-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(18px) saturate(180%);
        -webkit-backdrop-filter: blur(18px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 24px;
        padding: 2.2rem 1.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.2rem;
        position: relative;
        z-index: 1;
        transition: transform 0.35s ease, box-shadow 0.35s ease;
        animation: fadeInDown 0.8s ease;
    }

    .hero-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 40px rgba(124, 58, 237, 0.35);
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #38bdf8, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: 0.5px;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #e5e7eb;
        margin-top: 0.6rem;
        font-weight: 500;
        opacity: 0.9;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 1rem;
        padding: 0.45rem 1.1rem;
        border-radius: 999px;
        background: rgba(124, 58, 237, 0.25);
        border: 1px solid rgba(167, 139, 250, 0.5);
        color: #ddd6fe;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
    }

    .hero-badge:hover {
        background: rgba(124, 58, 237, 0.45);
        transform: scale(1.05);
    }

    /* ---------- Chat container glass card ---------- */
    .chat-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(14px) saturate(160%);
        -webkit-backdrop-filter: blur(14px) saturate(160%);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 22px;
        padding: 0.6rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.9s ease;
        transition: box-shadow 0.35s ease;
    }

    .chat-card:hover {
        box-shadow: 0 14px 38px rgba(56, 189, 248, 0.25);
    }

    /* ---------- Loading animation shown while the widget boots ---------- */
    .loader-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem 1rem;
        color: #e5e7eb;
    }

    .spinner {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        border: 4px solid rgba(255, 255, 255, 0.15);
        border-top-color: #a78bfa;
        border-right-color: #38bdf8;
        animation: spin 0.9s linear infinite;
        margin-bottom: 1rem;
    }

    .loader-text {
        font-size: 0.95rem;
        opacity: 0.85;
        letter-spacing: 0.3px;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-18px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ---------- Footer ---------- */
    .footer-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        text-align: center;
        padding: 0.9rem 1rem;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
        color: #cbd5e1;
        font-size: 0.85rem;
        position: relative;
        z-index: 1;
        transition: transform 0.3s ease;
    }

    .footer-card:hover {
        transform: translateY(-2px);
    }

    .footer-card b {
        color: #f1f5f9;
    }

    /* ---------- Responsive breakpoints ---------- */

    /* Tablet */
    @media (max-width: 992px) {
        .hero-title { font-size: 2.1rem; }
        .hero-subtitle { font-size: 1rem; }
        .block-container { padding-left: 1rem; padding-right: 1rem; }
    }

    /* Mobile */
    @media (max-width: 600px) {
        .hero-title { font-size: 1.5rem; }
        .hero-subtitle { font-size: 0.9rem; }
        .hero-badge { font-size: 0.78rem; padding: 0.35rem 0.8rem; }
        .hero-card { padding: 1.4rem 1rem; border-radius: 18px; }
        .chat-card { border-radius: 16px; padding: 0.4rem; }
        .block-container { padding-left: 0.5rem; padding-right: 0.5rem; }
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# 4. HERO SECTION
#    Glassmorphism card containing the app title, subtitle and a badge.
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">🎓 LearnMate AI Assistant</div>
        <div class="hero-subtitle">Powered by IBM watsonx Orchestrate</div>
        <div class="hero-badge">✨ AI Career Mentor</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------
# 5. CHATBOT SECTION
#    The IBM watsonx Orchestrate embed code is rendered here using
#    components.v1.html(). A CSS-only loading spinner is shown first and is
#    automatically hidden the moment the watsonx widget script finishes
#    loading, giving the user visual feedback while the external widget
#    initializes.
#
#    IMPORTANT: The wxOConfiguration object below (orchestrationID,
#    hostURL, deploymentPlatform, crn, agentId, agentEnvironmentId) is
#    copied EXACTLY as provided — no IDs or URLs have been modified.
#    The wxoLoader.js <script> tag is the standard IBM watsonx Orchestrate
#    loader that must accompany this configuration for the widget to boot.
# --------------------------------------------------------------------------

# Chat widget occupies almost the full viewport height.
CHATBOT_HEIGHT = 780  # pixels; container itself is also responsive (see HTML/CSS below)

WATSONX_EMBED_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
        /* Reset so the widget's own container can fill 100% of the iframe */
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            background: transparent;
            overflow: hidden;
        }

        /* Loader shown until the watsonx Orchestrate script has loaded */
        #wxo-loader {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            width: 100%;
            font-family: 'Segoe UI', sans-serif;
            color: #e5e7eb;
            background: transparent;
        }

        #wxo-loader .spinner {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 4px solid rgba(255, 255, 255, 0.15);
            border-top-color: #a78bfa;
            border-right-color: #38bdf8;
            animation: wxo-spin 0.9s linear infinite;
            margin-bottom: 1rem;
        }

        @keyframes wxo-spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

    <!-- Loading indicator, hidden automatically once the widget mounts -->
    <div id="wxo-loader">
        <div class="spinner"></div>
        <div>Loading your AI Career Mentor…</div>
    </div>

    <script>
        // ================================================================
        // IBM watsonx Orchestrate configuration
        // Copied exactly as supplied — DO NOT modify any IDs or URLs.
        // ================================================================
        window.wxOConfiguration = {
            orchestrationID: "fbf4ce62fa4b472d835ac9afb3ef3200_e7ad8616-b148-4169-9213-0413e10cac69",
            hostURL: "https://au-syd.watson-orchestrate.cloud.ibm.com",
            deploymentPlatform: "ibmcloud",
            crn: "crn:v1:bluemix:public:watsonx-orchestrate:au-syd:a/fbf4ce62fa4b472d835ac9afb3ef3200:e7ad8616-b148-4169-9213-0413e10cac69::",
            chatOptions: {
                agentId: "87fe3ad0-fb0d-4aca-8f7a-78179712c02c",
                agentEnvironmentId: "b2f40f9b-452b-43f3-b94c-ec90ca6b39f9"
            },
            onLoad: function (instance) {
                // Once the widget instance is ready, remove the loader
                var loader = document.getElementById('wxo-loader');
                if (loader) { loader.style.display = 'none'; }
                instance.render();
            }
        };
    </script>

    <script>
        // Fallback: hide the loader after the external script fires 'load',
        // even if onLoad above is not invoked by the widget for any reason.
        function hideLoaderFallback() {
            setTimeout(function () {
                var loader = document.getElementById('wxo-loader');
                if (loader) { loader.style.display = 'none'; }
            }, 4000);
        }
    </script>

    <!-- IBM watsonx Orchestrate loader script -->
    <script
        src="https://res.cdn.watson-orchestrate.ibm.com/wxoLoader.js"
        onload="wxoLoader.init(); hideLoaderFallback();">
    </script>

</body>
</html>
"""

# Wrap the chatbot iframe in a glassmorphism card for visual consistency
st.markdown('<div class="chat-card">', unsafe_allow_html=True)
components.html(WATSONX_EMBED_HTML, height=CHATBOT_HEIGHT, scrolling=True)
st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------------------------------
# 6. FOOTER
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer-card">
        © 2026 LearnMate AI <br>
        <b>Powered by IBM watsonx Orchestrate</b>
    </div>
    """,
    unsafe_allow_html=True,
)

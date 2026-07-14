"""
app.py
--------
AI Career Learning Pathway - main Streamlit entrypoint.

Run locally:
    streamlit run app.py

See README.md for full setup, environment configuration, and deployment
instructions (Streamlit Community Cloud + GitHub).
"""

from __future__ import annotations

import streamlit as st
from streamlit_option_menu import option_menu

from config import CONFIG
from agent_instructions import DOMAIN_SPECIALIZATION
from backend.logger_setup import get_logger
from backend.watsonx_client import watsonx_client, WatsonxError
from backend.roadmap_engine import StudentProfile, generate_roadmap
from backend.skill_gap import normalize_skill_gaps, overall_readiness_percent
from backend.pdf_report import build_pdf_report
from utils.validators import validate_profile

from frontend.styles import inject_css
from frontend.components import (
    hero, metric_card, glass_card_open, glass_card_close, progress_bar,
    pill_row, milestone_node, skill_gap_row, empty_state,
)
from frontend.charts import readiness_gauge, skill_gap_bar, weekly_effort_line, progress_donut

logger = get_logger(__name__)

DOMAINS = sorted(DOMAIN_SPECIALIZATION.keys())
LEVELS = ["Beginner", "Intermediate", "Advanced"]
LEARNING_STYLES = ["Video Lectures", "Reading / Docs", "Hands-on Projects", "Mixed / Balanced"]

# ----------------------------------------------------------------------
# Page config (must be first Streamlit call)
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="AI Career Learning Pathway",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Session state defaults
# ----------------------------------------------------------------------
DEFAULTS = {
    "dark_mode": True,
    "profile": None,
    "roadmap": None,
    "completed_weeks": set(),
    "page": "Home",
}
for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)

inject_css(dark_mode=st.session_state["dark_mode"])


# ----------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        "<h2 class='pathway-display' style='margin-bottom:0;'>🧭 Career Pathway</h2>"
        "<p class='muted' style='margin-top:2px;'>AI Mentor powered by IBM Granite</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    page = option_menu(
        menu_title=None,
        options=[
            "Home",
            "Profile",
            "AI Roadmap",
            "Skill Gap",
            "Courses & Certs",
            "Progress Tracker",
            "Dashboard",
        ],
        icons=[
            "house",
            "person-badge",
            "signpost-split",
            "bar-chart-steps",
            "mortarboard",
            "check2-square",
            "grid-1x2",
        ],
        default_index=[
            "Home",
            "Profile",
            "AI Roadmap",
            "Skill Gap",
            "Courses & Certs",
            "Progress Tracker",
            "Dashboard",
        ].index(st.session_state["page"]),
        styles={
            "container": {
                "padding": "0",
                "background-color": "transparent",
            },
            "icon": {
                "color": "#7C5CFF",
                "font-size": "16px",
            },
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "2px 0",
                "border-radius": "10px",
            },
            "nav-link-selected": {
                "background": "linear-gradient(120deg, #7C5CFF, #22D3B0)",
                "color": "white",
            },
        },
    )

    #  Indented correctly with 4 spaces inside the 'with' block
    st.session_state["page"] = page

    st.markdown("---")
    dark = st.toggle("🌙 Dark Mode", value=st.session_state["dark_mode"])
    if dark != st.session_state["dark_mode"]:
        st.session_state["dark_mode"] = dark
        st.rerun()

    st.markdown("---")
    status_ok = CONFIG.is_configured
    status_label = "🟢 watsonx.ai configured" if status_ok else "🟡 Offline demo mode"
    st.caption(status_label)
    if not status_ok:
        st.caption(
            "Add WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL and "
            "WATSONX_MODEL_ID to your .env file to enable live AI generation."
        )


# ----------------------------------------------------------------------
# PAGE: Home
# ----------------------------------------------------------------------
def render_home_page() -> None:
    hero(
    "Welcome",
    "Your AI Career Mentor",
    "Build personalized learning roadmaps using IBM Granite AI."
)

st.markdown("")

col1, col2 = st.columns([1.2,1])

with col1:

    st.markdown("""
### 🚀 Learn Smarter

Generate:

- AI Career Roadmap
- Skill Gap Analysis
- Weekly Learning Plan
- Project Recommendations
- Course Suggestions
- Certification Guide

""")

    if st.button("🚀 Start Your Journey", use_container_width=True):
        st.session_state["page"] = "Profile"
        st.rerun()

with col2:

    st.info(
        """
🤖 IBM Granite AI

✔ Personalized Learning

✔ Career Guidance

✔ Weekly Roadmaps

✔ PDF Reports

✔ Progress Dashboard
"""
    )
    # Home page code goes here

# ----------------------------------------------------------------------
# PAGE: Profile
# ----------------------------------------------------------------------
def render_profile_page() -> None:
    hero(
        "Step 1 of 3",
        "Tell us about you",
        "Your AI Career Mentor uses this profile to design a roadmap tailored "
        "exactly to your goal, pace, and starting point.",
    )

    with st.form("profile_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name *", placeholder="e.g. Aisha Khan")
            career_goal = st.text_input(
                "Career Goal *", placeholder="e.g. Become a Machine Learning Engineer"
            )
            current_level = st.selectbox("Current Level *", LEVELS)
            study_hours = st.number_input(
                "Study Hours per Week *", min_value=1, max_value=100, value=10, step=1
            )
        with c2:
            preferred_domain = st.selectbox("Preferred Domain *", DOMAINS)
            learning_preference = st.selectbox("Preferred Learning Style *", LEARNING_STYLES)
            existing_skills_raw = st.text_area(
                "Existing Skills (comma-separated)",
                placeholder="e.g. Python, Excel, HTML, SQL",
                height=100,
            )

        submitted = st.form_submit_button("🚀 Generate My Roadmap", use_container_width=True)

    if submitted:
        existing_skills = [s.strip() for s in existing_skills_raw.split(",") if s.strip()]
        errors = validate_profile(
            name, career_goal, current_level, study_hours,
            preferred_domain, learning_preference, existing_skills,
        )
        if errors:
            for e in errors:
                st.error(e)
            return

        profile = StudentProfile(
            name=name.strip(),
            career_goal=career_goal.strip(),
            current_level=current_level,
            study_hours_per_week=int(study_hours),
            preferred_domain=preferred_domain,
            learning_preference=learning_preference,
            existing_skills=existing_skills,
        )
        st.session_state["profile"] = profile

        with st.spinner("🧠 Your AI Career Mentor is designing your roadmap..."):
            try:
                roadmap = generate_roadmap(profile)
                st.session_state["roadmap"] = roadmap
                st.session_state["completed_weeks"] = set()
                logger.info("Roadmap successfully generated for %s", profile.name)
            except Exception as exc:  # noqa: BLE001 - surfaced to user safely
                logger.exception("Unexpected error generating roadmap")
                st.error(f"Something went wrong while generating your roadmap: {exc}")
                return

        st.success(f"✅ Roadmap generated for **{profile.name}**! Open **AI Roadmap** from the sidebar.")
        st.balloons()


# ----------------------------------------------------------------------
# PAGE: AI Roadmap
# ----------------------------------------------------------------------
def render_roadmap_page() -> None:
    profile: StudentProfile | None = st.session_state["profile"]
    roadmap = st.session_state["roadmap"]

    if not profile or not roadmap:
        empty_state("🧭", "No roadmap yet. Fill out your profile first to generate a personalized pathway.")
        return

    domain_display = profile.preferred_domain.title()
    hero(
        "AI-Generated Pathway",
        f"{profile.name}'s Roadmap to {profile.career_goal}",
        f"Domain: **{domain_display}** &bull; Level: {profile.current_level} &bull; "
        f"{profile.study_hours_per_week} hrs/week &bull; "
        f"~{roadmap.get('estimated_duration_weeks', '-')} weeks",
    )

    if roadmap.get("_source", "").startswith("offline"):
        st.warning(
            "⚠️ Shown in **offline demo mode** because watsonx.ai wasn't reachable "
            f"({roadmap.get('_fallback_reason', 'not configured')}). "
            "Configure your `.env` for fully AI-personalized roadmaps."
        )

    glass_card_open("📋 Overview")
    st.write(roadmap.get("summary", ""))
    glass_card_close()

    st.markdown("### 🛤️ Weekly Milestones")
    for m in roadmap.get("weekly_milestones", []):
        glass_card_open()
        milestone_node(m)
        glass_card_close()

    if roadmap.get("capstone_project"):
        glass_card_open("🏆 Capstone Project")
        st.write(roadmap["capstone_project"])
        glass_card_close()

    # PDF export
    st.markdown("### 📥 Export")
    try:
        pdf_bytes = build_pdf_report(
            profile={
                "name": profile.name,
                "career_goal": profile.career_goal,
                "current_level": profile.current_level,
                "study_hours_per_week": profile.study_hours_per_week,
                "preferred_domain": domain_display,
                "learning_preference": profile.learning_preference,
                "existing_skills": profile.existing_skills,
            },
            roadmap=roadmap,
        )
        st.download_button(
            "⬇️ Download Roadmap as PDF",
            data=pdf_bytes,
            file_name=f"{profile.name.replace(' ', '_')}_career_roadmap.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception:
        logger.exception("PDF generation failed")
        st.error("Couldn't generate the PDF report right now. Please try again.")


# ----------------------------------------------------------------------
# PAGE: Skill Gap
# ----------------------------------------------------------------------
def render_skill_gap_page() -> None:
    roadmap = st.session_state["roadmap"]
    profile = st.session_state["profile"]
    if not roadmap:
        empty_state("📊", "Generate your roadmap first to see your skill-gap analysis.")
        return

    domain_display = profile.preferred_domain.title() if profile else ""
    hero("Skill Gap Analysis", f"Where You Stand in {domain_display}",
         "A side-by-side look at your current skill levels vs. what your target role requires.")

    gaps = normalize_skill_gaps(roadmap.get("skill_gap_analysis", []))
    if not gaps:
        empty_state("✅", "No skill gaps identified yet.")
        return

    readiness = overall_readiness_percent(roadmap.get("skill_gap_analysis", []))
    c1, c2 = st.columns([1, 2])
    with c1:
        st.plotly_chart(readiness_gauge(readiness, st.session_state["dark_mode"]), use_container_width=True)
    with c2:
        st.plotly_chart(skill_gap_bar(gaps, st.session_state["dark_mode"]), use_container_width=True)

    glass_card_open("Detailed Breakdown")
    hc1, hc2, hc3, hc4 = st.columns([3, 2, 2, 1.4])
    hc1.markdown("**Skill**")
    hc2.markdown("**Current**")
    hc3.markdown("**Required**")
    hc4.markdown("**Priority**")
    st.markdown("<hr style='margin:4px 0; opacity:0.15;'>", unsafe_allow_html=True)
    for g in gaps:
        skill_gap_row(g)
    glass_card_close()


# ----------------------------------------------------------------------
# PAGE: Courses & Certifications
# ----------------------------------------------------------------------
def render_courses_page() -> None:
    roadmap = st.session_state["roadmap"]
    if not roadmap:
        empty_state("🎓", "Generate your roadmap first to see course & certification recommendations.")
        return

    hero("Course Recommendation Dashboard", "Courses & Certifications",
         "Curated learning resources mapped to each stage of your roadmap.")

    st.markdown("### 📚 Courses by Week")
    milestones = roadmap.get("weekly_milestones", [])
    cols = st.columns(3)
    for i, m in enumerate(milestones):
        with cols[i % 3]:
            glass_card_open(f"Week {m.get('week')}: {m.get('title', '')}")
            for c in m.get("recommended_courses", []):
                st.markdown(f"- {c}")
            glass_card_close()

    st.markdown("### 🏅 Recommended Certifications")
    certs = roadmap.get("certifications", [])
    ccols = st.columns(min(3, max(1, len(certs))) or 1)
    for i, cert in enumerate(certs):
        with ccols[i % len(ccols)]:
            metric_card("Certification", cert)


# ----------------------------------------------------------------------
# PAGE: Progress Tracker
# ----------------------------------------------------------------------
def render_progress_page() -> None:
    roadmap = st.session_state["roadmap"]
    profile = st.session_state["profile"]
    if not roadmap:
        empty_state("✅", "Generate your roadmap first to start tracking progress.")
        return

    hero("Progress Tracker", f"{profile.name}'s Journey" if profile else "Your Journey",
         "Check off each week as you complete it - your dashboard updates automatically.")

    milestones = roadmap.get("weekly_milestones", [])
    total = len(milestones)
    completed = st.session_state["completed_weeks"]

    progress_bar(round((len(completed) / total) * 100) if total else 0, "Overall Roadmap Progress")
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    for m in milestones:
        week = m.get("week")
        checked = week in completed
        new_val = st.checkbox(
            f"Week {week}: {m.get('title', '')}", value=checked, key=f"week_check_{week}"
        )
        if new_val and week not in completed:
            completed.add(week)
        elif not new_val and week in completed:
            completed.discard(week)

    st.session_state["completed_weeks"] = completed


# ----------------------------------------------------------------------
# PAGE: Dashboard
# ----------------------------------------------------------------------
def render_dashboard_page() -> None:
    roadmap = st.session_state["roadmap"]
    profile = st.session_state["profile"]
    if not roadmap or not profile:
        empty_state("📈", "Generate your roadmap first to unlock your interactive dashboard.")
        return

    domain_display = profile.preferred_domain.title()
    hero("Interactive Dashboard", f"{domain_display} Career Overview",
         f"A bird's-eye view of {profile.name}'s roadmap, pace, and readiness.")

    milestones = roadmap.get("weekly_milestones", [])
    total_weeks = roadmap.get("estimated_duration_weeks", len(milestones) or 1)
    completed = len(st.session_state["completed_weeks"])
    readiness = overall_readiness_percent(roadmap.get("skill_gap_analysis", []))
    total_hours = total_weeks * profile.study_hours_per_week

    m1, m2, m3, m4 = st.columns(4)
    metric_card("Target Domain", domain_display, m1)
    metric_card("Roadmap Duration", f"{total_weeks} wks", m2)
    metric_card("Total Study Hours", f"{total_hours} hrs", m3)
    metric_card("Weeks Completed", f"{completed}/{len(milestones)}", m4)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(progress_donut(completed, len(milestones), st.session_state["dark_mode"]), use_container_width=True)
    with c2:
        st.plotly_chart(readiness_gauge(readiness, st.session_state["dark_mode"]), use_container_width=True)

    st.plotly_chart(
        weekly_effort_line(total_weeks, profile.study_hours_per_week, st.session_state["dark_mode"]),
        use_container_width=True,
    )

    gaps = normalize_skill_gaps(roadmap.get("skill_gap_analysis", []))
    if gaps:
        st.plotly_chart(skill_gap_bar(gaps, st.session_state["dark_mode"]), use_container_width=True)


# ----------------------------------------------------------------------
# Router
# ----------------------------------------------------------------------
PAGES = {
    "Home": render_home_page,
    "Profile": render_profile_page,
    "AI Roadmap": render_roadmap_page,
    "Skill Gap": render_skill_gap_page,
    "Courses & Certs": render_courses_page,
    "Progress Tracker": render_progress_page,
    "Dashboard": render_dashboard_page,
}

try:
    PAGES[st.session_state["page"]]()
except Exception as exc:  # noqa: BLE001 - top-level safety net
    logger.exception("Unhandled error rendering page '%s'", st.session_state["page"])
    st.error(f"An unexpected error occurred: {exc}")
    st.caption("Please refresh the page or check the logs for more details.")

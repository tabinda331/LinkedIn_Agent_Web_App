# app.py
# ============================================================
# MULTI-AGENT LINKEDIN CONTENT STUDIO (WEB UI – DeepSeek)
# ============================================================

import os
import requests
import html
from datetime import datetime
from typing import List, Dict

import pandas as pd
import streamlit as st

# ============================================================
# CONFIG
# ============================================================

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"  # change if needed


if not DEEPSEEK_API_KEY:
    st.warning(
        "⚠️ Environment variable DEEPSEEK_API_KEY is not set.\n\n"
        "Set it before running, e.g. on Windows:\n"
        "  set DEEPSEEK_API_KEY=your_key_here\n"
        "or on Linux/Mac:\n"
        "  export DEEPSEEK_API_KEY=your_key_here"
    )


# ============================================================
# LLM WRAPPER
# ============================================================

def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """Call DeepSeek chat completion."""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    resp = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


# ============================================================
# AGENTS (same logic as notebook, simplified)
# ============================================================

def generate_auto_trending_topics(n: int, niche: str) -> List[str]:
    niche_part = "" if niche == "Mixed / General" else f"\nFocus niche: {niche}\n"
    system_prompt = f"""
You generate ONLY a numbered list of trending LinkedIn topics.

STRICT RULES:
- Max 18 words each
- No explanations
- No markdown
- Output must be:
1. Topic
2. Topic
...
{niche_part}
"""
    user_prompt = f"Generate {n} trending LinkedIn topics."

    raw = call_llm(system_prompt, user_prompt, temperature=0.9)
    topics: List[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if "." in line[:4]:
            line = line.split(".", 1)[1].strip()
        if line:
            topics.append(line)
    return topics[:n]


def build_writer_system_prompt(language: str, brand_voice: str) -> str:
    LANG = {
        "English": "Write in English.",
        "Urdu": "Write in natural Urdu.",
        "Hindi": "Write in natural Hindi.",
        "Arabic": "Write in Modern Standard Arabic.",
        "Chinese": "Write in simplified Chinese.",
        "Japanese": "Write in Japanese.",
        "Spanish": "Write in Spanish.",
        "French": "Write in French.",
    }.get(language, "Write in English.")

    brand = ""
    if brand_voice.strip():
        brand = f"""
Match this tone:
--- START ---
{brand_voice}
--- END ---
"""

    return f"""
You output EXACT LinkedIn posts in this format:

LinkedIn Post:
[post]

Suggested Posting Times:
Primary: [day, time, timezone or “global audience”] – [reason]
Backup: [day, time, timezone or “global audience”] – [reason]
------------------------------------------------------------

Rules:
- 120–230 words
- Hook in 1–2 lines
- Short paragraphs
- 1–3 emojis allowed
- 6–10 hashtags at end
- No markdown, no explanations
- {LANG}
{brand}
"""


def writer_agent_create_post(topic: str, language: str, brand_voice: str) -> str:
    system_prompt = build_writer_system_prompt(language, brand_voice)
    user_prompt = f"Topic: {topic}\nCreate one LinkedIn post package that follows ALL rules and exact format."
    return call_llm(system_prompt, user_prompt, temperature=0.7)


def render_linkedin_preview(full_post_text: str) -> str:
    """Return HTML preview similar to LinkedIn feed card."""
    post_section = full_post_text
    if "Suggested Posting Times:" in post_section:
        post_section = post_section.split("Suggested Posting Times:", 1)[0]
    if "LinkedIn Post:" in post_section:
        post_section = post_section.split("LinkedIn Post:", 1)[1].strip()

    escaped = html.escape(post_section)
    paragraphs = [p.strip() for p in escaped.split("\n\n") if p.strip()]
    body_html = "<br>".join(p.replace("\n", "<br>") for p in paragraphs)

    card_html = f"""
    <div style="border:1px solid #ddd;border-radius:10px;padding:12px;
                background:#f9fafb;font-family:system-ui,-apple-system,
                BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:14px;
                line-height:1.5; max-width:680px;">
      <div style="display:flex;align-items:center;margin-bottom:8px;">
        <div style="width:32px;height:32px;border-radius:50%;
                    background:#ccc;margin-right:8px;"></div>
        <div>
          <div style="font-weight:600;">Your Profile · LinkedIn</div>
          <div style="font-size:12px;color:#555;">Following · 1h · 🌐</div>
        </div>
      </div>
      <div style="margin-top:4px;">{body_html}</div>
    </div>
    """
    return card_html


# ============================================================
# APP STATE (in-memory)
# ============================================================

if "history" not in st.session_state:
    st.session_state.history: List[Dict] = []  # each item: {time, topic, mode, niche, language, post}


# ============================================================
# STREAMLIT UI
# ============================================================

st.set_page_config(
    page_title="Multi-Agent LinkedIn Content Studio",
    page_icon="💼",
    layout="wide",
)

st.title("💼 Multi-Agent LinkedIn Content Studio (DeepSeek Web UI)")

st.caption("Powered by DeepSeek · Auto topics · Multi-language · Brand voice · Web preview")


# Sidebar controls
with st.sidebar:
    st.header("⚙️ Settings")

    mode = st.selectbox(
        "Mode",
        ["Auto Trending (No Input)", "Single Topic (Manual)"],
        index=0,
    )

    topic_input = st.text_input(
        "Topic (used only in Single Topic mode)",
        value="Why getting jobs is harder day by day",
    )

    num_posts = st.slider("Number of posts", min_value=1, max_value=10, value=3, step=1)

    niche = st.selectbox(
        "Niche",
        [
            "Mixed / General",
            "AI & Automation",
            "Business & Startups",
            "Career & Jobs",
            "Freelancing & Clients",
            "Leadership & Management",
            "Personal Branding & Content",
            "Productivity & Focus",
        ],
        index=0,
    )

    language = st.selectbox(
        "Language",
        ["English", "Urdu", "Hindi", "Arabic", "Chinese", "Japanese", "Spanish", "French"],
        index=0,
    )

    brand_voice = st.text_area(
        "Brand voice (optional)",
        help="Paste 1–3 of your LinkedIn-style posts to train tone.",
        height=120,
    )

    st.markdown("---")
    st.write("When ready:")
    do_generate = st.button("🚀 Generate Posts", use_container_width=True)


# Main layout: columns
col_left, col_right = st.columns([1.2, 1.3])

with col_left:
    st.subheader("📌 Topics")
    topics_box = st.empty()

    st.subheader("📝 Raw Output (All Posts)")
    posts_box = st.empty()

with col_right:
    st.subheader("👀 LinkedIn-style Preview (Latest Post)")
    preview_box = st.empty()

    st.subheader("📜 History & Export")
    hist_box = st.empty()
    export_col1, export_col2 = st.columns(2)
    with export_col1:
        export_csv_btn = st.button("💾 Download History CSV")
    with export_col2:
        clear_hist_btn = st.button("🧹 Clear History")


# ============================================================
# GENERATION LOGIC
# ============================================================

generated_posts: List[str] = []
used_topics: List[str] = []

if do_generate and DEEPSEEK_API_KEY:
    with st.spinner("Generating content with DeepSeek..."):
        # 1) topics
        if mode == "Auto Trending (No Input)":
            used_topics = generate_auto_trending_topics(num_posts, niche)
        else:
            base_topic = topic_input.strip() or "Why AI-powered content matters in 2025"
            used_topics = [base_topic] * num_posts

        # show topics immediately
        topics_box.write("\n".join(f"{i+1}. {t}" for i, t in enumerate(used_topics)))

        # 2) posts
        for idx, t in enumerate(used_topics, start=1):
            post_text = writer_agent_create_post(t, language, brand_voice)
            generated_posts.append(post_text)

            # save to history
            st.session_state.history.append(
                {
                    "time": datetime.now().isoformat(timespec="seconds"),
                    "mode": mode,
                    "topic": t,
                    "niche": niche,
                    "language": language,
                    "brand_voice": "yes" if brand_voice.strip() else "no",
                    "post": post_text,
                }
            )

        # display all posts concatenated
        all_posts_text = "\n\n".join(
            f"=== Post {i+1} (Topic: {t}) ===\n{p}"
            for i, (t, p) in enumerate(zip(used_topics, generated_posts))
        )
        posts_box.text_area("Generated Posts", value=all_posts_text, height=350)

        # preview latest
        latest_post = generated_posts[-1] if generated_posts else ""
        if latest_post:
            preview_html = render_linkedin_preview(latest_post)
            preview_box.markdown(preview_html, unsafe_allow_html=True)


# ============================================================
# HISTORY SECTION
# ============================================================

history_df = pd.DataFrame(st.session_state.history) if st.session_state.history else pd.DataFrame()

if not history_df.empty:
    hist_box.dataframe(history_df[["time", "mode", "topic", "niche", "language"]], use_container_width=True)
else:
    hist_box.info("No posts generated yet in this session.")

# Export history
if export_csv_btn:
    if history_df.empty:
        st.warning("No history to export yet.")
    else:
        csv = history_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download CSV",
            data=csv,
            file_name="linkedin_posts_history_web.csv",
            mime="text/csv",
        )

# Clear history
if clear_hist_btn:
    st.session_state.history = []
    st.experimental_rerun()


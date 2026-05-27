import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
from storage.db import get_all, init_db
from scraper.scraper import scrape_policy
from agent.scorer import score_policy
from storage.db import save_result
import time

init_db()

def get_grade(total):
    if total >= 9: return "A"
    elif total >= 7: return "B"
    elif total >= 5: return "C"
    elif total >= 3: return "D"
    else: return "F"

def grade_color(grade):
    return {"A": "green", "B": "blue", "C": "orange", "D": "red", "F": "darkred"}[grade]

st.title("🛡️ EduGuard")
st.caption("Audits EdTech privacy policies and scores them across 5 dimensions — so you don't have to read the fine print.")

st.divider()

with st.sidebar:
    st.header("Audit a new platform")
    name = st.text_input("Platform name")
    urls_input = st.text_area(
        "Privacy policy URLs (one per line)",
        height=150,
        placeholder="https://example.com/privacy\nhttps://example.com/terms"
    )
    run = st.button("Run audit", use_container_width=True)

# --- Audit result ---
if run and name and urls_input:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]
    combined_text = ""

    st.subheader(f"Audit result — {name}")
    progress = st.status("Scraping pages...", expanded=True)

    with progress:
        for url in urls:
            try:
                st.write(f"Scraping `{url}`")
                text = scrape_policy(url)
                combined_text += f"\n\n--- Source: {url} ---\n{text}"
                time.sleep(1)
            except Exception as e:
                st.warning(f"Could not scrape {url}: {e}")
        st.write("Scoring with AI...")

    if combined_text:
        scores = score_policy(combined_text[:4000])
        save_result(name, " | ".join(urls), scores)
        progress.update(label="Done!", state="complete")

        total = int(scores['total'])
        grade = get_grade(total)
        color = grade_color(grade)

        col_grade, col_score = st.columns([1, 3])
        with col_grade:
            st.markdown(f"<div style='text-align:center;padding:16px;background:#f0f0f0;border-radius:12px'>"
                        f"<span style='font-size:64px;font-weight:bold;color:{color}'>{grade}</span>"
                        f"<br><span style='color:gray;font-size:14px'>Grade</span></div>",
                        unsafe_allow_html=True)
        with col_score:
            st.markdown(f"<div style='padding:16px'>"
                        f"<span style='font-size:48px;font-weight:bold;color:{color}'>{total}/10</span>"
                        f"<br><span style='color:gray;font-size:14px'>Overall privacy score</span></div>",
                        unsafe_allow_html=True)

        st.markdown("### Score breakdown")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("C1 — Data Collection", f"{int(scores['C1'])}/2")
        col2.metric("C2 — Third-Party Sharing", f"{int(scores['C2'])}/2")
        col3.metric("C3 — Children & Consent", f"{int(scores['C3'])}/2")
        col4.metric("C4 — AI & Automation", f"{int(scores['C4'])}/2")
        col5.metric("C5 — Accountability", f"{int(scores['C5'])}/2")

        st.markdown("### What each score means")
        rubric = {
            "C1 — Data Collection": [
                "No meaningful description of data collected",
                "Only broad/vague categories (e.g. 'usage data')",
                "Specific data types listed + minimization claim"
            ],
            "C2 — Third-Party Sharing": [
                "Not mentioned",
                "Generic 'trusted partners' with no names",
                "Third parties named or sub-processor list linked"
            ],
            "C3 — Children & Consent": [
                "No engagement with children's data",
                "Law cited but vague, or consent only vaguely mentioned",
                "Law cited + explained + consent process described"
            ],
            "C4 — AI & Automation": [
                "No mention despite visible AI features",
                "Generic 'we personalize' with no specifics",
                "AI features named + model training + decisions described"
            ],
            "C5 — Accountability": [
                "None of the below",
                "Generic privacy email + vague breach language",
                "Named contact + specific breach timeline + SOC2/ISO cert"
            ],
        }
        score_vals = {
            "C1 — Data Collection": scores['C1'],
            "C2 — Third-Party Sharing": scores['C2'],
            "C3 — Children & Consent": scores['C3'],
            "C4 — AI & Automation": scores['C4'],
            "C5 — Accountability": scores['C5'],
        }
        for dim, descriptions in rubric.items():
            val = int(score_vals[dim])
            icon = "🟢" if val == 2 else "🟡" if val == 1 else "🔴"
            with st.expander(f"{icon} {dim}: {val}/2"):
                for i, desc in enumerate(descriptions):
                    prefix = "✅" if i == val else "　"
                    st.markdown(f"{prefix} **{i}** — {desc}")

        if scores.get("flags"):
            st.markdown("### Auditor notes")
            st.info(scores["flags"])

        st.divider()

# --- Leaderboard ---
st.subheader("📊 Leaderboard")
rows = get_all()
if rows:
    df = pd.DataFrame(rows, columns=["Platform","URL","C1","C2","C3","C4","C5","Total","Notes","Audited"])
    df = df.drop_duplicates(subset=["Platform"], keep="last")
    df = df.sort_values("Total", ascending=False).reset_index(drop=True)
    df["Grade"] = df["Total"].apply(get_grade)
    st.dataframe(
        df[["Platform","Grade","C1","C2","C3","C4","C5","Total","Notes"]],
        use_container_width=True
    )
    st.download_button("Export CSV", df.to_csv(index=False), "eduguard_results.csv")

else:
    st.info("No audits yet. Run one from the sidebar.")
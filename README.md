# 🛡️ EduGuard

**Audits EdTech privacy policies and scores them across 5 dimensions**
Built to automate a manual research study that coded privacy policies for 48 EdTech platforms across the US and India.

---

## 📊 Scoring Rubric (C1–C5)

Each platform is scored out of 10, with 2 points per dimension:

| Dimension | What it measures |
|---|---|
| **C1 — Data Collection Scope** | Are specific data types listed? Is there a minimization claim? |
| **C2 — Third-Party Sharing** | Are third parties named? Is a sub-processor list linked? |
| **C3 — Children & Consent** | Is relevant law (COPPA/FERPA/DPDPA) cited and explained? |
| **C4 — AI & Automated Decision-Making** | Are AI features named? Is model training addressed? |
| **C5 — Accountability & Breach Response** | Named contact + breach timeline + governance cert? |

**Grading:** A (9–10) · B (7–8) · C (5–6) · D (3–4) · F (0–2)

---

## 🗂️ Dataset — `Meghna.xlsx`

- Contains hand-coded audit scores for 48 EdTech platforms. All policy documents were sourced from links accessible within 1–2 clicks from each platform's homepage. No login or paywalled content was used. The dataset serves as the seed for the leaderboard and as a ground truth benchmark to validate EduGuard's automated scores against human coding.
---

## 🚀 How to Run

### Prerequisites
- Python 3.11+
- Free [Groq API key](https://console.groq.com) (no billing required)

### Setup

```bash
git clone https://github.com/Meghna19BCE1459/EduGuard.git
cd EduGuard
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
playwright install chromium
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```

### Run

```bash
# Extract platform URLs from dataset
python extract_platforms.py

# Audit all 48 platforms
python run_audit.py

# Launch the UI
streamlit run ui/app.py
```

Open `http://localhost:8501` in your browser.

---

## ⚠️ Limitations

- Some platforms (e.g. Quizlet) block scrapers entirely and must be scored manually
- Only the first ~4,000 characters of policy text are scored due to token limits — very long policies may be partially assessed
- Groq's free tier allows 100,000 tokens/day — auditing all 48 platforms in one run may hit this limit; just wait and re-run failed platforms the next day
- Privacy policies change over time — scores reflect the policy at the time of scraping

---

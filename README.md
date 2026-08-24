# 🏛️ COEP Scopus Live Research Dashboard

An interactive, live institutional bibliometrics and research intelligence dashboard for **COEP (COEP Technological University, Pune / College of Engineering Pune)** powered by the **Elsevier Scopus API** and **Streamlit**.

---

## 📌 Top 10 KPIs at a Glance

| KPI | Description |
| :--- | :--- |
| **Total Scopus Publications** | Total count of all Scopus-indexed research articles & proceedings |
| **Publications – 2026** | Current calendar year research output & growth trajectory |
| **Publications – 2025** | Total research output for the preceding academic year |
| **Total Citations** | Cumulative citation count across all COEP indexed publications |
| **Citations per Publication** | Average citation impact per research paper |
| **Q1 Publications** | Count and percentage of publications in top Quartile 1 journals |
| **International Collaborations** | Share of publications co-authored with international universities |
| **Industry Collaborations** | Publications co-authored with corporate & industrial R&D partners |
| **Active Publishing Faculty** | Count of unique active COEP faculty authors |
| **Publications in Last 30 Days** | Recent publishing velocity over the last month |

---

## 🚀 Key Dashboard Sections

1. **📈 Publication Trends**:
   - Annual publication growth with dual-axis cumulative curve.
   - Monthly publication breakdown for current and recent years.
   - Department-wise publication distribution (Computer, Mechanical, E&TC, Electrical, Civil, Metallurgy, etc.).

2. **🎯 Research Impact**:
   - Total citations and average citations per paper by year.
   - Citations per publication across academic departments.
   - **Highly Cited Papers Leaderboard** with direct DOI resolution.

3. **🌐 Collaboration Dynamics**:
   - Collaboration breakdown (International vs National vs Industry vs Institutional).
   - Top collaborating institutions (IIT Bombay, SPPU, BARC, Purdue, Siemens, etc.).
   - Interactive **Global Choropleth Map** of foreign co-author countries.

4. **🏆 Research Quality**:
   - **Q1 / Q2 / Q3 / Q4 Quartile Distribution** (CiteScore / SJR percentiles).
   - Departmental breakdown by quartile.
   - Scopus CiteScore & SCImago Journal Rank (SJR) distributions.
   - Top 10% High-Impact benchmark indicator.

5. **📰 Live Publication Feed & Searchable Explorer**:
   - Full-text search across titles, authors, departments, journals, and DOIs.
   - Multi-filtering by year, department, quartile, and collaboration type.
   - Card view with Quartile badges, CiteScore, SJR, citations count, and abstract previews.
   - One-click export to **CSV**, **Excel (.xlsx)**, and **BibTeX (.bib)**.

---

## 🛠️ Quick Start & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Scopus API Key
You can either:
- Enter your API Key directly in the **Dashboard Sidebar** under **Scopus API Settings**, OR
- Open `.env` and set your key:
  ```ini
  SCOPUS_API_KEY=your_elsevier_scopus_api_key
  SCOPUS_INST_TOKEN=optional_institutional_token
  ```

### 3. Launch the Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ⚡ Elsevier Scopus API Sync
- Click **"🔄 Sync Live"** in the sidebar to fetch real-time Scopus indexed documents for COEP.
- The dashboard automatically saves and caches the synced data to `data/coep_scopus_cache.json` for rapid subsequent loading without exceeding API rate limits.
- Click **"📥 Benchmark"** at any time to reload the comprehensive baseline dataset.

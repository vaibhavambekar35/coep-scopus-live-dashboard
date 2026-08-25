# COEP Scopus Live Dashboard - Production Release
"""
COEP AI Research Copilot & Intelligence Engine
Provides interactive natural language question answering, executive dossier generation,
and smart analytical querying over COEP Scopus publication dataset.
"""

import os
import json
import requests
import pandas as pd
from typing import Dict, List, Any, Optional

def get_gemini_api_key() -> Optional[str]:
    """Retrieves Gemini API key from environment or Streamlit secrets."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
    return key.strip() if key else None


def call_gemini_api(prompt: str, context: str, api_key: str) -> Optional[str]:
    """Calls Google Gemini REST API with provided prompt and data context."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_instruction = (
            "You are the COEP Research Intelligence AI Copilot for COEP Technological University, Pune (Estd. 1854). "
            "You have access to verified Scopus bibliometric data for COEP faculty and departments. "
            "Provide concise, authoritative, executive-level insights, rankings, data tables, and strategic recommendations. "
            "Always base your answers strictly on the provided Scopus data context. If data is unavailable, state it clearly. "
            "Format responses using clean Markdown with bolding, bullet points, and tables where appropriate."
        )
        
        full_content = f"SYSTEM CONTEXT:\n{context}\n\nUSER QUESTION:\n{prompt}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_content}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1200
            }
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
    except Exception:
        pass
    return None


def generate_data_context(df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
    """Builds a structured contextual summary of the dataset for LLM ingestion."""
    if df.empty:
        return "Dataset is currently empty."
    
    total_pubs = len(df)
    total_cites = int(df["citations"].sum()) if "citations" in df.columns else 0
    cpp = round(total_cites / max(1, total_pubs), 2)
    
    dept_counts = df["department"].value_counts().head(8).to_dict() if "department" in df.columns else {}
    dept_cites = df.groupby("department")["citations"].sum().sort_values(ascending=False).head(8).to_dict() if "department" in df.columns and "citations" in df.columns else {}
    q_counts = df["quartile"].value_counts().to_dict() if "quartile" in df.columns else {}
    
    top_authors = []
    if "author" in df.columns:
        auth_grp = df.groupby("author").agg(pubs=("title", "count"), cites=("citations", "sum")).sort_values("cites", ascending=False).head(10)
        for auth, row in auth_grp.iterrows():
            top_authors.append(f"{auth}: {int(row['pubs'])} papers, {int(row['cites'])} citations")
            
    landmarks = []
    if "citations" in df.columns:
        top_papers = df.sort_values("citations", ascending=False).head(5)
        for _, r in top_papers.iterrows():
            landmarks.append(f"- {r.get('title', 'Unknown')} ({r.get('year', 'N/A')}) in {r.get('journal', 'N/A')} - {int(r.get('citations', 0))} citations [Dept: {r.get('department', 'N/A')}]")

    q1_count = q_counts.get('Q1', 0)
    q1_pct = round(q1_count / max(1, total_pubs) * 100, 1)

    lines = [
        "COEP TECHNOLOGICAL UNIVERSITY - SCOPUS RESEARCH DATASET CONTEXT:",
        f"- Total Indexed Publications: {total_pubs:,}",
        f"- Total Cumulative Citations: {total_cites:,}",
        f"- Citations Per Paper (CPP): {cpp}",
        f"- Q1 Tier Publications: {q1_count:,} ({q1_pct}%)",
        f"- Q2 Tier Publications: {q_counts.get('Q2', 0):,}",
        f"- Q3 Tier Publications: {q_counts.get('Q3', 0):,}",
        f"- Q4 Tier Publications: {q_counts.get('Q4', 0):,}",
        f"- International Collaborations: {kpis.get('intl_collab', 'N/A')}",
        f"- Industry Co-authored: {kpis.get('industry_collab', 'N/A')}",
        "",
        "DEPARTMENT RESEARCH OUTPUT (Top 8):",
        json.dumps(dept_counts, indent=2),
        "",
        "DEPARTMENT CITATION IMPACT (Top 8):",
        json.dumps(dept_cites, indent=2),
        "",
        "TOP CONTRIBUTING FACULTY:",
        "\n".join(top_authors),
        "",
        "LANDMARK HIGHLY CITED RESEARCH:",
        "\n".join(landmarks)
    ]
    return "\n".join(lines)


def run_analytical_copilot(prompt: str, df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
    """
    Intelligent built-in analytical engine that answers natural language research questions
    directly from pandas computations with zero API latency.
    """
    q = prompt.lower().strip()
    
    if df.empty:
        return "⚠️ **No publication data available** for the currently selected filters. Please adjust the year range or department in the sidebar."

    total_pubs = len(df)
    total_cites = int(df["citations"].sum()) if "citations" in df.columns else 0
    cpp = round(total_cites / max(1, total_pubs), 2)
    
    # 1. Accreditation / Executive / NIRF / NAAC Summary
    if any(w in q for w in ["dossier", "executive", "nirf", "naac", "accreditation", "report", "overview", "summary"]):
        return generate_executive_dossier(df, kpis)
    
    # 2. Department Rankings / Leaderboard
    if any(w in q for w in ["department", "dept", "school", "branch", "ranking"]):
        if "department" in df.columns and "citations" in df.columns:
            dept_stats = df.groupby("department").agg(
                pubs=("title", "count"),
                cites=("citations", "sum"),
                q1=("quartile", lambda x: (x == "Q1").sum())
            ).reset_index()
            dept_stats["cpp"] = (dept_stats["cites"] / dept_stats["pubs"]).round(2)
            dept_stats = dept_stats.sort_values("pubs", ascending=False)
            
            top_dept = dept_stats.iloc[0]["department"]
            top_cite_dept = dept_stats.sort_values("cites", ascending=False).iloc[0]["department"]
            top_q1_dept = dept_stats.sort_values("q1", ascending=False).iloc[0]["department"]
            
            table_rows = []
            for i, r in dept_stats.head(10).iterrows():
                table_rows.append(f"| **{r['department']}** | {int(r['pubs']):,} | {int(r['cites']):,} | {r['cpp']} | {int(r['q1']):,} |")
                
            return f"""### 🏛️ Departmental Research Leaderboard & Impact

**Key Takeaways:**
- 🥇 **Highest Volume Department:** **{top_dept}** ({int(dept_stats.iloc[0]['pubs']):,} indexed papers).
- 🌟 **Highest Citation Impact:** **{top_cite_dept}** ({int(dept_stats.sort_values('cites', ascending=False).iloc[0]['cites']):,} total citations).
- 🏆 **Most Q1 High-Impact Papers:** **{top_q1_dept}** ({int(dept_stats.sort_values('q1', ascending=False).iloc[0]['q1']):,} Q1 publications).

| Department / School | Publications | Total Citations | Citations/Paper (CPP) | Q1 Papers |
| :--- | :---: | :---: | :---: | :---: |
""" + "\n".join(table_rows) + f"""

💡 *Recommendation:* Encourage joint interdisciplinary projects between **{top_dept}** and emerging research groups to scale institutional Q1 output.
"""

    # 3. Quality & Quartile Distribution (Q1, Q2, Q3, Q4)
    if any(w in q for w in ["q1", "q2", "q3", "q4", "quartile", "quality", "tier", "impact factor"]):
        if "quartile" in df.columns:
            q_counts = df["quartile"].value_counts()
            q1_c = int(q_counts.get("Q1", 0))
            q2_c = int(q_counts.get("Q2", 0))
            q3_c = int(q_counts.get("Q3", 0))
            q4_c = int(q_counts.get("Q4", 0))
            q1_pct = round(q1_c / max(1, total_pubs) * 100, 1)
            q2_pct = round(q2_c / max(1, total_pubs) * 100, 1)
            
            top_q1_papers = df[df["quartile"] == "Q1"].sort_values("citations", ascending=False).head(3)
            p_list = []
            for _, r in top_q1_papers.iterrows():
                p_list.append(f"- 🏅 **{r.get('title', 'N/A')}** ({r.get('year', 'N/A')}) — *{r.get('journal', 'N/A')}* ({int(r.get('citations', 0))} citations)")

            return f"""### 🏆 Journal Quality & Quartile (Q1–Q4) Analysis

**Quality Distribution:**
- 🥇 **Q1 (Top 25% Journals):** **{q1_c:,}** publications (**{q1_pct}%** of all output)
- 🥈 **Q2 (Top 50% Journals):** **{q2_c:,}** publications (**{q2_pct}%** of all output)
- 🥉 **Q3 & Q4 Journals:** **{q3_c + q4_c:,}** publications

| Tier | Publication Count | Proportion | Strategic Assessment |
| :--- | :---: | :---: | :--- |
| **Q1 (High Impact)** | {q1_c:,} | {q1_pct}% | Excellent institutional core; targeted for global ranking benchmarks |
| **Q2 (Upper Mid)** | {q2_c:,} | {q2_pct}% | Strong pipeline for future Q1 upgrades |
| **Q3 (Lower Mid)** | {q3_c:,} | {round(q3_c/max(1, total_pubs)*100, 1)}% | Solid peer-reviewed foundation |
| **Q4 (Entry Tier)** | {q4_c:,} | {round(q4_c/max(1, total_pubs)*100, 1)}% | Transition opportunities |

**Top Cited Q1 Papers from COEP:**
""" + "\n".join(p_list)

    # 4. Top Authors & Faculty Intelligence
    if any(w in q for w in ["author", "faculty", "professor", "researcher", "scientist", "who"]):
        if "author" in df.columns:
            auth_grp = df.groupby("author").agg(
                pubs=("title", "count"),
                cites=("citations", "sum"),
                dept=("department", "first")
            ).reset_index().sort_values("cites", ascending=False).head(8)
            
            rows = []
            for i, r in auth_grp.iterrows():
                cpp_auth = round(r["cites"] / max(1, r["pubs"]), 1)
                rows.append(f"| **{r['author']}** | {r['dept']} | {int(r['pubs']):,} | {int(r['cites']):,} | {cpp_auth} |")
                
            top_auth = auth_grp.iloc[0]["author"]
            top_pubs_auth = df["author"].value_counts().index[0]
            
            return f"""### 👥 Top Author & Faculty Research Intelligence

**Faculty Highlights:**
- 🌟 **Most Cited Researcher:** **{top_auth}** ({int(auth_grp.iloc[0]['cites']):,} citations)
- 📚 **Highest Volume Contributor:** **{top_pubs_auth}** ({int(df['author'].value_counts().iloc[0]):,} papers)

| Author / Faculty | Primary Department | Papers | Total Citations | CPP |
| :--- | :--- | :---: | :---: | :---: |
""" + "\n".join(rows) + f"""

💡 *Note:* Citation counts reflect all indexed Scopus publications currently loaded in the dashboard repository.
"""

    # 5. Cross-Department & Multidisciplinary Collaborations
    if any(w in q for w in ["collab", "international", "industry", "cross", "multidisciplinary", "partner"]):
        intl = kpis.get("intl_collab", 0)
        ind = kpis.get("industry_collab", 0)
        return f"""### 🤝 Strategic Collaboration & Cross-Departmental Opportunities

**Current Collaboration Metrics:**
- 🌐 **International Co-authored Papers:** **{intl}**
- 🏭 **Industry & Corporate Co-authored Papers:** **{ind}**
- 🏛️ **Institutional Cross-Linkages:** Active collaborations across IISc, IITs, SPPU, and overseas universities.

**High-Potential Interdisciplinary Research Clusters for COEP:**
1. **AI & Smart Manufacturing:** Joint initiative between *Computer Engineering*, *Mechanical*, and *Production Engineering*.
2. **Clean Energy & Battery Materials:** Collaborative cluster combining *Metallurgy & Material Science*, *Chemical*, and *Electrical Engineering*.
3. **Smart Urban Infrastructure & IoT:** Multi-department cluster between *Civil Engineering*, *Electronics & Telecommunication*, and *Instrumentation*.

💡 *Recommendation:* Establish targeted seed grants for inter-departmental collaborative proposals to maximize Q1 international co-authorship.
"""

    # 6. Default Comprehensive Response
    return f"""### 🤖 COEP Research Intelligence Overview

Based on the filtered Scopus dataset of **{total_pubs:,} indexed publications**:

- 📊 **Cumulative Impact:** Accrued **{total_cites:,} citations** with an institutional **{cpp} Citations Per Paper (CPP)** average.
- 🏆 **Quality Standard:** **{kpis.get('q1_count', 'N/A')} Q1 publications** represent COEP's highest tier global research impact.
- 🌐 **Collaboration Reach:** **{kpis.get('intl_collab', 'N/A')} international** and **{kpis.get('industry_collab', 'N/A')} industry** joint publications.

**Suggested Deep Dives:**
- Ask: *\"Which department has the most Q1 papers?\"*
- Ask: *\"Who are the top 5 cited authors in COEP?\"*
- Ask: *\"Generate Executive NIRF/NAAC Summary\"*
- Ask: *\"Identify cross-department collaboration opportunities\"*
"""


def generate_executive_dossier(df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
    """Generates a comprehensive executive research briefing for NIRF/NAAC review."""
    if df.empty:
        return "⚠️ No publication data available to generate executive dossier."

    total_pubs = len(df)
    total_cites = int(df["citations"].sum()) if "citations" in df.columns else 0
    cpp = round(total_cites / max(1, total_pubs), 2)
    q1_count = int((df["quartile"] == "Q1").sum()) if "quartile" in df.columns else 0
    q1_pct = round(q1_count / max(1, total_pubs) * 100, 1)

    top_dept = df["department"].value_counts().index[0] if "department" in df.columns and not df["department"].empty else "N/A"
    top_cites_dept = df.groupby("department")["citations"].sum().sort_values(ascending=False).index[0] if "department" in df.columns and "citations" in df.columns else "N/A"
    
    top_papers = df.sort_values("citations", ascending=False).head(3) if "citations" in df.columns else pd.DataFrame()
    top_papers_str = []
    for _, r in top_papers.iterrows():
        top_papers_str.append(f"- **{r.get('title', 'N/A')}** ({r.get('year', 'N/A')}) — {r.get('journal', 'N/A')} | **{int(r.get('citations', 0))} Citations**")

    return f"""# 🏛️ COEP Technological University, Pune
## Executive Research & Bibliometric Dossier (Scopus Intelligence)

---

### 1. Executive Summary & Macro Performance
COEP Technological University demonstrates sustained research productivity and scientific citation impact across core engineering and technological disciplines.

- **Total Scopus Indexed Publications:** **{total_pubs:,}**
- **Cumulative Citations Accrued:** **{total_cites:,}**
- **Institutional Citations Per Paper (CPP):** **{cpp}**
- **Q1 High-Impact Publications:** **{q1_count:,}** ({q1_pct}% of total research output)
- **Active Publishing Faculty:** **{kpis.get('active_authors', 'N/A')}**

---

### 2. Departmental Research Pillars
- **Volume Driver:** **{top_dept}** leads total publication volume.
- **Citation Driver:** **{top_cites_dept}** commands the highest cumulative academic impact.
- **Multidisciplinary Trends:** Emerging research clusters in AI/Data Science, Materials & Nanotechnology, and Sustainable Energy show the fastest 3-year publication growth.

---

### 3. Landmark Scientific Works
""" + ("\n".join(top_papers_str) if top_papers_str else 'N/A') + f"""

---

### 4. Strategic Recommendations for NIRF & Global Accreditations
1. **Elevate Q1 Publication Share:** Incentivize submissions to IEEE Transactions, Elsevier, and Nature Springer high-impact Q1 venues.
2. **Broaden International Co-Authorships:** Establish formal research exchange programs with top-100 global partner institutions.
3. **Industry-Sponsored Research Integration:** Expand translational research projects with industrial R&D centers across Pune and Maharashtra manufacturing hubs.

---
*Report Generated automatically by COEP AI Research Copilot on {pd.Timestamp.now().strftime('%d %b %Y, %H:%M UTC')}.*
"""


def query_ai_copilot(prompt: str, df: pd.DataFrame, kpis: Dict[str, Any], chat_history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Unified query entry point:
    Attempts Google Gemini API if key is present; gracefully falls back to the analytical engine.
    """
    api_key = get_gemini_api_key()
    
    if api_key:
        context = generate_data_context(df, kpis)
        llm_response = call_gemini_api(prompt, context, api_key)
        if llm_response:
            return llm_response
            
    return run_analytical_copilot(prompt, df, kpis)

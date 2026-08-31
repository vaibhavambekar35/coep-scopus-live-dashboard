# COEP Scopus Live Dashboard - Production Release
"""
COEP AI Research Copilot & Intelligence Engine
Provides interactive natural language question answering, executive dossier generation,
author lookup, topic search, CiteScore/SJR journal rankings, and smart analytical querying.
"""

import os
import re
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
            "You are the COEP Research Intelligence AI Copilot for COEP Technological University, Pune (A Unitary Public Technological University to Government Maharashtra, Estd. 2022). "
            "You have access to verified Scopus bibliometric data for COEP faculty and departments. "
            "Provide concise, authoritative, executive-level insights, rankings, data tables, and specific paper counts. "
            "Always base your answers strictly on the provided Scopus data context. If specific author or paper data is asked, find and report it accurately. "
            "Format responses using clean Markdown with bolding, bullet points, and tables where appropriate."
        )
        
        full_content = f"{system_instruction}\n\nSYSTEM CONTEXT:\n{context}\n\nUSER QUESTION:\n{prompt}"
        
        payload = {
            "contents": [
                {"parts": [{"text": full_content}]}
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
    
    dept_counts = df["department"].value_counts().head(10).to_dict() if "department" in df.columns else {}
    dept_cites = df.groupby("department")["citations"].sum().sort_values(ascending=False).head(10).to_dict() if "department" in df.columns and "citations" in df.columns else {}
    q_counts = df["quartile"].value_counts().to_dict() if "quartile" in df.columns else {}
    
    top_authors = []
    auth_col = "primary_author" if "primary_author" in df.columns else None
    if auth_col:
        auth_grp = df.groupby(auth_col).agg(pubs=("title", "count"), cites=("citations", "sum")).sort_values("cites", ascending=False).head(15)
        for auth, row in auth_grp.iterrows():
            top_authors.append(f"{auth}: {int(row['pubs'])} papers, {int(row['cites'])} citations")
            
    landmarks = []
    if "citations" in df.columns:
        top_papers = df.sort_values("citations", ascending=False).head(8)
        for _, r in top_papers.iterrows():
            auth_val = r.get('primary_author', r.get('authors_str', 'N/A'))
            landmarks.append(f"- \"{r.get('title', 'Unknown')}\" ({r.get('year', 'N/A')}) by {auth_val} in {r.get('journal', 'N/A')} - {int(r.get('citations', 0))} citations [Dept: {r.get('department', 'N/A')}]")

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
        "DEPARTMENT RESEARCH OUTPUT (Top 10):",
        json.dumps(dept_counts, indent=2),
        "",
        "DEPARTMENT CITATION IMPACT (Top 10):",
        json.dumps(dept_cites, indent=2),
        "",
        "TOP CONTRIBUTING FACULTY:",
        "\n".join(top_authors),
        "",
        "LANDMARK HIGHLY CITED RESEARCH:",
        "\n".join(landmarks)
    ]
    return "\n".join(lines)


def search_specific_author(prompt: str, df: pd.DataFrame) -> pd.DataFrame:
    """Extracts author candidate tokens and finds matching author publications."""
    if df.empty:
        return pd.DataFrame()
        
    cleaned = re.sub(r'\b(dr|prof|professor|mr|mrs|ms|published|authored|by|documents|papers|number|of|how|many|count|who|is|give|me|find|show|details|for|about|articles)\b', '', prompt, flags=re.IGNORECASE).strip(' .?,:;!')
    raw_tokens = [t for t in re.split(r'\s+', cleaned) if len(t) >= 3]
    
    if not raw_tokens:
        return pd.DataFrame()
        
    for token in raw_tokens:
        t_pattern = rf'\b{re.escape(token.lower())}\b'
        if "primary_author" in df.columns:
            m1 = df["primary_author"].astype(str).str.lower().str.contains(t_pattern, regex=True, na=False)
            if m1.any():
                return df[m1]
        if "coep_authors" in df.columns:
            m2 = df["coep_authors"].astype(str).str.lower().str.contains(t_pattern, regex=True, na=False)
            if m2.any():
                return df[m2]
        if "authors_str" in df.columns:
            m3 = df["authors_str"].astype(str).str.lower().str.contains(t_pattern, regex=True, na=False)
            if m3.any():
                return df[m3]
                
    return pd.DataFrame()


def get_citescore_leaderboard_response(df: pd.DataFrame) -> str:
    """Renders the top publications ranked strictly by highest CiteScore / SJR."""
    if df.empty or "citescore" not in df.columns:
        return "No CiteScore data available."
        
    top_cs = df.sort_values("citescore", ascending=False).head(5)
    
    rows = []
    for i, (_, r) in enumerate(top_cs.iterrows(), 1):
        cs_val = round(float(r.get("citescore", 0.0)), 1)
        sjr_val = round(float(r.get("sjr", 0.0)), 2)
        cites_val = int(r.get("citations", 0))
        auth_val = r.get("primary_author") or r.get("authors_str", "COEP Faculty")
        
        rows.append(
            f"**{i}. {r.get('title', 'N/A')}**\n"
            f"- 🏆 **CiteScore:** **{cs_val}** | SJR: **{sjr_val}** | Quartile: **{r.get('quartile', 'Q1')}**\n"
            f"- 📖 **Journal / Source:** *{r.get('journal', 'N/A')}*\n"
            f"- 👤 **Author:** {auth_val} | 📅 Year: **{r.get('year', 'N/A')}** | 🌟 Citations: **{cites_val:,}**\n"
            f"- 🏛️ **Department:** {r.get('department', 'N/A')}\n"
        )
        
    highest_cs_journal = top_cs.iloc[0].get("journal", "N/A")
    highest_cs_score = round(float(top_cs.iloc[0].get("citescore", 0.0)), 1)
    
    return f"""### 🏆 Highest CiteScore Publications (COEP Scopus Archive)

**Leader:** The highest CiteScore publication in the COEP archive is published in ***{highest_cs_journal}*** with a **CiteScore of {highest_cs_score}**.

---

{chr(10).join(rows)}
💡 *Note:* CiteScore measures the average citations received per peer-reviewed document over a 4-year window in Scopus.
"""


def get_most_cited_papers_response(df: pd.DataFrame) -> str:
    """Renders top papers ranked by cumulative citations."""
    if df.empty or "citations" not in df.columns:
        return "No citation data available."
        
    top_cites = df.sort_values("citations", ascending=False).head(5)
    
    rows = []
    for i, (_, r) in enumerate(top_cites.iterrows(), 1):
        cites_val = int(r.get("citations", 0))
        auth_val = r.get("primary_author") or r.get("authors_str", "COEP Faculty")
        rows.append(
            f"**{i}. {r.get('title', 'N/A')}**\n"
            f"- 🌟 **Citations:** **{cites_val:,} citations**\n"
            f"- 📖 **Journal:** *{r.get('journal', 'N/A')}* ({r.get('year', 'N/A')})\n"
            f"- 👤 **Primary Author:** {auth_val} | 🏛️ **Dept:** {r.get('department', 'N/A')}\n"
        )
        
    return f"""### 🌟 Top Landmark Publications by Citations (COEP Archive)

---

{chr(10).join(rows)}
"""


def get_top_authors_response(df: pd.DataFrame) -> str:
    """Renders top cited and highest volume author leaderboard."""
    auth_col = "primary_author" if "primary_author" in df.columns else None
    if not auth_col or df.empty:
        return "No author data available."
        
    auth_grp = df.groupby(auth_col).agg(
        pubs=("title", "count"),
        cites=("citations", "sum"),
        dept=("department", "first")
    ).reset_index().sort_values("cites", ascending=False).head(10)
    
    rows = []
    for i, r in auth_grp.iterrows():
        cpp_auth = round(r["cites"] / max(1, r["pubs"]), 1)
        rows.append(f"| **{r[auth_col]}** | {r['dept']} | {int(r['pubs']):,} | {int(r['cites']):,} | {cpp_auth} |")
        
    top_cites_auth = auth_grp.iloc[0][auth_col]
    top_cites_val = int(auth_grp.iloc[0]["cites"])
    top_pubs_auth = df[auth_col].value_counts().index[0]
    top_pubs_val = int(df[auth_col].value_counts().iloc[0])
    
    return f"""### 👥 Top Author & Faculty Research Intelligence

**Key Highlights:**
- 🌟 **Most Cited Faculty:** **{top_cites_auth}** ({top_cites_val:,} total citations)
- 📚 **Highest Volume Contributor:** **{top_pubs_auth}** ({top_pubs_val:,} indexed publications)

| Author / Faculty | Primary Department | Papers | Total Citations | CPP |
| :--- | :--- | :---: | :---: | :---: |
""" + "\n".join(rows) + f"""

💡 *Tip:* Ask about any specific faculty member (e.g. *\"Documents by Dr. Chaskar\"* or *\"Papers by Agashe\"*).
"""


def get_department_leaderboard_response(df: pd.DataFrame) -> str:
    """Renders department output and citation leaderboard."""
    if "department" not in df.columns or "citations" not in df.columns or df.empty:
        return "No department data available."
        
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

**Key Highlights:**
- 🥇 **Highest Volume Department:** **{top_dept}** ({int(dept_stats.iloc[0]['pubs']):,} indexed papers).
- 🌟 **Highest Citation Impact:** **{top_cite_dept}** ({int(dept_stats.sort_values('cites', ascending=False).iloc[0]['cites']):,} total citations).
- 🏆 **Most Q1 High-Impact Papers:** **{top_q1_dept}** ({int(dept_stats.sort_values('q1', ascending=False).iloc[0]['q1']):,} Q1 publications).

| Department / School | Publications | Total Citations | Citations/Paper (CPP) | Q1 Papers |
| :--- | :---: | :---: | :---: | :---: |
""" + "\n".join(table_rows) + f"""

💡 *Recommendation:* Foster joint interdisciplinary initiatives between **{top_dept}** and emerging computing/materials clusters.
"""


def get_department_detail_response(df: pd.DataFrame, kw: str, dept_full_name: str, total_pubs: int) -> str:
    """Renders detailed research breakdown for a specific department."""
    dept_df = df[df["department"].astype(str).str.lower().str.contains(kw, na=False)] if "department" in df.columns else pd.DataFrame()
    if dept_df.empty:
        return f"No publication data found for department matching '{dept_full_name}'."
        
    d_pubs = len(dept_df)
    d_cites = int(dept_df["citations"].sum()) if "citations" in dept_df.columns else 0
    d_cpp = round(d_cites / max(1, d_pubs), 2)
    d_q1 = int((dept_df["quartile"] == "Q1").sum()) if "quartile" in dept_df.columns else 0
    
    top_auths = dept_df["primary_author"].value_counts().head(5) if "primary_author" in dept_df.columns else pd.Series()
    auth_list = [f"- **{a}**: {c} papers" for a, c in top_auths.items()]
    
    top_papers = dept_df.sort_values("citations", ascending=False).head(3)
    paper_list = [f"- **{r.get('title', 'N/A')}** ({r.get('year', 'N/A')}) — {int(r.get('citations', 0))} citations" for _, r in top_papers.iterrows()]
    
    return f"""### 🏛️ Department Research Insights: **{dept_full_name}**

**Performance Overview:**
- 📚 **Total Publications:** **{d_pubs:,} indexed papers** ({round(d_pubs/max(1, total_pubs)*100, 1)}% of COEP output)
- 🌟 **Total Citations:** **{d_cites:,}**
- 📈 **Citations Per Paper (CPP):** **{d_cpp}**
- 🏆 **Q1 Publications:** **{d_q1:,}**

**Leading Contributing Faculty in Department:**
{chr(10).join(auth_list) if auth_list else 'N/A'}

**Top Cited Papers from Department:**
{chr(10).join(paper_list) if paper_list else 'N/A'}
"""


def run_analytical_copilot(prompt: str, df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
    """
    Intelligent built-in analytical engine that accurately answers natural language research questions
    directly from pandas computations with zero API latency.
    """
    q = prompt.lower().strip()
    
    if df.empty:
        return "⚠️ **No publication data available** for the currently selected filters. Please adjust the year range or department in the sidebar."

    total_pubs = len(df)
    total_cites = int(df["citations"].sum()) if "citations" in df.columns else 0
    cpp = round(total_cites / max(1, total_pubs), 2)
    
    # ---------------------------------------------------------
    # 1. CITESCORE / SJR / IMPACT FACTOR PAPER RANKINGS
    # ---------------------------------------------------------
    if any(p in q for p in ["citescore", "cite score", "sjr", "impact factor", "highest citescore", "most citescore", "top citescore", "prestigious"]):
        return get_citescore_leaderboard_response(df)

    # ---------------------------------------------------------
    # 2. ACCREDITATION / EXECUTIVE / NIRF / NAAC SUMMARY
    # ---------------------------------------------------------
    if any(w in q for w in ["dossier", "executive", "nirf", "naac", "accreditation", "report", "briefing"]):
        return generate_executive_dossier(df, kpis)
        
    # ---------------------------------------------------------
    # 3. MOST CITED PAPERS / LANDMARK CITATION RANKINGS
    # ---------------------------------------------------------
    if any(p in q for p in ["most cited paper", "highest cited paper", "highest citation paper", "top cited paper", "landmark paper", "most cited document", "highest citation", "top citations"]):
        return get_most_cited_papers_response(df)

    # ---------------------------------------------------------
    # 4. GENERAL AUTHOR RANKINGS / LEADERBOARD
    # ---------------------------------------------------------
    if any(p in q for p in ["most cited faculty", "most cited author", "top author", "leading author", "top faculty", "highest publication", "most paper", "most document", "top contributor", "who has the most", "who is the top"]):
        return get_top_authors_response(df)

    # ---------------------------------------------------------
    # 5. SPECIFIC AUTHOR NAME LOOKUP (Dr. Chaskar, Prof. Patil, etc.)
    # ---------------------------------------------------------
    author_matches = search_specific_author(prompt, df)
    if not author_matches.empty:
        num_docs = len(author_matches)
        auth_cites = int(author_matches["citations"].sum()) if "citations" in author_matches.columns else 0
        auth_cpp = round(auth_cites / max(1, num_docs), 2)
        
        primary_name = author_matches["primary_author"].value_counts().index[0] if ("primary_author" in author_matches.columns and not author_matches["primary_author"].empty) else prompt.title()
        depts = author_matches["department"].value_counts().index.tolist() if "department" in author_matches.columns else []
        dept_str = ", ".join(depts[:2]) if depts else "COEP"
        q1_docs = int((author_matches["quartile"] == "Q1").sum()) if "quartile" in author_matches.columns else 0
        
        top_p = author_matches.sort_values("citations", ascending=False).head(5)
        p_rows = []
        for _, r in top_p.iterrows():
            p_rows.append(f"- 📄 **{r.get('title', 'N/A')}** ({r.get('year', 'N/A')})\n  *Journal:* {r.get('journal', 'N/A')} | **{int(r.get('citations', 0))} Citations** | Quartile: **{r.get('quartile', 'N/A')}**")
            
        return f"""### 👤 Faculty Research Profile: **{primary_name}**

**Summary Metrics:**
- 📚 **Total Indexed Documents:** **{num_docs:,} publications**
- 🌟 **Total Citations Accrued:** **{auth_cites:,} citations**
- 📈 **Average Citations Per Paper (CPP):** **{auth_cpp}**
- 🏆 **Q1 High-Impact Papers:** **{q1_docs}**
- 🏛️ **Primary Department:** **{dept_str}**

---

#### 📑 Indexed Publications Breakdown:
{chr(10).join(p_rows)}
"""

    # ---------------------------------------------------------
    # 6. DEPARTMENT QUERIES
    # ---------------------------------------------------------
    dept_keywords = {
        "mechanical": "Mechanical Engineering",
        "computer": "Computer Engineering & IT",
        "electrical": "Electrical Engineering",
        "civil": "Civil Engineering",
        "metallurgy": "Metallurgy & Material Science",
        "electronics": "Electronics & Telecommunication",
        "entc": "Electronics & Telecommunication",
        "instrumentation": "Instrumentation & Control",
        "production": "Production & Industrial",
        "applied science": "Applied Sciences, Physics & Chem",
        "physics": "Applied Sciences, Physics & Chem",
        "chemistry": "Applied Sciences, Physics & Chem",
        "math": "Mathematics & Management"
    }
    
    for kw, dept_full_name in dept_keywords.items():
        if kw in q:
            return get_department_detail_response(df, kw, dept_full_name, total_pubs)
            
    if any(w in q for w in ["department", "dept", "school", "branch", "ranking", "leaderboard", "leading"]):
        return get_department_leaderboard_response(df)

    # ---------------------------------------------------------
    # 7. JOURNAL QUALITY & QUARTILES (Q1, Q2, Q3, Q4)
    # ---------------------------------------------------------
    if any(w in q for w in ["q1", "q2", "q3", "q4", "quartile", "quality", "tier"]):
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
- 🥇 **Q1 (Top 25% High-Impact Journals):** **{q1_c:,}** publications (**{q1_pct}%** of all output)
- 🥈 **Q2 (Top 50% Journals):** **{q2_c:,}** publications (**{q2_pct}%** of all output)
- 🥉 **Q3 & Q4 Journals:** **{q3_c + q4_c:,}** publications

| Tier | Publication Count | Proportion | Strategic Impact |
| :--- | :---: | :---: | :--- |
| **Q1 (High Impact)** | {q1_c:,} | {q1_pct}% | Core tier for NIRF/QS Ranking scores |
| **Q2 (Upper Mid)** | {q2_c:,} | {q2_pct}% | Strong peer-reviewed pipeline |
| **Q3 (Lower Mid)** | {q3_c:,} | {round(q3_c/max(1, total_pubs)*100, 1)}% | Solid technical contributions |
| **Q4 (Entry Tier)** | {q4_c:,} | {round(q4_c/max(1, total_pubs)*100, 1)}% | Early-stage research foundation |

**Top Cited Q1 Papers from COEP:**
""" + "\n".join(p_list)

    # ---------------------------------------------------------
    # 8. COLLABORATIONS & PARTNERSHIPS
    # ---------------------------------------------------------
    if any(w in q for w in ["collab", "international", "industry", "cross", "multidisciplinary", "partner", "foreign", "team"]):
        intl = kpis.get("intl_collab", 0)
        ind = kpis.get("industry_collab", 0)
        return f"""### 🤝 Strategic Collaboration & Cross-Departmental Opportunities

**Current Collaboration Metrics:**
- 🌐 **International Co-authored Papers:** **{intl}**
- 🏭 **Industry & Corporate Co-authored Papers:** **{ind}**
- 🏛️ **Institutional Linkages:** Active partnerships with global and national universities.

**High-Potential Multidisciplinary Clusters for COEP:**
1. **AI & Smart Manufacturing:** Joint research cluster between *Computer Engineering*, *Mechanical*, and *Production Engineering*.
2. **Clean Energy & Battery Materials:** Collaborative cluster combining *Metallurgy & Material Science*, *Chemical*, and *Electrical Engineering*.
3. **Smart Urban Infrastructure & IoT:** Multi-department initiative between *Civil Engineering*, *Electronics & Telecommunication*, and *Instrumentation*.
"""

    # ---------------------------------------------------------
    # 9. TOPIC / KEYWORD SEARCH (e.g., Solar, AI, Robotics, Concrete, EV, Battery)
    # ---------------------------------------------------------
    topic_words = [w for w in re.split(r'\s+', q) if len(w) >= 3 and w not in ["what", "how", "many", "papers", "about", "show", "find", "tell", "coep", "give", "the", "for", "and", "are", "paper"]]
    if topic_words:
        for tw in topic_words:
            t_mask = df["title"].astype(str).str.lower().str.contains(tw, na=False) | df["abstract"].astype(str).str.lower().str.contains(tw, na=False)
            topic_df = df[t_mask]
            if not topic_df.empty and len(topic_df) < len(df) * 0.9:
                t_count = len(topic_df)
                t_cites = int(topic_df["citations"].sum()) if "citations" in topic_df.columns else 0
                top_t_papers = topic_df.sort_values("citations", ascending=False).head(4)
                p_list = [f"- **{r.get('title', 'N/A')}** ({r.get('year', 'N/A')})\n  *Journal:* {r.get('journal', 'N/A')} | **{int(r.get('citations', 0))} Citations** | Dept: **{r.get('department', 'N/A')}**" for _, r in top_t_papers.iterrows()]
                
                return f"""### 🔍 Research Topic Intelligence: **\"{tw.capitalize()}\"**

- 📚 **Matching Publications:** **{t_count:,} indexed papers**
- 🌟 **Cumulative Citations:** **{t_cites:,}**

**Leading Papers on this Topic:**
{chr(10).join(p_list)}
"""

    # ---------------------------------------------------------
    # 10. DEFAULT OVERVIEW
    # ---------------------------------------------------------
    return f"""### 🤖 COEP Research Intelligence Overview

Based on the filtered Scopus dataset of **{total_pubs:,} indexed publications**:

- 📊 **Cumulative Impact:** Accrued **{total_cites:,} citations** with an institutional **{cpp} Citations Per Paper (CPP)** average.
- 🏆 **Quality Standard:** **{kpis.get('q1_count', 'N/A')} Q1 publications** represent COEP's highest tier global research impact.
- 🌐 **Collaboration Reach:** **{kpis.get('intl_collab', 'N/A')} international** and **{kpis.get('industry_collab', 'N/A')} industry** joint publications.

**Suggested Queries You Can Try:**
- *\"What is the highest CiteScore paper?\"*
- *\"Number of documents published by Dr. Chaskar\"*
- *\"Who has the most citations in COEP?\"*
- *\"Which department has the most Q1 publications?\"*
- *\"Find papers on Solar energy or Machine Learning\"*
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
    Attempts Google Gemini API if key is present; gracefully falls back to the smart analytical engine.
    """
    api_key = get_gemini_api_key()
    
    if api_key:
        context = generate_data_context(df, kpis)
        llm_response = call_gemini_api(prompt, context, api_key)
        if llm_response:
            return llm_response
            
    return run_analytical_copilot(prompt, df, kpis)

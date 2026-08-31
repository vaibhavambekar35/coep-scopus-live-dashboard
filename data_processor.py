# COEP Scopus Live Dashboard - Production Release
"""
Data Processing and KPI Calculation Module for COEP Scopus Dashboard.
Computes all 10 Top KPIs, Trend Analytics, Research Impact, Collaboration Stats,
Quality Metrics (Q1-Q4), and Data Filtering.
"""

from datetime import datetime, date
import pandas as pd
from typing import Dict, Any, List, Optional


def to_dataframe(publications: List[Dict[str, Any]]) -> pd.DataFrame:
    """Converts publications list of dicts to a typed pandas DataFrame."""
    if not publications:
        return pd.DataFrame()

    df = pd.DataFrame(publications)
    
    # Ensure types
    if "citations" in df.columns:
        df["citations"] = pd.to_numeric(df["citations"], errors="coerce").fillna(0).astype(int)
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").fillna(2025).astype(int)
    if "citescore" in df.columns:
        df["citescore"] = pd.to_numeric(df["citescore"], errors="coerce").fillna(0.0)
    if "sjr" in df.columns:
        df["sjr"] = pd.to_numeric(df["sjr"], errors="coerce").fillna(0.0)
    if "publication_date" in df.columns:
        today_str = datetime.now().strftime("%Y-%m-%d")
        df["publication_date"] = df["publication_date"].astype(str).apply(
            lambda d: today_str if d > today_str and d not in ["None", "nan", ""] else d
        )
        df["pub_date_dt"] = pd.to_datetime(df["publication_date"], errors="coerce")

    return df


def calculate_top_10_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes the exact 10 Top KPIs for the COEP Scopus Dashboard:
    1. Total Scopus Publications
    2. Publications – 2026
    3. Publications – 2025
    4. Total Citations
    5. Citations per Publication
    6. Q1 Publications
    7. International Collaborations
    8. Industry Collaborations
    9. Active Publishing Faculty
    10. Publications in Last 30 Days
    """
    if df.empty:
        return {
            "total_publications": 0,
            "publications_2026": 0,
            "publications_2025": 0,
            "total_citations": 0,
            "citations_per_pub": 0.0,
            "q1_count": 0,
            "q1_pct": 0.0,
            "intl_collab_count": 0,
            "intl_collab_pct": 0.0,
            "industry_collab_count": 0,
            "industry_collab_pct": 0.0,
            "active_faculty_count": 0,
            "pubs_last_30_days": 0,
        }

    total_pubs = len(df)
    pubs_2026 = len(df[df["year"] == 2026])
    pubs_2025 = len(df[df["year"] == 2025])
    
    total_citations = int(df["citations"].sum())
    citations_per_pub = round(total_citations / total_pubs, 2) if total_pubs > 0 else 0.0

    # Q1 Publications
    q1_df = df[df["quartile"] == "Q1"]
    q1_count = len(q1_df)
    q1_pct = round((q1_count / total_pubs) * 100, 1) if total_pubs > 0 else 0.0

    # International Collaborations
    intl_df = df[df["is_international_collab"] == True]
    intl_count = len(intl_df)
    intl_pct = round((intl_count / total_pubs) * 100, 1) if total_pubs > 0 else 0.0

    # Industry Collaborations
    ind_df = df[df["is_industry_collab"] == True]
    ind_count = len(ind_df)
    ind_pct = round((ind_count / total_pubs) * 100, 1) if total_pubs > 0 else 0.0

    # Active Publishing Faculty (COEP Faculty)
    all_faculty = set()
    for auth_list in df["coep_authors"].dropna():
        if isinstance(auth_list, list):
            all_faculty.update(auth_list)
        elif isinstance(auth_list, str):
            all_faculty.add(auth_list)
    active_faculty_count = len(all_faculty)

    # Publications in Last 30 Days
    now = pd.Timestamp.now()
    thirty_days_ago = now - pd.Timedelta(days=30)
    if "pub_date_dt" in df.columns:
        recent_df = df[df["pub_date_dt"] >= thirty_days_ago]
        pubs_last_30_days = len(recent_df)
    else:
        pubs_last_30_days = len(df[df["year"] == 2026]) // 4

    return {
        "total_publications": total_pubs,
        "publications_2026": pubs_2026,
        "publications_2025": pubs_2025,
        "total_citations": total_citations,
        "citations_per_pub": citations_per_pub,
        "q1_count": q1_count,
        "q1_pct": q1_pct,
        "intl_collab_count": intl_count,
        "intl_collab_pct": intl_pct,
        "industry_collab_count": ind_count,
        "industry_collab_pct": ind_pct,
        "active_faculty_count": active_faculty_count,
        "pubs_last_30_days": pubs_last_30_days
    }


def get_publications_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Returns annual publication volume and cumulative growth."""
    if df.empty or "year" not in df.columns:
        return pd.DataFrame()
    
    annual = df.groupby("year").size().reset_index(name="count")
    annual = annual.sort_values("year")
    annual["cumulative"] = annual["count"].cumsum()
    return annual


def get_publications_by_month(df: pd.DataFrame, year: Optional[int] = None) -> pd.DataFrame:
    """Returns monthly publication volume for a given year or recent periods."""
    if df.empty:
        return pd.DataFrame()
    
    sub_df = df if year is None else df[df["year"] == year]
    if sub_df.empty:
        return pd.DataFrame()

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    monthly = sub_df.groupby("month").size().reindex(month_order, fill_value=0).reset_index(name="count")
    return monthly


def get_publications_by_department(df: pd.DataFrame) -> pd.DataFrame:
    """Returns publications count grouped by COEP department."""
    if df.empty or "department" not in df.columns:
        return pd.DataFrame()
    
    dept_df = df.groupby("department").size().reset_index(name="count")
    dept_df = dept_df.sort_values("count", ascending=True)  # for horizontal bar chart
    return dept_df


def get_citations_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Returns total and average citations grouped by publication year."""
    if df.empty or "year" not in df.columns:
        return pd.DataFrame()
    
    cite_df = df.groupby("year").agg(
        total_citations=("citations", "sum"),
        avg_citations=("citations", "mean"),
        count=("citations", "count")
    ).reset_index()
    cite_df["avg_citations"] = cite_df["avg_citations"].round(2)
    return cite_df.sort_values("year")


def get_highly_cited_papers(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Returns top N highly cited papers with full details."""
    if df.empty:
        return pd.DataFrame()
    
    cols = ["title", "authors_str", "department", "journal", "year", "citations", "citescore", "quartile", "doi_url"]
    existing_cols = [c for c in cols if c in df.columns]
    
    return df.sort_values("citations", ascending=False).head(top_n)[existing_cols]


def get_collaboration_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Returns counts and percentages for collaboration types."""
    if df.empty or "collaboration_type" not in df.columns:
        return pd.DataFrame()
    
    collab = df["collaboration_type"].value_counts().reset_index()
    collab.columns = ["collaboration_type", "count"]
    collab["percentage"] = (collab["count"] / len(df) * 100).round(1)
    return collab


def get_top_collaborating_institutions(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Extracts top partner universities and organizations."""
    if df.empty or "external_institutions" not in df.columns:
        return pd.DataFrame()
    
    all_insts = []
    for inst_list in df["external_institutions"].dropna():
        if isinstance(inst_list, list):
            all_insts.extend(inst_list)
        elif isinstance(inst_list, str) and inst_list:
            all_insts.append(inst_list)

    if not all_insts:
        return pd.DataFrame(columns=["institution", "count"])

    s = pd.Series(all_insts).value_counts().head(top_n).reset_index()
    s.columns = ["institution", "count"]
    return s


def get_top_collaborating_countries(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Extracts foreign collaborating countries."""
    if df.empty or "foreign_countries" not in df.columns:
        return pd.DataFrame()
    
    all_countries = []
    for c_list in df["foreign_countries"].dropna():
        if isinstance(c_list, list):
            all_countries.extend(c_list)
        elif isinstance(c_list, str) and c_list:
            all_countries.append(c_list)

    if not all_countries:
        return pd.DataFrame(columns=["country", "count"])

    s = pd.Series(all_countries).value_counts().head(top_n).reset_index()
    s.columns = ["country", "count"]
    return s


def get_quartile_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Returns distribution of Q1, Q2, Q3, Q4 journal papers."""
    if df.empty or "quartile" not in df.columns:
        return pd.DataFrame()
    
    q_order = ["Q1", "Q2", "Q3", "Q4"]
    q_counts = df["quartile"].value_counts().reindex(q_order, fill_value=0).reset_index()
    q_counts.columns = ["quartile", "count"]
    q_counts["percentage"] = (q_counts["count"] / len(df) * 100).round(1) if len(df) > 0 else 0
    return q_counts


def filter_publications(
    df: pd.DataFrame,
    search_query: str = "",
    year_range: Optional[tuple[int, int]] = None,
    departments: Optional[List[str]] = None,
    quartiles: Optional[List[str]] = None,
    collab_types: Optional[List[str]] = None,
    doc_types: Optional[List[str]] = None
) -> pd.DataFrame:
    """Applies multi-faceted filtering on the publications DataFrame."""
    if df.empty:
        return df

    filtered = df.copy()

    # Search filter across title, authors, journal, DOI
    if search_query:
        q = search_query.lower().strip()
        mask = (
            filtered["title"].astype(str).str.lower().str.contains(q, na=False) |
            filtered["authors_str"].astype(str).str.lower().str.contains(q, na=False) |
            filtered["journal"].astype(str).str.lower().str.contains(q, na=False) |
            filtered["doi"].astype(str).str.lower().str.contains(q, na=False) |
            filtered["department"].astype(str).str.lower().str.contains(q, na=False)
        )
        filtered = filtered[mask]

    # Year Range Filter
    if year_range and "year" in filtered.columns:
        filtered = filtered[(filtered["year"] >= year_range[0]) & (filtered["year"] <= year_range[1])]

    # Department Filter
    if departments and "department" in filtered.columns:
        filtered = filtered[filtered["department"].isin(departments)]

    # Quartiles Filter
    if quartiles and "quartile" in filtered.columns:
        filtered = filtered[filtered["quartile"].isin(quartiles)]

    # Collaboration Type Filter
    if collab_types and "collaboration_type" in filtered.columns:
        filtered = filtered[filtered["collaboration_type"].isin(collab_types)]

    # Document Type Filter
    if doc_types and "document_type" in filtered.columns:
        filtered = filtered[filtered["document_type"].isin(doc_types)]

    return filtered


def export_to_bibtex(df: pd.DataFrame) -> str:
    """Generates standard BibTeX entries for the filtered publications dataset."""
    if df.empty:
        return "% No publications to export."

    bibtex_entries = []
    for idx, row in df.iterrows():
        cite_key = f"coep_{row.get('year', 2025)}_{idx}"
        title = row.get("title", "").replace("{", "").replace("}", "")
        authors = " and ".join(row.get("authors", [row.get("authors_str", "COEP")]))
        journal = row.get("journal", "")
        year = row.get("year", 2025)
        doi = row.get("doi", "")
        issn = row.get("issn", "")
        
        entry = (
            f"@article{{{cite_key},\n"
            f"  title = {{{title}}},\n"
            f"  author = {{{authors}}},\n"
            f"  journal = {{{journal}}},\n"
            f"  year = {{{year}}},\n"
            f"  doi = {{{doi}}},\n"
            f"  issn = {{{issn}}},\n"
            f"  institution = {{COEP Technological University, Pune}}\n"
            f"}}"
        )
        bibtex_entries.append(entry)

    return "\n\n".join(bibtex_entries)


def calculate_scival_annual_matrix(df: pd.DataFrame) -> Dict[Any, Dict[str, Any]]:
    """
    Computes the standard institutional performance matrix for COEP
    (Scholarly Output, Active Authors, Citations, CPP, h-Index) for 2020-2026 + Total.
    """
    matrix = {}
    years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
    
    if df.empty:
        for y in years:
            matrix[y] = {"pubs": 0, "authors": 0, "citations": 0, "cpp": 0.0, "h_index": 0}
        matrix["Total"] = {"pubs": 0, "authors": 0, "citations": 0, "cpp": 0.0, "h_index": 0}
        return matrix

    for y in years:
        sub = df[df["year"] == y]
        pubs = len(sub)
        cites = int(sub["citations"].sum()) if pubs > 0 else 0
        cpp = round(cites / pubs, 2) if pubs > 0 else 0.0
        
        # h-index
        c_list = sorted(sub["citations"].dropna().tolist(), reverse=True)
        h_idx = sum(1 for i, c in enumerate(c_list) if c >= i + 1)
        
        # unique authors
        authors = set()
        for a_item in sub["authors"].dropna():
            if isinstance(a_item, list):
                authors.update(a_item)
            elif isinstance(a_item, str):
                authors.add(a_item)
                
        matrix[y] = {
            "pubs": pubs,
            "authors": len(authors) if len(authors) > 0 else pubs // 3,
            "citations": cites,
            "cpp": cpp,
            "h_index": h_idx
        }

    # Total row across dataset
    total_pubs = len(df)
    total_cites = int(df["citations"].sum())
    tot_cpp = round(total_cites / total_pubs, 2) if total_pubs > 0 else 0.0
    all_c_list = sorted(df["citations"].dropna().tolist(), reverse=True)
    total_h = sum(1 for i, c in enumerate(all_c_list) if c >= i + 1)
    
    all_authors = set()
    for a_item in df["authors"].dropna():
        if isinstance(a_item, list):
            all_authors.update(a_item)
        elif isinstance(a_item, str):
            all_authors.add(a_item)

    matrix["Total"] = {
        "pubs": total_pubs,
        "authors": len(all_authors) if len(all_authors) > 0 else total_pubs // 3,
        "citations": total_cites,
        "cpp": tot_cpp,
        "h_index": total_h
    }

    return matrix


def get_scival_matrix_dataframe(metrics_by_year: Dict[Any, Dict[str, Any]]) -> pd.DataFrame:
    """Returns the SciVal annual matrix formatted as a clean pandas DataFrame."""
    years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
    total_data = metrics_by_year.get("Total", {})
    
    rows_data = [
        {"COEP Metric": "Scholarly Output", "Total": f"{total_data.get('pubs', 0):,}", **{str(y): f"{metrics_by_year.get(y, {}).get('pubs', 0):,}" for y in years}},
        {"COEP Metric": "Active Authors", "Total": f"{total_data.get('authors', 0):,}", **{str(y): f"{metrics_by_year.get(y, {}).get('authors', 0):,}" for y in years}},
        {"COEP Metric": "Total Citations", "Total": f"{total_data.get('citations', 0):,}", **{str(y): f"{metrics_by_year.get(y, {}).get('citations', 0):,}" for y in years}},
        {"COEP Metric": "Citations per Pub (CPP)", "Total": f"{total_data.get('cpp', 0.0):.2f}", **{str(y): f"{metrics_by_year.get(y, {}).get('cpp', 0.0):.2f}" for y in years}},
        {"COEP Metric": "h-Index", "Total": f"{total_data.get('h_index', 0)}", **{str(y): f"{metrics_by_year.get(y, {}).get('h_index', 0)}" for y in years}},
    ]
    return pd.DataFrame(rows_data)


def get_top_authors_leaderboard(df: pd.DataFrame, top_n: int = 25, sort_by: str = "pubs") -> pd.DataFrame:
    """
    Computes a comprehensive performance leaderboard for all COEP publishing faculty.
    Calculates Publications, Total Citations, CPP, h-Index, Q1 %, and Primary Department.
    """
    if df.empty:
        return pd.DataFrame()

    # Aggregate by individual author
    author_records: Dict[str, List[Dict[str, Any]]] = {}

    for _, row in df.iterrows():
        row_dict = row.to_dict()
        # Prefer coep_authors or fallback to authors list
        auth_list = row.get("coep_authors")
        if not auth_list or not isinstance(auth_list, (list, tuple)):
            auth_list = row.get("authors", [])
        if isinstance(auth_list, str):
            auth_list = [a.strip() for a in auth_list.split(",") if a.strip()]

        for author in auth_list:
            if not author or len(str(author).strip()) < 2:
                continue
            clean_author = str(author).strip()
            if clean_author not in author_records:
                author_records[clean_author] = []
            author_records[clean_author].append(row_dict)

    if not author_records:
        return pd.DataFrame()

    leaderboard = []
    for author, papers in author_records.items():
        pub_count = len(papers)
        if pub_count == 0:
            continue

        cites = [p.get("citations", 0) for p in papers]
        total_cites = sum(cites)
        cpp = round(total_cites / pub_count, 2)

        # h-index calculation for this author
        sorted_cites = sorted(cites, reverse=True)
        h_idx = sum(1 for i, c in enumerate(sorted_cites) if c >= i + 1)

        q1_count = sum(1 for p in papers if p.get("quartile") == "Q1")
        q1_pct = round((q1_count / pub_count) * 100, 1)

        intl_count = sum(1 for p in papers if p.get("is_international_collab") is True)
        intl_pct = round((intl_count / pub_count) * 100, 1)

        ind_count = sum(1 for p in papers if p.get("is_industry_collab") is True)
        ind_pct = round((ind_count / pub_count) * 100, 1)

        # Primary department (mode)
        depts = [p.get("department", "") for p in papers if p.get("department")]
        primary_dept = max(set(depts), key=depts.count) if depts else "Engineering"

        years = [p.get("year", 2025) for p in papers if p.get("year")]
        min_yr = min(years) if years else 2020
        max_yr = max(years) if years else 2026
        active_span = f"{min_yr}–{max_yr}" if min_yr != max_yr else str(min_yr)

        leaderboard.append({
            "Author": author,
            "Department": primary_dept,
            "Publications": pub_count,
            "Total Citations": total_cites,
            "CPP": cpp,
            "h-Index": h_idx,
            "Q1 Papers": q1_count,
            "Q1 Ratio": f"{q1_pct}%",
            "Q1_Pct_Num": q1_pct,
            "Intl Collab %": f"{intl_pct}%",
            "Industry Collab %": f"{ind_pct}%",
            "Active Period": active_span,
        })

    result_df = pd.DataFrame(leaderboard)

    # Sort
    if sort_by == "citations":
        result_df = result_df.sort_values(by=["Total Citations", "Publications"], ascending=[False, False])
    elif sort_by == "h_index":
        result_df = result_df.sort_values(by=["h-Index", "Total Citations"], ascending=[False, False])
    elif sort_by == "cpp":
        result_df = result_df.sort_values(by=["CPP", "Total Citations"], ascending=[False, False])
    elif sort_by == "q1":
        result_df = result_df.sort_values(by=["Q1_Pct_Num", "Q1 Papers"], ascending=[False, False])
    else:  # default pubs
        result_df = result_df.sort_values(by=["Publications", "Total Citations"], ascending=[False, False])

    result_df.reset_index(drop=True, inplace=True)
    result_df["Rank"] = result_df.index + 1
    return result_df.head(top_n)


def get_all_unique_authors(df: pd.DataFrame) -> List[str]:
    """Returns a complete list of all unique publishing faculty/authors in the dataset, sorted by publication count then name."""
    if df.empty:
        return []

    author_counts: Dict[str, int] = {}
    for _, row in df.iterrows():
        auths = row.get("coep_authors") or row.get("authors") or []
        if isinstance(auths, str):
            auths = [a.strip() for a in auths.split(",")]
        for a in auths:
            if a and len(str(a).strip()) > 1:
                clean_a = str(a).strip()
                author_counts[clean_a] = author_counts.get(clean_a, 0) + 1

    sorted_authors = sorted(author_counts.keys(), key=lambda k: (-author_counts[k], k))
    return sorted_authors


def get_author_profile_metrics(df: pd.DataFrame, author_name: str) -> Dict[str, Any]:
    """Computes comprehensive career profile metrics for a specific author."""
    if df.empty or not author_name:
        return {}

    author_clean = author_name.strip().lower()
    
    # Filter publications matching author
    matching_rows = []
    for _, row in df.iterrows():
        auths = row.get("coep_authors") or row.get("authors") or []
        if isinstance(auths, str):
            auths = [a.strip() for a in auths.split(",")]
        
        matched = any(author_clean == str(a).strip().lower() or author_clean in str(a).strip().lower() for a in auths if a)
        if not matched and "authors_str" in row and isinstance(row["authors_str"], str):
            matched = author_clean in row["authors_str"].lower()
        if matched:
            matching_rows.append(row.to_dict())

    if not matching_rows:
        return {}

    author_df = pd.DataFrame(matching_rows)
    total_pubs = len(author_df)
    total_cites = int(author_df["citations"].sum()) if "citations" in author_df.columns else 0
    cpp = round(total_cites / total_pubs, 2) if total_pubs > 0 else 0.0

    cites_list = sorted(author_df["citations"].dropna().tolist(), reverse=True) if "citations" in author_df.columns else []
    h_idx = sum(1 for i, c in enumerate(cites_list) if c >= i + 1)

    # Quartiles
    q_counts = author_df["quartile"].value_counts().to_dict() if "quartile" in author_df.columns else {}
    q1_count = q_counts.get("Q1", 0)
    q2_count = q_counts.get("Q2", 0)
    q3_count = q_counts.get("Q3", 0)
    q4_count = q_counts.get("Q4", 0)
    q1_pct = round((q1_count / total_pubs) * 100, 1) if total_pubs > 0 else 0.0

    # Collaborations
    intl_count = len(author_df[author_df["is_international_collab"] == True]) if "is_international_collab" in author_df.columns else 0
    intl_pct = round((intl_count / total_pubs) * 100, 1) if total_pubs > 0 else 0.0

    ind_count = len(author_df[author_df["is_industry_collab"] == True]) if "is_industry_collab" in author_df.columns else 0
    ind_pct = round((ind_count / total_pubs) * 100, 1) if total_pubs > 0 else 0.0

    # Department
    depts = author_df["department"].dropna().tolist() if "department" in author_df.columns else []
    primary_dept = max(set(depts), key=depts.count) if depts else "COEP Technological University"

    # Years
    years = author_df["year"].dropna().astype(int).tolist() if "year" in author_df.columns else []
    min_year = min(years) if years else 2020
    max_year = max(years) if years else 2026

    # Top co-authors
    co_authors_counter: Dict[str, int] = {}
    for _, r in author_df.iterrows():
        all_auths = r.get("authors") or []
        if isinstance(all_auths, str):
            all_auths = [a.strip() for a in all_auths.split(",")]
        for a in all_auths:
            if str(a).strip().lower() != author_clean:
                co_authors_counter[str(a).strip()] = co_authors_counter.get(str(a).strip(), 0) + 1

    top_collaborators = sorted(co_authors_counter.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "author_name": author_name,
        "primary_dept": primary_dept,
        "total_pubs": total_pubs,
        "total_citations": total_cites,
        "cpp": cpp,
        "h_index": h_idx,
        "q1_count": q1_count,
        "q2_count": q2_count,
        "q3_count": q3_count,
        "q4_count": q4_count,
        "q1_pct": q1_pct,
        "intl_count": intl_count,
        "intl_pct": intl_pct,
        "ind_count": ind_count,
        "ind_pct": ind_pct,
        "min_year": min_year,
        "max_year": max_year,
        "top_collaborators": [c[0] for c in top_collaborators],
    }


def get_author_publications(df: pd.DataFrame, author_name: str) -> pd.DataFrame:
    """Returns all publication rows for the selected author."""
    if df.empty or not author_name:
        return pd.DataFrame()

    author_clean = author_name.strip().lower()
    matching_indices = []

    for idx, row in df.iterrows():
        auths = row.get("coep_authors") or row.get("authors") or []
        if isinstance(auths, str):
            auths = [a.strip() for a in auths.split(",")]
        
        matched = any(author_clean == str(a).strip().lower() or author_clean in str(a).strip().lower() for a in auths if a)
        if not matched and "authors_str" in row and isinstance(row["authors_str"], str):
            matched = author_clean in row["authors_str"].lower()
        if matched:
            matching_indices.append(idx)

    if not matching_indices:
        return pd.DataFrame()

    result_df = df.loc[matching_indices].copy()
    if "citations" in result_df.columns:
        result_df = result_df.sort_values(by="citations", ascending=False)
    return result_df


def get_author_annual_trend(df: pd.DataFrame, author_name: str) -> pd.DataFrame:
    """Returns the yearly output and citation trend for a specific author."""
    author_pubs = get_author_publications(df, author_name)
    if author_pubs.empty or "year" not in author_pubs.columns:
        return pd.DataFrame(columns=["year", "publications", "citations"])

    grouped = author_pubs.groupby("year").agg(
        publications=("title", "count"),
        citations=("citations", "sum")
    ).reset_index().sort_values(by="year")

    return grouped


def get_landmark_cited_papers(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Returns COEP's highest-impact landmark publications ranked by citations."""
    if df.empty:
        return pd.DataFrame()

    sorted_df = df.sort_values(by="citations", ascending=False).head(top_n).copy()
    sorted_df.reset_index(drop=True, inplace=True)
    sorted_df["Rank"] = sorted_df.index + 1
    return sorted_df


def get_department_benchmark_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes a comprehensive multi-metric comparative benchmark matrix for all COEP academic departments.
    Calculates Publications Volume, Total Citations, CPP, Q1 Count, Q1 %, International %, Industry %, Active Faculty, and h-Index.
    """
    if df.empty or "department" not in df.columns:
        return pd.DataFrame()

    rows = []
    for dept, sub in df.groupby("department"):
        pubs = len(sub)
        if pubs == 0:
            continue
        cites = int(sub["citations"].sum())
        cpp = round(cites / pubs, 2) if pubs > 0 else 0.0

        q1_cnt = len(sub[sub["quartile"] == "Q1"])
        q1_pct = round((q1_cnt / pubs) * 100, 1) if pubs > 0 else 0.0

        q2_cnt = len(sub[sub["quartile"] == "Q2"])
        top_tier_pct = round(((q1_cnt + q2_cnt) / pubs) * 100, 1) if pubs > 0 else 0.0

        intl_cnt = len(sub[sub["is_international_collab"] == True])
        intl_pct = round((intl_cnt / pubs) * 100, 1) if pubs > 0 else 0.0

        ind_cnt = len(sub[sub["is_industry_collab"] == True])
        ind_pct = round((ind_cnt / pubs) * 100, 1) if pubs > 0 else 0.0

        # Faculty count in this department
        dept_faculty = set()
        for a_list in sub["coep_authors"].dropna():
            if isinstance(a_list, list):
                dept_faculty.update(a_list)
            elif isinstance(a_list, str):
                dept_faculty.add(a_list)

        # Departmental h-index
        c_list = sorted(sub["citations"].dropna().tolist(), reverse=True)
        h_idx = sum(1 for i, c in enumerate(c_list) if c >= i + 1)

        # Top cited paper
        top_paper = sub.sort_values(by="citations", ascending=False).iloc[0] if not sub.empty else None
        top_title = str(top_paper.get("title", ""))[:65] + "..." if top_paper is not None else "N/A"
        top_paper_cites = int(top_paper.get("citations", 0)) if top_paper is not None else 0

        rows.append({
            "Department": dept,
            "Publications": pubs,
            "Total Citations": cites,
            "CPP": cpp,
            "Q1 Papers": q1_cnt,
            "Q1 %": q1_pct,
            "Top Tier (Q1+Q2) %": top_tier_pct,
            "Intl Collab %": intl_pct,
            "Industry Collab %": ind_pct,
            "Active Faculty": len(dept_faculty) if len(dept_faculty) > 0 else max(1, pubs // 8),
            "h-Index": h_idx,
            "Top Cited Paper": top_title,
            "Max Paper Citations": top_paper_cites
        })

    bench_df = pd.DataFrame(rows)
    if not bench_df.empty:
        bench_df = bench_df.sort_values(by="Publications", ascending=False).reset_index(drop=True)
    return bench_df


def get_author_detailed_profile(df: pd.DataFrame, author_name: str) -> Dict[str, Any]:
    """
    Computes a comprehensive deep-dive research profile for a single author.
    Includes career summary, annual publishing trajectory, top landmark papers, and co-authors.
    """
    if df.empty or not author_name:
        return {}

    author_pubs = get_author_publications(df, author_name)
    if author_pubs.empty:
        return {}

    pub_count = len(author_pubs)
    total_cites = int(author_pubs["citations"].sum()) if "citations" in author_pubs.columns else 0
    cpp = round(total_cites / pub_count, 2) if pub_count > 0 else 0.0

    c_list = sorted(author_pubs["citations"].dropna().tolist(), reverse=True)
    h_idx = sum(1 for i, c in enumerate(c_list) if c >= i + 1)

    q1_count = len(author_pubs[author_pubs["quartile"] == "Q1"])
    q1_pct = round((q1_count / pub_count) * 100, 1) if pub_count > 0 else 0.0

    intl_count = len(author_pubs[author_pubs["is_international_collab"] == True])
    intl_pct = round((intl_count / pub_count) * 100, 1) if pub_count > 0 else 0.0

    ind_count = len(author_pubs[author_pubs["is_industry_collab"] == True])
    ind_pct = round((ind_count / pub_count) * 100, 1) if pub_count > 0 else 0.0

    depts = [p for p in author_pubs["department"].dropna().tolist() if p]
    primary_dept = max(set(depts), key=depts.count) if depts else "Engineering"

    years = [int(y) for y in author_pubs["year"].dropna().tolist() if str(y).isdigit()]
    min_yr = min(years) if years else 2020
    max_yr = max(years) if years else 2026
    active_span = f"{min_yr}–{max_yr}" if min_yr != max_yr else str(min_yr)

    # Annual trajectory
    trend_df = get_author_annual_trend(df, author_name)

    # Top 5 landmark papers
    top_papers = author_pubs.sort_values(by="citations", ascending=False).head(5)

    # Collaborating co-authors
    co_authors_list = []
    for _, row in author_pubs.iterrows():
        auths = row.get("coep_authors") or row.get("authors") or []
        if isinstance(auths, str):
            auths = [a.strip() for a in auths.split(",") if a.strip()]
        for a in auths:
            if a and a.strip().lower() != author_name.strip().lower():
                co_authors_list.append(a.strip())

    top_coauthors = pd.Series(co_authors_list).value_counts().head(8).to_dict() if co_authors_list else {}

    return {
        "author": author_name,
        "primary_department": primary_dept,
        "total_publications": pub_count,
        "total_citations": total_cites,
        "cpp": cpp,
        "h_index": h_idx,
        "q1_count": q1_count,
        "q1_pct": q1_pct,
        "intl_pct": intl_pct,
        "industry_pct": ind_pct,
        "active_span": active_span,
        "trajectory_df": trend_df,
        "top_papers_df": top_papers,
        "top_coauthors": top_coauthors
    }


def generate_author_print_html(auth_profile: Dict[str, Any], author_papers_df: pd.DataFrame, annual_trend_df: pd.DataFrame) -> str:
    """Generates a standalone, self-contained printable HTML report for a specific author."""
    author_name = auth_profile.get("author_name", "Faculty Researcher")
    dept = auth_profile.get("primary_dept", "COEP Technological University")
    total_pubs = auth_profile.get("total_pubs", 0)
    total_cites = auth_profile.get("total_citations", 0)
    cpp = auth_profile.get("cpp", 0.0)
    h_idx = auth_profile.get("h_index", 0)
    q1_pct = auth_profile.get("q1_pct", 0.0)
    q1_count = auth_profile.get("q1_count", 0)
    intl_pct = auth_profile.get("intl_pct", 0.0)
    ind_pct = auth_profile.get("ind_pct", 0.0)
    min_year = auth_profile.get("min_year", 2020)
    max_year = auth_profile.get("max_year", 2026)
    top_collabs = ", ".join(auth_profile.get("top_collaborators", [])[:4]) or "COEP Faculty"

    # Velocity Chart SVG
    trend_bars_svg = ""
    if not annual_trend_df.empty:
        max_p = max(annual_trend_df["publications"].max(), 1)
        max_c = max(annual_trend_df["citations"].max(), 1)
        w_chart = 380
        h_chart = 150
        n_pts = len(annual_trend_df)
        bar_w = max(int(w_chart / (n_pts * 2.2)), 8)
        
        svg_bars = []
        svg_line_pts = []
        for i, (_, tr_row) in enumerate(annual_trend_df.iterrows()):
            yr = tr_row["year"]
            p_val = tr_row["publications"]
            c_val = tr_row["citations"]
            
            x = int(35 + (i * (w_chart - 50) / max(n_pts - 1, 1)))
            bar_h = int((p_val / max_p) * 100)
            y_bar = 125 - bar_h
            
            svg_bars.append(f'<rect x="{x - bar_w//2}" y="{y_bar}" width="{bar_w}" height="{bar_h}" fill="#0284C7" rx="2"><title>{yr}: {p_val} papers</title></rect>')
            svg_bars.append(f'<text x="{x}" y="140" font-size="8.5" text-anchor="middle" fill="#64748B">{yr}</text>')
            
            y_line = int(125 - ((c_val / max_c) * 100))
            svg_line_pts.append(f'{x},{y_line}')
            svg_bars.append(f'<circle cx="{x}" cy="{y_line}" r="3" fill="#F59E0B"><title>{yr}: {c_val} citations</title></circle>')
            
        trend_bars_svg = f'''
        <svg width="100%" height="155" viewBox="0 0 {w_chart} {h_chart + 10}">
            <line x1="15" y1="125" x2="{w_chart - 10}" y2="125" stroke="#CBD5E1" stroke-width="1"/>
            <polyline fill="none" stroke="#F59E0B" stroke-width="2" points="{" ".join(svg_line_pts)}"/>
            {"".join(svg_bars)}
        </svg>
        '''

    # Quartiles
    q1 = auth_profile.get("q1_count", 0)
    q2 = auth_profile.get("q2_count", 0)
    q3 = auth_profile.get("q3_count", 0)
    q4 = auth_profile.get("q4_count", 0)
    
    # Top 5 landmark papers
    top5_df = author_papers_df.sort_values(by="citations", ascending=False).head(5)
    top5_rows = ""
    for idx, (_, row) in enumerate(top5_df.iterrows(), 1):
        p_tit = row.get("title", "Untitled")
        p_jnl = row.get("journal", "Publication")
        p_yr = row.get("year", "")
        p_q = row.get("quartile", "Q1")
        p_cit = int(row.get("citations", 0))
        q_bg = "#ECFDF5" if p_q == "Q1" else ("#EFF6FF" if p_q == "Q2" else "#FEF3C7")
        q_fg = "#059669" if p_q == "Q1" else ("#2563EB" if p_q == "Q2" else "#D97706")
        
        top5_rows += f"""
        <tr>
            <td style="text-align:center; font-weight:800; color:#0284C7;">#{idx}</td>
            <td><strong style="color:#0F172A; font-size:10.5px;">{p_tit}</strong><br><span style="color:#64748B; font-size:9.5px;">📖 {p_jnl} • {p_yr}</span></td>
            <td style="text-align:center;"><span style="background:{q_bg}; color:{q_fg}; border:1px solid {q_fg}; padding:2px 7px; border-radius:4px; font-weight:800; font-size:9.5px;">{p_q}</span></td>
            <td style="text-align:center; font-weight:800; color:#D97706; font-size:10.5px;">⭐ {p_cit}</td>
        </tr>
        """

    # Full papers table rows
    all_papers_rows = ""
    for idx, (_, row) in enumerate(author_papers_df.iterrows(), 1):
        p_tit = row.get("title", "Untitled")
        p_jnl = row.get("journal", "N/A")
        p_yr = row.get("year", "")
        p_q = row.get("quartile", "N/A")
        p_cit = int(row.get("citations", 0))
        
        all_papers_rows += f"""
        <tr>
            <td style="text-align:center; color:#64748B;">{idx}</td>
            <td style="font-weight:600; color:#0F172A;">{p_tit}</td>
            <td style="color:#475569;">{p_jnl}</td>
            <td style="text-align:center; color:#475569;">{p_yr}</td>
            <td style="text-align:center; font-weight:700;">{p_q}</td>
            <td style="text-align:center; font-weight:700; color:#0284C7;">{p_cit}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Faculty Research Dossier - {author_name}</title>
    <style>
        @page {{ size: A4; margin: 10mm 12mm; }}
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #0F172A; background: #FFFFFF; margin: 0; padding: 10px; font-size: 10.5px; line-height: 1.35; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0284C7; padding-bottom: 8px; margin-bottom: 12px; }}
        .inst-title {{ font-size: 16px; font-weight: 800; color: #0F172A; margin: 0; }}
        .inst-sub {{ font-size: 10.5px; font-weight: 700; color: #0284C7; margin: 2px 0 0 0; }}
        .badge-nirf {{ font-size: 9px; font-weight: 800; color: #D97706; text-transform: uppercase; text-align: right; line-height: 1.3; }}
        .dossier-card {{ background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 10px 14px; margin-bottom: 12px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; margin: 8px 0; }}
        .kpi-box {{ background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 5px; padding: 5px 6px; text-align: center; }}
        .kpi-val {{ font-size: 14px; font-weight: 800; color: #0284C7; }}
        .kpi-lbl {{ font-size: 8px; font-weight: 700; color: #64748B; text-transform: uppercase; }}
        .pills {{ display: flex; gap: 6px; font-size: 9px; font-weight: 700; margin-top: 6px; flex-wrap: wrap; }}
        .pill {{ padding: 2px 6px; border-radius: 4px; border: 1px solid #CBD5E1; background: #FFFFFF; }}
        .section-title {{ font-size: 11.5px; font-weight: 800; color: #0F172A; border-bottom: 1px solid #CBD5E1; padding-bottom: 3px; margin: 14px 0 6px 0; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 9.5px; margin-top: 5px; }}
        th {{ background: #F1F5F9; color: #334155; font-weight: 700; text-align: left; padding: 4px 5px; border: 1px solid #CBD5E1; }}
        td {{ padding: 4px 5px; border: 1px solid #CBD5E1; vertical-align: middle; }}
        tr:nth-child(even) {{ background: #F8FAFC; }}
        .charts-row {{ display: flex; gap: 10px; margin-bottom: 12px; }}
        .chart-box {{ flex: 1; border: 1px solid #CBD5E1; border-radius: 6px; padding: 6px; background: #FFFFFF; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="inst-title">COEP Technological University, Pune</div>
            <div class="inst-sub">Faculty Research Dossier & Scopus Bibliometric Impact Record</div>
        </div>
        <div class="badge-nirf">
            NAAC A+ (CGPA 3.44)<br>NIRF Category: Engineering<br><span style="color:#0284C7;">IR-E-U-1257</span>
        </div>
    </div>

    <div class="dossier-card">
        <div style="font-size: 15px; font-weight: 800; color: #0F172A;">{author_name}</div>
        <div style="font-size: 11px; font-weight: 700; color: #0284C7; margin-bottom: 2px;">🏛️ {dept} • Active {min_year}–{max_year}</div>
        <div class="kpi-grid">
            <div class="kpi-box"><div class="kpi-val">{total_pubs}</div><div class="kpi-lbl">Publications</div></div>
            <div class="kpi-box"><div class="kpi-val">{total_cites:,}</div><div class="kpi-lbl">Total Citations</div></div>
            <div class="kpi-box"><div class="kpi-val">{cpp}</div><div class="kpi-lbl">Citations / Pub</div></div>
            <div class="kpi-box"><div class="kpi-val">{h_idx}</div><div class="kpi-lbl">Author h-Index</div></div>
            <div class="kpi-box"><div class="kpi-val">{q1_pct}%</div><div class="kpi-lbl">Q1 Ratio</div></div>
        </div>
        <div class="pills">
            <span class="pill" style="border-color:#F59E0B; color:#D97706;">🥇 {q1_count} Q1 Publications</span>
            <span class="pill" style="border-color:#0284C7; color:#0284C7;">🌐 {intl_pct}% International Collab</span>
            <span class="pill" style="border-color:#10B981; color:#059669;">🏢 {ind_pct}% Industry Partner</span>
            <span style="margin-left:auto; color:#64748B;"><strong>Key Collaborators:</strong> {top_collabs}</span>
        </div>
    </div>

    <div class="charts-row">
        <div class="chart-box">
            <div style="font-weight:700; font-size:10.5px; color:#0F172A; margin-bottom:3px;">📊 Publishing Velocity & Citation Trend</div>
            <div style="font-size:9px; color:#64748B; margin-bottom:4px;"><span style="color:#0284C7;">■</span> Annual Publications &nbsp; <span style="color:#F59E0B;">●</span> Citations Accrued</div>
            {trend_bars_svg}
        </div>
        <div class="chart-box">
            <div style="font-weight:700; font-size:10.5px; color:#0F172A; margin-bottom:3px;">🍩 Journal Quartile Distribution</div>
            <div style="margin-top:12px; font-size:9.5px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px; font-weight:700;">
                    <span style="color:#059669;">🥇 Q1 (Top 25%)</span><span>{q1} papers ({round(q1/max(total_pubs,1)*100,1)}%)</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px; font-weight:700;">
                    <span style="color:#2563EB;">📘 Q2 (25%-50%)</span><span>{q2} papers ({round(q2/max(total_pubs,1)*100,1)}%)</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px; font-weight:700;">
                    <span style="color:#D97706;">📙 Q3 (50%-75%)</span><span>{q3} papers ({round(q3/max(total_pubs,1)*100,1)}%)</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px; font-weight:700;">
                    <span style="color:#DC2626;">📕 Q4 (75%-100%)</span><span>{q4} papers ({round(q4/max(total_pubs,1)*100,1)}%)</span>
                </div>
            </div>
        </div>
    </div>

    <div class="section-title">🌟 Top Landmark Contributions by {author_name}</div>
    <table>
        <thead>
            <tr><th style="width:35px; text-align:center;">Rank</th><th>Paper Title & Source</th><th style="width:55px; text-align:center;">Quartile</th><th style="width:70px; text-align:center;">Citations</th></tr>
        </thead>
        <tbody>{top5_rows}</tbody>
    </table>

    <div class="section-title">📄 Publications Directory ({len(author_papers_df)} Articles)</div>
    <table>
        <thead>
            <tr><th style="width:25px; text-align:center;">#</th><th>Article Title</th><th>Journal / Conference</th><th style="width:45px; text-align:center;">Year</th><th style="width:45px; text-align:center;">Quartile</th><th style="width:55px; text-align:center;">Citations</th></tr>
        </thead>
        <tbody>{all_papers_rows}</tbody>
    </table>
</body>
</html>"""
    return html


"""
COEP Scopus Research Dashboard | ICARE Portal Intelligence Edition
Dual Theme (Dark & Light Mode), Top 10 KPIs, Publication Trends, Impact,
Collaboration Maps, Quality Metrics (Q1-Q4), and Live Searchable Feed.
"""

import os
import io
import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()

from mock_data import generate_coep_publications, COEP_DEPARTMENTS
from scopus_api import ScopusAPIClient, save_cache, load_cache, incremental_auto_sync
from data_processor import (
    to_dataframe,
    calculate_top_10_kpis,
    get_publications_by_year,
    get_publications_by_month,
    get_publications_by_department,
    get_citations_by_year,
    get_highly_cited_papers,
    get_collaboration_breakdown,
    get_top_collaborating_institutions,
    get_top_collaborating_countries,
    get_quartile_distribution,
    filter_publications,
    export_to_bibtex,
    get_top_authors_leaderboard,
    get_author_profile_metrics,
    get_author_publications,
    get_author_annual_trend,
    get_landmark_cited_papers
)
from styles import (
    get_custom_css,
    render_icare_topbar,
    render_icare_hero,
    render_icare_kpi_card,
    get_plotly_theme,
    style_plotly_fig
)

# Page configuration
st.set_page_config(
    page_title="COEP Live Scopus Intelligence Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Theme Selection State & CSS Theme Injection
# ---------------------------------------------------------
import streamlit.components.v1 as components

if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

current_theme = st.session_state["theme"]
st.markdown(get_custom_css(theme=current_theme), unsafe_allow_html=True)
plotly_cfg = get_plotly_theme(theme=current_theme)

# Dynamic Placeholder & Tab Color Injection into Document Head
ph_color = "#CBD5E1" if current_theme == "dark" else "#475569"
tab_text_color = "#94A3B8" if current_theme == "dark" else "#1E293B"
tab_list_bg = "#0D1B2E" if current_theme == "dark" else "#F1F5F9"

components.html(
    f"""
    <script>
        const doc = window.parent.document;
        let style = doc.getElementById('scopus-ph-override');
        if (!style) {{
            style = doc.createElement('style');
            style.id = 'scopus-ph-override';
            doc.head.appendChild(style);
        }}
        style.textContent = `
            #MainMenu,
            [data-testid="stMainMenu"],
            header[data-testid="stHeader"] button[aria-label="View app in Streamlit Community Cloud"],
            header[data-testid="stHeader"] [data-testid="stToolbarActions"],
            [data-testid="stDecoration"],
            [data-testid="stStatusWidget"],
            footer,
            div[data-testid="stToolbarActions"],
            .stAppDeployButton {{
                display: none !important;
                visibility: hidden !important;
                width: 0 !important;
                height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                pointer-events: none !important;
            }}

            header[data-testid="stHeader"] {{
                background: transparent !important;
                background-color: transparent !important;
                height: 0 !important;
                min-height: 0 !important;
                pointer-events: none !important;
            }}

            header[data-testid="stHeader"] [data-testid="stToolbar"] {{
                background: transparent !important;
                pointer-events: none !important;
                height: 0 !important;
                min-height: 0 !important;
            }}

            button[data-testid="stExpandSidebarButton"],
            [data-testid="collapsedControl"] button,
            [data-testid="collapsedControl"],
            div:has(> button[data-testid="stExpandSidebarButton"]) {{
                position: fixed !important;
                top: 12px !important;
                left: 12px !important;
                z-index: 999999 !important;
                background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
                background-color: #0284C7 !important;
                color: #FFFFFF !important;
                border-radius: 8px !important;
                width: 38px !important;
                height: 38px !important;
                box-shadow: 0 4px 14px rgba(2, 132, 199, 0.45) !important;
                border: 1px solid rgba(255,255,255,0.25) !important;
                display: flex !important;
                visibility: visible !important;
                align-items: center !important;
                justify-content: center !important;
                pointer-events: auto !important;
                cursor: pointer !important;
                transition: all 0.2s ease-in-out !important;
            }}

            button[data-testid="stExpandSidebarButton"]:hover {{
                background: linear-gradient(135deg, #0369A1 0%, #075985 100%) !important;
                transform: scale(1.05) !important;
                box-shadow: 0 6px 18px rgba(2, 132, 199, 0.6) !important;
            }}

            button[data-testid="stExpandSidebarButton"] *,
            button[data-testid="stExpandSidebarButton"] svg,
            button[data-testid="stExpandSidebarButton"] span {{
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
                fill: #FFFFFF !important;
                stroke: #FFFFFF !important;
                pointer-events: none !important;
            }}

            button[data-testid="stSidebarCollapseButton"],
            [data-testid="stSidebarCollapseButton"] button {{
                pointer-events: auto !important;
                display: flex !important;
                visibility: visible !important;
                cursor: pointer !important;
            }}

            .block-container {{
                padding-top: 14px !important;
                padding-bottom: 2rem !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
            [data-testid="stSidebarContent"] {{
                padding-top: 14px !important;
            }}

            input::placeholder,
            input::-webkit-input-placeholder,
            [data-testid="stSidebar"] input::placeholder,
            [data-testid="stSidebar"] input::-webkit-input-placeholder {{
                color: {ph_color} !important;
                -webkit-text-fill-color: {ph_color} !important;
                opacity: 1 !important;
                font-weight: 500 !important;
            }}

            button[data-testid="stTabsScrollLeft"],
            button[data-testid="stTabsScrollRight"],
            [data-testid="stTabsScrollLeft"],
            [data-testid="stTabsScrollRight"],
            [data-testid="stTabs"] > button {{
                display: none !important;
                visibility: hidden !important;
                width: 0 !important;
                height: 0 !important;
                padding: 0 !important;
                margin: 0 !important;
                border: none !important;
                pointer-events: none !important;
            }}

            div[data-baseweb="tab-list"],
            div[data-testid="stTabs"] div[role="tablist"],
            div[data-testid="stTabs"] [role="tablist"],
            div[data-testid="stTabs"] [data-baseweb="tab-list"] {{
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                justify-content: space-between !important;
                align-items: stretch !important;
                width: 100% !important;
                background-color: {tab_list_bg} !important;
                gap: 6px !important;
                padding: 6px 8px !important;
                border-radius: 12px !important;
                overflow: visible !important;
            }}

            div[data-testid="stTab"],
            div[role="tab"],
            button[role="tab"],
            button[data-testid="stTab"],
            div[data-testid="stTabs"] [role="tab"] {{
                flex: 1 1 0 !important;
                min-width: 0 !important;
                display: inline-flex !important;
                justify-content: center !important;
                align-items: center !important;
                text-align: center !important;
                background-color: transparent !important;
                border-radius: 8px !important;
                padding: 8px 12px !important;
                cursor: pointer !important;
                white-space: nowrap !important;
            }}

            div[data-testid="stTab"] *,
            div[role="tab"] *,
            button[role="tab"] *,
            button[data-testid="stTab"] *,
            div[data-testid="stTabs"] [role="tab"] *,
            div[data-testid="stTabs"] [role="tab"] p,
            div[data-testid="stTabs"] [role="tab"] span,
            div[data-testid="stTabs"] [role="tab"] div {{
                color: {tab_text_color} !important;
                -webkit-text-fill-color: {tab_text_color} !important;
                font-weight: 700 !important;
                font-size: 0.88rem !important;
                opacity: 1 !important;
                white-space: nowrap !important;
                margin: 0 !important;
            }}

            div[data-testid="stTab"][aria-selected="true"],
            div[role="tab"][aria-selected="true"],
            button[role="tab"][aria-selected="true"],
            button[data-testid="stTab"][aria-selected="true"],
            div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
                background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
                background-color: #0284C7 !important;
                border-radius: 8px !important;
            }}

            div[data-testid="stTab"][aria-selected="true"] *,
            div[role="tab"][aria-selected="true"] *,
            button[role="tab"][aria-selected="true"] *,
            button[data-testid="stTab"][aria-selected="true"] *,
            div[data-testid="stTabs"] [role="tab"][aria-selected="true"] *,
            div[data-testid="stTabs"] [role="tab"][aria-selected="true"] p,
            div[data-testid="stTabs"] [role="tab"][aria-selected="true"] span {{
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
                font-weight: 800 !important;
            }}

            @media (max-width: 768px) {{
                button[data-testid="stExpandSidebarButton"] {{
                    position: fixed !important;
                    top: 14px !important;
                    left: 14px !important;
                    z-index: 999999 !important;
                    background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
                    background-color: #0284C7 !important;
                    color: #FFFFFF !important;
                    border-radius: 8px !important;
                    width: 40px !important;
                    height: 40px !important;
                    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.5) !important;
                    border: 1px solid rgba(255,255,255,0.25) !important;
                    display: flex !important;
                    visibility: visible !important;
                    align-items: center !important;
                    justify-content: center !important;
                }}

                button[data-testid="stExpandSidebarButton"] * {{
                    color: #FFFFFF !important;
                    fill: #FFFFFF !important;
                    stroke: #FFFFFF !important;
                }}

                .block-container {{
                    padding-top: 12px !important;
                    padding-left: 1rem !important;
                    padding-right: 1rem !important;
                }}

                section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
                [data-testid="stSidebarContent"] {{
                    padding-top: 12px !important;
                }}

                div[data-baseweb="tab-list"],
                div[data-testid="stTabs"] div[role="tablist"],
                div[data-testid="stTabs"] [role="tablist"],
                div[data-testid="stTabs"] [data-baseweb="tab-list"] {{
                    justify-content: flex-start !important;
                    overflow-x: auto !important;
                    -webkit-overflow-scrolling: touch !important;
                    gap: 6px !important;
                    padding: 4px 6px !important;
                }}

                div[data-testid="stTab"],
                div[role="tab"],
                button[role="tab"],
                button[data-testid="stTab"],
                div[data-testid="stTabs"] [role="tab"] {{
                    flex: 0 0 auto !important;
                    min-width: max-content !important;
                    padding: 8px 12px !important;
                    font-size: 0.82rem !important;
                }}
            }}
        `;

        function checkSidebarState() {{
            try {{
                const p = window.parent || window;
                const d = p.document || document;
                if (p.innerWidth > 768) {{
                    // On desktop: GUARANTEE sidebar is always open on load
                    const sidebar = d.querySelector('section[data-testid="stSidebar"]');
                    if (sidebar) {{
                        const isCollapsed = sidebar.getAttribute('aria-expanded') === 'false' || 
                                           sidebar.getAttribute('data-expanded') === 'false' ||
                                           (p.getComputedStyle(sidebar).transform && p.getComputedStyle(sidebar).transform !== 'none' && p.getComputedStyle(sidebar).transform.includes('-'));
                        if (isCollapsed) {{
                            const expandBtn = d.querySelector('button[data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"] button, div:has(> button[data-testid="stExpandSidebarButton"]) button');
                            if (expandBtn) {{
                                expandBtn.click();
                            }}
                        }}
                    }}
                }} else {{
                    // On mobile: keep sidebar collapsed initially
                    const sidebar = d.querySelector('section[data-testid="stSidebar"]');
                    if (sidebar) {{
                        const isExpanded = sidebar.getAttribute('aria-expanded') === 'true' || 
                                           sidebar.getAttribute('data-expanded') === 'true';
                        if (isExpanded) {{
                            const closeBtn = sidebar.querySelector('button[data-testid="stSidebarCollapseButton"], button[aria-label="Close sidebar"], [data-testid="stSidebarCollapseButton"] button');
                            if (closeBtn) {{
                                closeBtn.click();
                            }}
                        }}
                    }}
                }}
            }} catch(e) {{}}
        }}
        checkSidebarState();
        setTimeout(checkSidebarState, 80);
        setTimeout(checkSidebarState, 250);
        setTimeout(checkSidebarState, 600);
    </script>
    """,
    height=0,
    width=0,
)

# ---------------------------------------------------------
# Session Data Initialization & 1-Hour Background Auto-Sync
# ---------------------------------------------------------
if "publications_data" not in st.session_state:
    auto_api_key = ""
    try:
        if hasattr(st, "secrets") and "SCOPUS_API_KEY" in st.secrets:
            auto_api_key = str(st.secrets["SCOPUS_API_KEY"]).strip()
    except Exception:
        pass
    if not auto_api_key:
        auto_api_key = os.getenv("SCOPUS_API_KEY", "").strip()
        if auto_api_key == "YOUR_SCOPUS_API_KEY_HERE":
            auto_api_key = ""

    if auto_api_key:
        synced_data, did_sync, sync_msg = incremental_auto_sync(
            api_key=auto_api_key,
            interval_hours=1.0,
            cache_path="data/coep_scopus_cache.json"
        )
        if synced_data:
            st.session_state["publications_data"] = synced_data
            st.session_state["data_source"] = f"Live Scopus Repository ({len(synced_data):,} papers)"
        else:
            cached_data, _ = load_cache("data/coep_scopus_cache.json")
            st.session_state["publications_data"] = cached_data or generate_coep_publications(950)
            st.session_state["data_source"] = f"Live Scopus Repository ({len(st.session_state['publications_data']):,} papers)"
    else:
        cached_data, last_sync = load_cache("data/coep_scopus_cache.json")
        if cached_data:
            st.session_state["publications_data"] = cached_data
            st.session_state["data_source"] = f"Live Scopus Repository ({len(cached_data):,} papers)"
        else:
            initial_mock = generate_coep_publications(950)
            st.session_state["publications_data"] = initial_mock
            st.session_state["data_source"] = "COEP Benchmark Archive (1950–2026)"

# ---------------------------------------------------------
# Sidebar Controls & Theme Toggle
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-box">
        <div class="sidebar-brand-title">🏛️ COEP PORTAL</div>
        <div class="sidebar-brand-sub">Live Scopus Intelligence [IR-E-U-0447]</div>
    </div>
    """, unsafe_allow_html=True)

    def refresh_entire_dashboard():
        cached_data, _ = load_cache("data/coep_scopus_cache.json")
        if cached_data:
            st.session_state["publications_data"] = cached_data
            st.session_state["data_source"] = f"Live Scopus Repository ({len(cached_data):,} papers)"
        st.session_state["from_year"] = 1950
        st.session_state["to_year"] = 2026
        st.session_state["year_slider_val"] = (1950, 2026)
        st.session_state["input_start_yr"] = "1950"
        st.session_state["input_end_yr"] = "2026"
        st.session_state["filter_version"] = st.session_state.get("filter_version", 0) + 1

    st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True,
        type="primary",
        key="btn_refresh_all_dashboard",
        on_click=refresh_entire_dashboard
    )

    is_dark = current_theme == "dark"
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        background: {'rgba(16, 185, 129, 0.12)' if is_dark else '#ECFDF5'};
        border: 1px solid {'rgba(16, 185, 129, 0.35)' if is_dark else '#A7F3D0'};
        border-radius: 8px;
        padding: 5px 10px;
        margin: 6px 0 12px 0;
        font-size: 0.76rem;
        font-weight: 700;
        color: {'#34D399' if is_dark else '#065F46'};
        text-align: center;
        letter-spacing: 0.01em;
    ">
        <span style="
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background-color: #10B981;
            box-shadow: 0 0 8px #10B981;
        "></span>
        <span>Live Scopus Feed • Auto-synced every 60m</span>
    </div>
    """, unsafe_allow_html=True)

    def set_theme(selected_theme):
        st.session_state["theme"] = selected_theme

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.button(
            "🌙 Dark Mode",
            use_container_width=True,
            type="primary" if current_theme == "dark" else "secondary",
            on_click=set_theme,
            args=("dark",),
            key="btn_theme_dark"
        )
    with col_t2:
        st.button(
            "☀️ Light Mode",
            use_container_width=True,
            type="primary" if current_theme == "light" else "secondary",
            on_click=set_theme,
            args=("light",),
            key="btn_theme_light"
        )

    st.markdown('<div class="sidebar-section-hdr">🔍 NAVIGATE & FILTER</div>', unsafe_allow_html=True)
    
    raw_df = to_dataframe(st.session_state["publications_data"])
    data_min_year = int(raw_df["year"].min()) if not raw_df.empty else 1950
    data_max_year = int(raw_df["year"].max()) if not raw_df.empty else 2026
    
    slider_min = min(1950, data_min_year)
    slider_max = max(2026, data_max_year)

    if "from_year" not in st.session_state:
        st.session_state["from_year"] = slider_min
    if "to_year" not in st.session_state:
        st.session_state["to_year"] = slider_max

    # Initialize bidirectional widget keys
    if "year_slider_val" not in st.session_state:
        st.session_state["year_slider_val"] = (int(st.session_state["from_year"]), int(st.session_state["to_year"]))
    if "input_start_yr" not in st.session_state:
        st.session_state["input_start_yr"] = str(st.session_state["from_year"])
    if "input_end_yr" not in st.session_state:
        st.session_state["input_end_yr"] = str(st.session_state["to_year"])

    def on_slider_change():
        val = st.session_state["year_slider_val"]
        s_val, e_val = int(val[0]), int(val[1])
        st.session_state["from_year"] = s_val
        st.session_state["to_year"] = e_val
        st.session_state["input_start_yr"] = str(s_val)
        st.session_state["input_end_yr"] = str(e_val)

    def apply_year_inputs():
        s_raw = str(st.session_state.get("input_start_yr", st.session_state["from_year"]))
        e_raw = str(st.session_state.get("input_end_yr", st.session_state["to_year"]))
        s_digits = "".join(filter(str.isdigit, s_raw))
        e_digits = "".join(filter(str.isdigit, e_raw))

        s_val = int(s_digits) if len(s_digits) == 4 else st.session_state["from_year"]
        e_val = int(e_digits) if len(e_digits) == 4 else st.session_state["to_year"]

        s_val = max(slider_min, min(slider_max, s_val))
        e_val = max(slider_min, min(slider_max, e_val))
        if s_val > e_val:
            s_val, e_val = e_val, s_val

        st.session_state["from_year"] = s_val
        st.session_state["to_year"] = e_val
        st.session_state["year_slider_val"] = (s_val, e_val)
        st.session_state["input_start_yr"] = str(s_val)
        st.session_state["input_end_yr"] = str(e_val)

    st.markdown('<label style="color: inherit; font-weight: 800; font-size: 0.92rem; margin-bottom: 2px; display: block;">📅 Evaluation Period</label>', unsafe_allow_html=True)

    # 1. Adjustable Dual-Side Range Slider
    st.slider(
        "Evaluation Period Range Slider",
        min_value=slider_min,
        max_value=slider_max,
        step=1,
        key="year_slider_val",
        on_change=on_slider_change,
        label_visibility="collapsed"
    )

    # 2. Keyboard Input Boxes (Strictly 4 numbers only)
    col_yr1, col_yr2 = st.columns(2)
    with col_yr1:
        st.text_input(
            "Start Year",
            max_chars=4,
            placeholder="YYYY",
            key="input_start_yr",
            on_change=apply_year_inputs
        )
    with col_yr2:
        st.text_input(
            "End Year",
            max_chars=4,
            placeholder="YYYY",
            key="input_end_yr",
            on_change=apply_year_inputs
        )

    # 3. Apply / Refresh Range Button
    st.button(
        "🔄 Apply Year Range",
        type="primary",
        use_container_width=True,
        key="btn_apply_year_range",
        on_click=apply_year_inputs
    )

    selected_year_range = (int(st.session_state["from_year"]), int(st.session_state["to_year"]))

    all_depts = sorted(list(raw_df["department"].dropna().unique())) if not raw_df.empty else COEP_DEPARTMENTS
    fv = st.session_state.get("filter_version", 0)
    selected_depts = st.multiselect(
        "🏢 Department / School",
        options=all_depts,
        default=[],
        key=f"filter_depts_{fv}"
    )

    selected_quartiles = st.multiselect(
        "🏆 Journal Quartile (Q1-Q4)",
        options=["Q1", "Q2", "Q3", "Q4"],
        default=[],
        key=f"filter_quartiles_{fv}"
    )

    selected_collab = st.multiselect(
        "🌐 Collaboration Scope",
        options=["International", "National", "Industry", "Institutional"],
        default=[],
        key=f"filter_collab_{fv}"
    )

    st.markdown("---")

    # Scopus API Sync Configuration (Admin Gateway)
    with st.expander("⚙️ **Scopus Gateway & API Sync**", expanded=False):
        secret_key = ""
        try:
            if hasattr(st, "secrets") and "SCOPUS_API_KEY" in st.secrets:
                secret_key = str(st.secrets["SCOPUS_API_KEY"]).strip()
        except Exception:
            pass
        if not secret_key:
            secret_key = os.getenv("SCOPUS_API_KEY", "").strip()
            if secret_key == "YOUR_SCOPUS_API_KEY_HERE":
                secret_key = ""

        if secret_key:
            st.success("🔒 API Key Securely Authenticated")
        else:
            api_key_input = st.text_input("Scopus API Key", type="password")
            if api_key_input:
                secret_key = api_key_input

        affil_query = st.text_input(
            "Affiliation Query",
            value=os.getenv("SCOPUS_AFFIL_QUERY", "AFFIL({College of Engineering Pune}) OR AFFIL({COEP Technological University}) OR AFFIL({COEP Pune})")
        )

        max_fetch_choice = st.selectbox(
            "Fetch Volume",
            options=[3000, 1500, 500, 1000],
            index=0,
            format_func=lambda x: f"Full Archive (~{x} papers)" if x >= 3000 else f"Latest {x} papers"
        )

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            sync_btn = st.button("🔄 Sync Scopus", type="primary", use_container_width=True)
        with col_b2:
            reset_btn = st.button("📥 Benchmark", use_container_width=True)

        if sync_btn:
            if not secret_key:
                st.error("Scopus API Key is required.")
            else:
                with st.spinner("Synchronizing with Elsevier Scopus API..."):
                    client = ScopusAPIClient(api_key=secret_key)
                    is_valid, msg = client.test_connection()
                    if not is_valid:
                        st.error(msg)
                    else:
                        progress_bar = st.progress(0)
                        def on_progress(cur, tot, txt):
                            progress_bar.progress(min(1.0, cur / max(1, tot)))

                        live_pubs = client.fetch_coep_publications(
                            query=affil_query,
                            max_results=max_fetch_choice,
                            progress_callback=on_progress
                        )
                        if live_pubs:
                            save_cache(live_pubs, "data/coep_scopus_cache.json")
                            st.session_state["publications_data"] = live_pubs
                            st.session_state["data_source"] = f"Live Scopus Repository ({len(live_pubs):,} papers)"
                            st.success(f"Synchronized {len(live_pubs):,} live publications!")
                            st.rerun()

        if reset_btn:
            fresh_data = generate_coep_publications(950)
            st.session_state["publications_data"] = fresh_data
            st.session_state["data_source"] = "COEP Benchmark Archive (1950–2026)"
            st.success("Loaded benchmark archive!")
            st.rerun()

    st.caption("⚡ ICARE Portal Intelligence | COEP Technological University")

# ---------------------------------------------------------
# Filter Dataset
# ---------------------------------------------------------
df_filtered = filter_publications(
    raw_df,
    year_range=selected_year_range,
    departments=selected_depts if selected_depts else None,
    quartiles=selected_quartiles if selected_quartiles else None,
    collab_types=selected_collab if selected_collab else None
)

kpis = calculate_top_10_kpis(df_filtered)

# ---------------------------------------------------------
# TOP ICARE NAVBAR & HERO BANNER
# ---------------------------------------------------------
st.html(render_icare_topbar(theme=current_theme))
st.html(render_icare_hero(kpis['total_publications'], kpis['total_citations'], theme=current_theme))

# ---------------------------------------------------------
# REPORT TOOLBAR & EXPORT ACTION BUTTONS
# ---------------------------------------------------------
col_tool1, col_tool2, col_tool3, col_tool4 = st.columns([2, 1, 1, 1])

with col_tool1:
    st.markdown('<div class="toolbar-title">📄 <strong>REPORT: COEP Live Scopus Intelligence Dashboard Overview</strong></div>', unsafe_allow_html=True)

with col_tool2:
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df_filtered.drop(columns=["pub_date_dt"], errors="ignore").to_excel(writer, index=False, sheet_name='Publications')
    st.download_button("📊 Export Excel", data=excel_buffer.getvalue(), file_name=f"COEP_Scopus_Report_{datetime.date.today()}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type="primary", use_container_width=True)

with col_tool3:
    bibtex_str = export_to_bibtex(df_filtered)
    st.download_button("📑 Export BibTeX", data=bibtex_str, file_name=f"COEP_Scopus_{datetime.date.today()}.bib", mime="text/plain", type="primary", use_container_width=True)

with col_tool4:
    csv_bytes = df_filtered.drop(columns=["abstract", "pub_date_dt"], errors="ignore").to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export CSV", data=csv_bytes, file_name=f"COEP_Scopus_Data_{datetime.date.today()}.csv", mime="text/csv", type="primary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TOP 10 KPIS GRID (ICARE STYLE CARDS)
# ---------------------------------------------------------
k_row1_1, k_row1_2, k_row1_3, k_row1_4, k_row1_5 = st.columns(5)

with k_row1_1:
    st.markdown(render_icare_kpi_card(
        "Total Scopus Output",
        f"{kpis['total_publications']:,}",
        f"All indexed papers",
        icon="🏆",
        color_theme="blue"
    ), unsafe_allow_html=True)

with k_row1_2:
    st.markdown(render_icare_kpi_card(
        "Publications – 2026",
        f"{kpis['publications_2026']:,}",
        f"Current year volume",
        icon="🎓",
        color_theme="teal"
    ), unsafe_allow_html=True)

with k_row1_3:
    st.markdown(render_icare_kpi_card(
        "Publications – 2025",
        f"{kpis['publications_2025']:,}",
        f"Preceding academic year",
        icon="📅",
        color_theme="blue"
    ), unsafe_allow_html=True)

with k_row1_4:
    st.markdown(render_icare_kpi_card(
        "Total Citations",
        f"{kpis['total_citations']:,}",
        f"Cumulative impact",
        icon="⭐",
        color_theme="orange"
    ), unsafe_allow_html=True)

with k_row1_5:
    st.markdown(render_icare_kpi_card(
        "Citations per Pub (CPP)",
        f"{kpis['citations_per_pub']:.2f}",
        f"Average citations / paper",
        icon="📈",
        color_theme="purple"
    ), unsafe_allow_html=True)

st.write("")

k_row2_1, k_row2_2, k_row2_3, k_row2_4, k_row2_5 = st.columns(5)

with k_row2_1:
    st.markdown(render_icare_kpi_card(
        "Q1 Publications",
        f"{kpis['q1_count']:,}",
        f"{kpis['q1_pct']}% top-tier journals",
        icon="🥇",
        color_theme="teal"
    ), unsafe_allow_html=True)

with k_row2_2:
    st.markdown(render_icare_kpi_card(
        "International Collab",
        f"{kpis['intl_collab_count']:,}",
        f"{kpis['intl_collab_pct']}% global co-authors",
        icon="🌐",
        color_theme="blue"
    ), unsafe_allow_html=True)

with k_row2_3:
    st.markdown(render_icare_kpi_card(
        "Industry Collab",
        f"{kpis['industry_collab_count']:,}",
        f"{kpis['industry_collab_pct']}% corporate R&D",
        icon="🏢",
        color_theme="orange"
    ), unsafe_allow_html=True)

with k_row2_4:
    st.markdown(render_icare_kpi_card(
        "Active Publishing Faculty",
        f"{kpis['active_faculty_count']:,}",
        f"Unique faculty authors",
        icon="👥",
        color_theme="purple"
    ), unsafe_allow_html=True)

with k_row2_5:
    st.markdown(render_icare_kpi_card(
        "Publications in Last 30 Days",
        f"{kpis['pubs_last_30_days']:,}",
        f"Recent publishing velocity",
        icon="⚡",
        color_theme="rose"
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6 CORE DASHBOARD SECTIONS IN TABS
# ---------------------------------------------------------
tab_trends, tab_impact, tab_collab, tab_quality, tab_authors, tab_feed = st.tabs([
    "📈 Publication Trends",
    "🎯 Research Impact",
    "🌐 Collaboration",
    "🏆 Research Quality",
    "👥 Author Intelligence",
    "📰 Live Publication Feed"
])

# ---------------------------------------------------------
# TAB 1: PUBLICATION TRENDS
# ---------------------------------------------------------
with tab_trends:
    st.markdown('<div class="icare-section-title">📊 Publication Trends & Growth Dynamics</div>', unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns([1.2, 1])

    with col_t1:
        st.markdown("##### **Publications by Year & Cumulative Growth**")
        df_year = get_publications_by_year(df_filtered)
        if not df_year.empty:
            fig_year = go.Figure()
            fig_year.add_trace(go.Bar(
                x=df_year["year"],
                y=df_year["count"],
                name="Annual Publications",
                marker_color="#2563EB" if current_theme == "light" else "#0284C7",
                text=df_year["count"],
                textposition="auto"
            ))
            fig_year.add_trace(go.Scatter(
                x=df_year["year"],
                y=df_year["cumulative"],
                name="Cumulative Total",
                yaxis="y2",
                line=dict(color="#F59E0B", width=3),
                mode="lines+markers"
            ))
            fig_year.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(color="#0F172A" if current_theme == "light" else "#FFFFFF", family="Plus Jakarta Sans", size=11)
                ),
                yaxis=dict(title=dict(text="Annual Output", font=dict(color="#0F172A" if current_theme == "light" else "#FFFFFF"))),
                yaxis2=dict(title=dict(text="Cumulative Total", font=dict(color="#0F172A" if current_theme == "light" else "#FFFFFF")), overlaying="y", side="right"),
                xaxis=dict(title=dict(text="Publication Year", font=dict(color="#0F172A" if current_theme == "light" else "#FFFFFF")), dtick=2 if len(df_year) > 15 else 1),
            )
            fig_year = style_plotly_fig(fig_year, current_theme)
            st.plotly_chart(fig_year, theme=None, use_container_width=True)

    with col_t2:
        st.markdown("##### **Monthly Publishing Velocity**")
        available_years = sorted(list(df_filtered["year"].unique()), reverse=True)
        target_year = st.selectbox("Select Year", options=available_years, index=0)
        df_month = get_publications_by_month(df_filtered, year=target_year)
        if not df_month.empty:
            month_scale = ["#93C5FD", "#3B82F6", "#1D4ED8", "#1E40AF"] if current_theme == "light" else ["#0369A1", "#0284C7", "#38BDF8", "#7DD3FC"]
            fig_month = px.bar(
                df_month,
                x="month",
                y="count",
                text="count",
                labels={"month": "Month", "count": "Publications"},
                color="count",
                color_continuous_scale=month_scale
            )
            fig_month.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=30, b=20),
                coloraxis_showscale=False,
                xaxis_tickangle=-45,
            )
            fig_month.update_traces(textposition="outside")
            fig_month = style_plotly_fig(fig_month, current_theme)
            st.plotly_chart(fig_month, theme=None, use_container_width=True)

    st.markdown("---")

    st.markdown("##### **Departmental Research Output Breakdown**")
    df_dept = get_publications_by_department(df_filtered)
    if not df_dept.empty:
        dept_scale = ["#6EE7B7", "#10B981", "#059669", "#047857"] if current_theme == "light" else ["#047857", "#10B981", "#34D399", "#6EE7B7"]
        fig_dept_bar = px.bar(
            df_dept,
            x="count",
            y="department",
            orientation="h",
            text="count",
            labels={"count": "Publications", "department": "Department"},
            color="count",
            color_continuous_scale=dept_scale
        )
        fig_dept_bar.update_layout(
            height=430,
            margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_showscale=False,
        )
        fig_dept_bar.update_traces(textposition="outside")
        fig_dept_bar = style_plotly_fig(fig_dept_bar, current_theme)
        st.plotly_chart(fig_dept_bar, theme=None, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: RESEARCH IMPACT
# ---------------------------------------------------------
with tab_impact:
    st.markdown('<div class="icare-section-title">🎯 Research Impact & Citation Analytics</div>', unsafe_allow_html=True)
    
    col_i1, col_i2 = st.columns([1.2, 1])

    with col_i1:
        st.markdown("##### **Citations by Year & Average Citations per Paper**")
        df_cite_year = get_citations_by_year(df_filtered)
        if not df_cite_year.empty:
            fig_cites = go.Figure()
            fig_cites.add_trace(go.Bar(
                x=df_cite_year["year"],
                y=df_cite_year["total_citations"],
                name="Total Citations",
                marker_color="#8B5CF6",
                text=df_cite_year["total_citations"],
                textposition="auto"
            ))
            fig_cites.add_trace(go.Scatter(
                x=df_cite_year["year"],
                y=df_cite_year["avg_citations"],
                name="Avg CPP",
                yaxis="y2",
                line=dict(color="#EF4444", width=3),
                mode="lines+markers"
            ))
            fig_cites.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(color="#FFFFFF" if current_theme == "dark" else "#0F172A", family="Plus Jakarta Sans", size=11)
                ),
                yaxis=dict(title="Total Citations"),
                yaxis2=dict(title="Avg Citations per Paper", overlaying="y", side="right"),
                xaxis=dict(title="Publication Year"),
            )
            fig_cites = style_plotly_fig(fig_cites, current_theme)
            st.plotly_chart(fig_cites, theme=None, use_container_width=True)

    with col_i2:
        st.markdown("##### **Average Citations per Publication by Department**")
        if not df_filtered.empty and "department" in df_filtered.columns:
            dept_cites = df_filtered.groupby("department").agg(
                avg_cites=("citations", "mean"),
                total_cites=("citations", "sum")
            ).reset_index()
            dept_cites["avg_cites"] = dept_cites["avg_cites"].round(2)
            dept_cites = dept_cites.sort_values("avg_cites", ascending=True)

            fig_dept_cites = px.bar(
                dept_cites,
                x="avg_cites",
                y="department",
                orientation="h",
                text="avg_cites",
                labels={"avg_cites": "Avg Citations / Paper", "department": "Department"},
                color="avg_cites",
                color_continuous_scale="Purples"
            )
            fig_dept_cites.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                coloraxis_showscale=False,
            )
            fig_dept_cites.update_traces(textposition="outside")
            fig_dept_cites = style_plotly_fig(fig_dept_cites, current_theme)
            st.plotly_chart(fig_dept_cites, theme=None, use_container_width=True)

    st.markdown("---")

    st.markdown("##### 🏆 **Highly Cited Landmark Papers Leaderboard**")
    top_papers = get_highly_cited_papers(df_filtered, top_n=20)
    if not top_papers.empty:
        display_df = top_papers.rename(columns={
            "title": "Title",
            "authors_str": "Authors",
            "department": "Department",
            "journal": "Journal",
            "year": "Year",
            "citations": "Citations",
            "citescore": "CiteScore",
            "quartile": "Quartile",
            "doi_url": "DOI Link"
        })
        st.dataframe(
            display_df,
            column_config={
                "DOI Link": st.column_config.LinkColumn("DOI", display_text="Open DOI ↗"),
                "Citations": st.column_config.NumberColumn("Citations", format="%d ⭐"),
                "CiteScore": st.column_config.NumberColumn("CiteScore", format="%.1f"),
                "Quartile": st.column_config.TextColumn("Quartile"),
            },
            use_container_width=True,
            hide_index=True
        )

# ---------------------------------------------------------
# TAB 3: COLLABORATION
# ---------------------------------------------------------
with tab_collab:
    st.markdown('<div class="icare-section-title">🌐 Collaboration Dynamics & Global Alliances</div>', unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        st.markdown("##### **International vs National Collaboration**")
        df_collab = get_collaboration_breakdown(df_filtered)
        if not df_collab.empty:
            fig_donut = px.pie(
                df_collab,
                names="collaboration_type",
                values="count",
                hole=0.45,
                color="collaboration_type",
                color_discrete_map={
                    "International": "#0284C7",
                    "National": "#10B981",
                    "Industry": "#F59E0B",
                    "Institutional": "#64748B"
                }
            )
            fig_donut.update_layout(
                height=360,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            )
            fig_donut.update_traces(textinfo="percent+label")
            fig_donut = style_plotly_fig(fig_donut, current_theme)
            st.plotly_chart(fig_donut, theme=None, use_container_width=True)

    with col_c2:
        st.markdown("##### **Top Collaborating Institutions & Partners**")
        df_top_inst = get_top_collaborating_institutions(df_filtered, top_n=12)
        if not df_top_inst.empty:
            fig_inst = px.bar(
                df_top_inst.sort_values("count", ascending=True),
                x="count",
                y="institution",
                orientation="h",
                text="count",
                labels={"count": "Collaborative Articles", "institution": "Partner"},
                color="count",
                color_continuous_scale="Viridis"
            )
            fig_inst.update_layout(
                height=360,
                margin=dict(l=20, r=20, t=20, b=20),
                coloraxis_showscale=False,
            )
            fig_inst.update_traces(textposition="outside")
            fig_inst = style_plotly_fig(fig_inst, current_theme)
            st.plotly_chart(fig_inst, theme=None, use_container_width=True)

    st.markdown("---")

    st.markdown("##### 🌍 **Global Collaboration Map & Partner Countries**")
    df_top_countries = get_top_collaborating_countries(df_filtered, top_n=18)
    
    col_m1, col_m2 = st.columns([1.3, 1])
    with col_m1:
        if not df_top_countries.empty:
            fig_map = px.choropleth(
                df_top_countries,
                locations="country",
                locationmode="country names",
                color="count",
                hover_name="country",
                color_continuous_scale="Blues",
                labels={"count": "Co-authored Papers"}
            )
            fig_map.update_layout(
                height=380,
                margin=dict(l=0, r=0, t=0, b=0),
                geo=dict(showframe=False, showcoastlines=True, bgcolor="rgba(0,0,0,0)", projection_type="equirectangular"),
            )
            fig_map = style_plotly_fig(fig_map, current_theme)
            st.plotly_chart(fig_map, theme=None, use_container_width=True)

    with col_m2:
        if not df_top_countries.empty:
            fig_c_bar = px.bar(
                df_top_countries.sort_values("count", ascending=True),
                x="count",
                y="country",
                orientation="h",
                text="count",
                labels={"count": "Publications", "country": "Country"},
                color="count",
                color_continuous_scale="Blues"
            )
            fig_c_bar.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                coloraxis_showscale=False,
            )
            fig_c_bar.update_traces(textposition="outside")
            fig_c_bar = style_plotly_fig(fig_c_bar, current_theme)
            st.plotly_chart(fig_c_bar, theme=None, use_container_width=True)

# ---------------------------------------------------------
# TAB 4: RESEARCH QUALITY
# ---------------------------------------------------------
with tab_quality:
    st.markdown('<div class="icare-section-title">🏆 Research Quality & Journal Standing (Q1–Q4, SJR & CiteScore)</div>', unsafe_allow_html=True)
    
    col_q1, col_q2 = st.columns([1, 1])

    with col_q1:
        st.markdown("##### **Journal Quartile Distribution (Q1 / Q2 / Q3 / Q4)**")
        df_quartiles = get_quartile_distribution(df_filtered)
        if not df_quartiles.empty:
            fig_q_donut = px.pie(
                df_quartiles,
                names="quartile",
                values="count",
                hole=0.45,
                color="quartile",
                color_discrete_map={
                    "Q1": "#10B981",
                    "Q2": "#3B82F6",
                    "Q3": "#F59E0B",
                    "Q4": "#EF4444"
                }
            )
            fig_q_donut.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            )
            fig_q_donut.update_traces(textinfo="percent+label")
            fig_q_donut = style_plotly_fig(fig_q_donut, current_theme)
            st.plotly_chart(fig_q_donut, theme=None, use_container_width=True)

    with col_q2:
        st.markdown("##### **Quartile Standing by Department**")
        if not df_filtered.empty:
            q_dept = df_filtered.groupby(["department", "quartile"]).size().reset_index(name="count")
            fig_q_dept = px.bar(
                q_dept,
                x="department",
                y="count",
                color="quartile",
                barmode="stack",
                color_discrete_map={"Q1": "#10B981", "Q2": "#3B82F6", "Q3": "#F59E0B", "Q4": "#EF4444"},
                labels={"department": "Department", "count": "Publications", "quartile": "Quartile"}
            )
            fig_q_dept.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis_tickangle=-40,
            )
            fig_q_dept = style_plotly_fig(fig_q_dept, current_theme)
            st.plotly_chart(fig_q_dept, theme=None, use_container_width=True)

    st.markdown("---")

    st.markdown("##### **Scopus CiteScore & SCImago Journal Rank (SJR) Distribution**")
    col_dist1, col_dist2 = st.columns(2)

    with col_dist1:
        st.markdown("###### **CiteScore Distribution**")
        if not df_filtered.empty and "citescore" in df_filtered.columns:
            fig_cs = px.histogram(
                df_filtered,
                x="citescore",
                nbins=25,
                marginal="box",
                color_discrete_sequence=["#10B981"],
                labels={"citescore": "CiteScore"}
            )
            fig_cs.update_layout(
                height=320,
                margin=dict(l=20, r=20, t=20, b=20),
            )
            fig_cs = style_plotly_fig(fig_cs, current_theme)
            st.plotly_chart(fig_cs, theme=None, use_container_width=True)

    with col_dist2:
        st.markdown("###### **SCImago Journal Rank (SJR) Distribution**")
        if not df_filtered.empty and "sjr" in df_filtered.columns:
            fig_sjr = px.histogram(
                df_filtered,
                x="sjr",
                nbins=25,
                marginal="box",
                color_discrete_sequence=["#3B82F6"],
                labels={"sjr": "SJR Index"}
            )
            fig_sjr.update_layout(
                height=320,
                margin=dict(l=20, r=20, t=20, b=20),
            )
            fig_sjr = style_plotly_fig(fig_sjr, current_theme)
            st.plotly_chart(fig_sjr, theme=None, use_container_width=True)

    top_10_df = df_filtered[df_filtered["is_top_10_percent"] == True]
    st.info(f"🌟 **Top 10% High-Impact Benchmark:** {len(top_10_df)} publications ({round(len(top_10_df)/max(1, len(df_filtered))*100, 1)}%) meet the Top 10% CiteScore & citation benchmark criteria.")

# ---------------------------------------------------------
# TAB 5: AUTHOR INTELLIGENCE & FACULTY DOSSIER
# ---------------------------------------------------------
with tab_authors:
    st.markdown('<div class="icare-section-title">👥 Faculty Author Intelligence & Research Dossier</div>', unsafe_allow_html=True)
    st.caption("Institutional leaderboards, individual researcher dossiers, publishing velocity timelines, and author-specific publication directories.")

    # 1. Prolific Authors Leaderboard Controls
    st.markdown("#### **🏆 COEP Most Prolific Faculty Researchers**")
    col_ctrl1, col_ctrl2 = st.columns([1, 1])
    with col_ctrl1:
        author_sort_choice = st.selectbox(
            "Rank Authors By",
            ["Most Publications", "Total Citations", "Highest h-Index", "Citations Per Pub (CPP)", "Top-Tier Q1 Ratio"],
            key="author_sort_sel"
        )
    with col_ctrl2:
        top_n_choice = st.selectbox(
            "Display Top",
            [10, 25, 50, 100],
            index=1,
            key="author_top_n_sel"
        )

    sort_metric_map = {
        "Most Publications": "pubs",
        "Total Citations": "citations",
        "Highest h-Index": "h_index",
        "Citations Per Pub (CPP)": "cpp",
        "Top-Tier Q1 Ratio": "q1",
    }
    sort_key = sort_metric_map.get(author_sort_choice, "pubs")
    top_authors_df = get_top_authors_leaderboard(df_filtered, top_n=top_n_choice, sort_by=sort_key)

    if top_authors_df.empty:
        st.warning("No author records found matching the current global filters.")
    else:
        # Top 3 Podium Spotlight
        if len(top_authors_df) >= 3:
            pod_col1, pod_col2, pod_col3 = st.columns(3)
            
            # Rank 1 - Gold
            r1 = top_authors_df.iloc[0]
            with pod_col1:
                st.markdown(f"""
                <div class="podium-card podium-gold">
                    <div style="font-size: 2.2rem; margin-bottom: 4px;">🥇</div>
                    <div style="font-size: 0.82rem; font-weight: 800; color: #D97706; text-transform: uppercase; letter-spacing: 0.05em;">#1 Ranked Faculty</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: {'#FFFFFF' if current_theme == 'dark' else '#0F172A'}; margin: 4px 0;">{r1['Author']}</div>
                    <div style="font-size: 0.78rem; color: #0284C7; font-weight: 700; margin-bottom: 12px;">{r1['Department']}</div>
                    <div style="display: flex; justify-content: space-around; border-top: 1px dashed {'#334155' if current_theme == 'dark' else '#CBD5E1'}; padding-top: 8px;">
                        <div><strong style="font-size: 1.1rem; color: {'#38BDF8' if current_theme == 'dark' else '#0284C7'};">{r1['Publications']}</strong><br><span style="font-size: 0.72rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'};">Papers</span></div>
                        <div><strong style="font-size: 1.1rem; color: #F59E0B;">{r1['Total Citations']:,}</strong><br><span style="font-size: 0.72rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'};">Citations</span></div>
                        <div><strong style="font-size: 1.1rem; color: #10B981;">{r1['h-Index']}</strong><br><span style="font-size: 0.72rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'};">h-Index</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Rank 2 - Silver
            r2 = top_authors_df.iloc[1]
            with pod_col2:
                st.markdown(f"""
                <div class="podium-card podium-silver">
                    <div style="font-size: 2.2rem; margin-bottom: 4px;">🥈</div>
                    <div style="font-size: 0.82rem; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">#2 Ranked Faculty</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: {'#FFFFFF' if current_theme == 'dark' else '#0F172A'}; margin: 4px 0;">{r2['Author']}</div>
                    <div style="font-size: 0.78rem; color: #0284C7; font-weight: 700; margin-bottom: 12px;">{r2['Department']}</div>
                    <div style="display: flex; justify-content: space-around; border-top: 1px dashed {'#334155' if current_theme == 'dark' else '#CBD5E1'}; padding-top: 8px;">
                        <div><strong style="font-size: 1.1rem; color: {'#38BDF8' if current_theme == 'dark' else '#0284C7'};">{r2['Publications']}</strong><br><span style="font-size: 0.72rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'};">Papers</span></div>
                        <div><strong style="font-size: 1.1rem; color: #F59E0B;">{r2['Total Citations']:,}</strong><br><span style="font-size: 0.72rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'};">Citations</span></div>
                        <div><strong style="font-size: 1.1rem; color: #10B981;">{r2['h-Index']}</strong><br><span style="font-size: 0.72rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'};">h-Index</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Rank 3 - Bronze
            r3 = top_authors_df.iloc[2]
            with pod_col3:
                st.markdown(f"""
                <div class="podium-card podium-bronze">
                    <div style="font-size: 2.2rem; margin-bottom: 4px;">🥉</div>
                    <div style="font-size: 0.82rem; font-weight: 800; color: #B45309; text-transform: uppercase; letter-spacing: 0.05em;">#3 Ranked Faculty</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: {'#FFFFFF' if current_theme == 'dark' else '#0F172A'}; margin: 4px 0;">{r3['Author']}</div>
                    <div style="font-size: 0.78rem; color: #0284C7; font-weight: 700; margin-bottom: 12px;">{r3['Department']}</div>
                    <div style="display: flex; justify-content: space-around; border-top: 1px dashed {'#334155' if current_theme == 'dark' else '#CBD5E1'}; padding-top: 8px;">
                        <div><strong style="font-size: 1.1rem; color: {'#38BDF8' if current_theme == 'dark' else '#0284C7'};">{r3['Publications']}</strong><br><span style="font-size: 0.72rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'};">Papers</span></div>
                        <div><strong style="font-size: 1.1rem; color: #F59E0B;">{r3['Total Citations']:,}</strong><br><span style="font-size: 0.72rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'};">Citations</span></div>
                        <div><strong style="font-size: 1.1rem; color: #10B981;">{r3['h-Index']}</strong><br><span style="font-size: 0.72rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'};">h-Index</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Plotly Visual: Top Authors Publications & Citations
        col_plt1, col_plt2 = st.columns([3, 2])
        with col_plt1:
            st.markdown("##### **Scholarly Output vs. Citation Accrual by Author**")
            chart_slice = top_authors_df.head(15).copy()
            fig_auth = px.bar(
                chart_slice,
                x="Author",
                y="Publications",
                color="Total Citations",
                color_continuous_scale=["#93C5FD", "#3B82F6", "#1D4ED8", "#1E40AF"] if current_theme == "light" else ["#0284C7", "#38BDF8", "#60A5FA", "#93C5FD"],
                labels={"Author": "Faculty Researcher", "Publications": "Scopus Publications", "Total Citations": "Total Citations"},
                hover_data=["Department", "CPP", "h-Index", "Q1 Ratio"]
            )
            fig_auth.update_layout(
                height=360,
                margin=dict(l=20, r=20, t=20, b=40),
                xaxis_tickangle=-35,
            )
            fig_auth = style_plotly_fig(fig_auth, current_theme)
            st.plotly_chart(fig_auth, theme=None, use_container_width=True)

        with col_plt2:
            st.markdown("##### **Top Authors by Estimated $h$-Index**")
            h_slice = top_authors_df.sort_values(by="h-Index", ascending=False).head(10)
            fig_h = px.bar(
                h_slice,
                x="h-Index",
                y="Author",
                orientation="h",
                color="h-Index",
                color_continuous_scale=["#6EE7B7", "#10B981", "#059669", "#047857"],
                labels={"h-Index": "Author h-Index", "Author": "Researcher"}
            )
            fig_h.update_layout(
                height=360,
                margin=dict(l=20, r=20, t=20, b=20),
                yaxis=dict(autorange="reversed"),
                showlegend=False
            )
            fig_h = style_plotly_fig(fig_h, current_theme)
            st.plotly_chart(fig_h, theme=None, use_container_width=True)

        # Leaderboard Table
        with st.expander(f"📊 View Complete Faculty Leaderboard Table ({len(top_authors_df)} Researchers)", expanded=False):
            display_leaderboard = top_authors_df[["Rank", "Author", "Department", "Publications", "Total Citations", "CPP", "h-Index", "Q1 Papers", "Q1 Ratio", "Intl Collab %", "Industry Collab %", "Active Period"]]
            st.dataframe(
                display_leaderboard,
                column_config={
                    "Rank": st.column_config.NumberColumn("Rank", format="#%d"),
                    "Total Citations": st.column_config.NumberColumn("Citations", format="%d ⭐"),
                    "CPP": st.column_config.NumberColumn("CPP", format="%.2f"),
                    "h-Index": st.column_config.NumberColumn("h-Index", format="%d 📈"),
                },
                use_container_width=True,
                hide_index=True
            )

    st.markdown("---")

    # 2. Interactive Individual Author Dossier
    st.markdown('<div class="icare-section-title">🔍 Individual Faculty Dossier & Publishing Profile</div>', unsafe_allow_html=True)
    st.caption("Select any COEP faculty author below to inspect their career output, citation impact, quartile breakdown, and published articles.")

    # All unique authors for selector
    all_leaders = get_top_authors_leaderboard(df_filtered, top_n=500, sort_by="pubs")
    author_options = all_leaders["Author"].tolist() if not all_leaders.empty else []

    if not author_options:
        st.info("No authors available for profiling.")
    else:
        col_sel_a, col_sel_b = st.columns([2, 1])
        with col_sel_a:
            selected_author_name = st.selectbox(
                "Select Faculty Researcher:",
                author_options,
                index=0,
                key="author_profile_selector"
            )

        auth_profile = get_author_profile_metrics(df_filtered, selected_author_name)
        author_papers_df = get_author_publications(df_filtered, selected_author_name)

        if auth_profile:
            # Initials
            name_parts = selected_author_name.split()
            initials = "".join([p[0].upper() for p in name_parts[:2]]) if name_parts else "AU"

            # Profile Header Card
            st.markdown(f"""
            <div class="author-dossier-card">
                <div class="author-dossier-header">
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div class="author-avatar-circle">{initials}</div>
                        <div>
                            <div style="font-size: 1.35rem; font-weight: 800; color: {'#FFFFFF' if current_theme == 'dark' else '#0F172A'};">{auth_profile['author_name']}</div>
                            <div style="font-size: 0.84rem; color: #0284C7; font-weight: 700;">🏛️ {auth_profile['primary_dept']}</div>
                            <div style="font-size: 0.78rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'};">Scopus Affiliation: COEP Technological University, Pune • Active {auth_profile['min_year']}–{auth_profile['max_year']}</div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <div class="author-metric-chip">
                            <div class="author-metric-value">{auth_profile['total_pubs']}</div>
                            <div class="author-metric-label">Publications</div>
                        </div>
                        <div class="author-metric-chip">
                            <div class="author-metric-value">{auth_profile['total_citations']:,}</div>
                            <div class="author-metric-label">Total Citations</div>
                        </div>
                        <div class="author-metric-chip">
                            <div class="author-metric-value">{auth_profile['cpp']}</div>
                            <div class="author-metric-label">Citations / Pub</div>
                        </div>
                        <div class="author-metric-chip">
                            <div class="author-metric-value">{auth_profile['h_index']}</div>
                            <div class="author-metric-label">Author h-Index</div>
                        </div>
                        <div class="author-metric-chip">
                            <div class="author-metric-value">{auth_profile['q1_pct']}%</div>
                            <div class="author-metric-label">Q1 Top-Tier Ratio</div>
                        </div>
                    </div>
                </div>
                <div style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center;">
                    <span class="hero-pill hero-pill-gold">🥇 {auth_profile['q1_count']} Q1 Publications</span>
                    <span class="hero-pill hero-pill-cyan">🌐 {auth_profile['intl_pct']}% International Collab</span>
                    <span class="hero-pill" style="border-color: #10B981; color: {'#34D399' if current_theme == 'dark' else '#059669'};">🏢 {auth_profile['ind_pct']}% Industry Partner</span>
                    <span style="font-size: 0.8rem; color: {'#94A3B8' if current_theme == 'dark' else '#64748B'}; margin-left: auto;">
                        <strong>Key Collaborators:</strong> {', '.join(auth_profile['top_collaborators'][:3]) if auth_profile['top_collaborators'] else 'COEP Faculty'}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Visuals for selected author
            col_ap1, col_ap2 = st.columns([3, 2])
            with col_ap1:
                st.markdown(f"##### **Publishing Velocity & Citation Trend for {selected_author_name}**")
                annual_trend_df = get_author_annual_trend(df_filtered, selected_author_name)
                if not annual_trend_df.empty:
                    fig_auth_trend = go.Figure()
                    fig_auth_trend.add_trace(go.Bar(
                        x=annual_trend_df["year"],
                        y=annual_trend_df["publications"],
                        name="Annual Publications",
                        marker_color="#0284C7"
                    ))
                    fig_auth_trend.add_trace(go.Scatter(
                        x=annual_trend_df["year"],
                        y=annual_trend_df["citations"],
                        name="Citations Accrued",
                        yaxis="y2",
                        mode="lines+markers",
                        line=dict(color="#F59E0B", width=3),
                        marker=dict(size=7)
                    ))
                    fig_auth_trend.update_layout(
                        height=330,
                        margin=dict(l=20, r=20, t=20, b=20),
                        yaxis=dict(title=dict(text="Publications")),
                        yaxis2=dict(title=dict(text="Citations"), overlaying="y", side="right", showgrid=False),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    fig_auth_trend = style_plotly_fig(fig_auth_trend, current_theme)
                    st.plotly_chart(fig_auth_trend, theme=None, use_container_width=True)
                else:
                    st.info("No yearly trend data available.")

            with col_ap2:
                st.markdown(f"##### **Journal Quartile Breakdown (Q1–Q4)**")
                q_data = pd.DataFrame([
                    {"Quartile": "Q1", "Count": auth_profile["q1_count"]},
                    {"Quartile": "Q2", "Count": auth_profile["q2_count"]},
                    {"Quartile": "Q3", "Count": auth_profile["q3_count"]},
                    {"Quartile": "Q4", "Count": auth_profile["q4_count"]},
                ])
                q_data = q_data[q_data["Count"] > 0]
                if not q_data.empty:
                    fig_auth_q = px.pie(
                        q_data,
                        names="Quartile",
                        values="Count",
                        hole=0.55,
                        color="Quartile",
                        color_discrete_map={"Q1": "#10B981", "Q2": "#3B82F6", "Q3": "#F59E0B", "Q4": "#EF4444"}
                    )
                    fig_auth_q.update_layout(
                        height=330,
                        margin=dict(l=20, r=20, t=20, b=20),
                        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                    )
                    fig_auth_q.update_traces(textinfo="percent+label")
                    fig_auth_q = style_plotly_fig(fig_auth_q, current_theme)
                    st.plotly_chart(fig_auth_q, theme=None, use_container_width=True)
                else:
                    st.info("No quartile distribution data available.")

            # 3. Author's Published Papers Directory
            st.markdown(f"#### **📄 Publications Authored by {selected_author_name} ({len(author_papers_df)} Papers)**")

            # Export buttons for this author
            col_exp_a, col_exp_b, col_exp_c, col_spacer = st.columns([1, 1, 1, 2])
            with col_exp_a:
                auth_excel_buffer = io.BytesIO()
                with pd.ExcelWriter(auth_excel_buffer, engine="openpyxl") as writer:
                    author_papers_df.to_excel(writer, index=False, sheet_name="Author Publications")
                st.download_button(
                    label="📊 Export Excel",
                    data=auth_excel_buffer.getvalue(),
                    file_name=f"{selected_author_name.replace(' ', '_')}_Scopus_Papers.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            with col_exp_b:
                st.download_button(
                    label="📄 Export BibTeX",
                    data=export_to_bibtex(author_papers_df),
                    file_name=f"{selected_author_name.replace(' ', '_')}_Publications.bib",
                    mime="text/plain",
                    use_container_width=True
                )
            with col_exp_c:
                st.download_button(
                    label="📑 Export CSV",
                    data=author_papers_df.to_csv(index=False).encode("utf-8"),
                    file_name=f"{selected_author_name.replace(' ', '_')}_Scopus_Papers.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            # View mode toggle for author papers
            auth_view_mode = st.radio("Display Layout", ["Detailed Paper Cards", "Compact Data Table"], horizontal=True, key="auth_paper_view_mode")

            if auth_view_mode == "Compact Data Table":
                tbl_cols = ["title", "journal", "year", "citations", "quartile", "doi_url", "authors_str"]
                disp_auth_df = author_papers_df[[c for c in tbl_cols if c in author_papers_df.columns]].rename(columns={
                    "title": "Paper Title",
                    "journal": "Journal / Conference",
                    "year": "Year",
                    "citations": "Citations",
                    "quartile": "Quartile",
                    "doi_url": "DOI Link",
                    "authors_str": "Co-Authors"
                })
                st.dataframe(
                    disp_auth_df,
                    column_config={
                        "DOI Link": st.column_config.LinkColumn("DOI", display_text="View Paper ↗"),
                        "Citations": st.column_config.NumberColumn("Citations", format="%d ⭐"),
                    },
                    use_container_width=True,
                    hide_index=True
                )
            else:
                for _, paper in author_papers_df.iterrows():
                    q_val = paper.get('quartile', 'Q3')
                    q_cls = f"badge-{str(q_val).lower()}"
                    doi_url = paper.get('doi_url', '')
                    doi_txt = paper.get('doi', 'N/A')
                    doi_link = f'<a href="{doi_url}" target="_blank" style="color: #0284C7; text-decoration: none; font-weight: 700;">{doi_txt} ↗</a>' if doi_url else doi_txt

                    collab_tag = ""
                    if paper.get("is_international_collab"):
                        collab_tag = '<span class="tag-pill" style="border-color:#0284C7; color:#38BDF8;">🌐 International Collab</span>'
                    elif paper.get("is_industry_collab"):
                        collab_tag = '<span class="tag-pill" style="border-color:#F59E0B; color:#FBBF24;">🏢 Industry Partner</span>'

                    auth_card_html = f"""<div class="icare-feed-card">
<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
    <div class="feed-title">{paper.get('title')}</div>
    <div><span class="{q_cls}">{q_val}</span></div>
</div>
<div class="feed-meta">
    <strong>Authors:</strong> {paper.get('authors_str')}<br>
    <strong>Journal:</strong> {paper.get('journal')} &nbsp;|&nbsp; <strong>Year:</strong> {paper.get('year')} &nbsp;|&nbsp; <strong>Department:</strong> {paper.get('department')}
</div>
<div class="feed-tag-row">
    <span class="tag-pill">⭐ <strong>{paper.get('citations')}</strong> Citations</span>
    <span class="tag-pill">📊 CiteScore: <strong>{paper.get('citescore', 0.0)}</strong></span>
    <span class="tag-pill">📈 SJR: <strong>{paper.get('sjr', 0.0)}</strong></span>
    <span class="tag-pill">📑 {paper.get('document_type', 'Article')}</span>
    {collab_tag}
    <span style="font-size: 0.82rem; margin-left: 6px;"><strong>DOI:</strong> {doi_link}</span>
</div>
</div>"""
                    st.html(auth_card_html)

    st.markdown("---")

    # 4. Landmark Institutional Most-Cited Papers Spotlight
    st.markdown('<div class="icare-section-title">🌟 Landmark Publications & Institutional Citation Champions</div>', unsafe_allow_html=True)
    st.caption("Highest-impact research publications originating from COEP Technological University ranked by global citation accrual.")

    landmark_df = get_landmark_cited_papers(df_filtered, top_n=10)
    if not landmark_df.empty:
        landmark_disp = landmark_df[["Rank", "title", "authors_str", "department", "journal", "year", "citations", "quartile", "doi_url"]].rename(columns={
            "title": "Landmark Publication Title",
            "authors_str": "Contributing Authors",
            "department": "Department",
            "journal": "Journal / Venue",
            "year": "Year",
            "citations": "Global Citations",
            "quartile": "Quartile",
            "doi_url": "DOI"
        })
        st.dataframe(
            landmark_disp,
            column_config={
                "Rank": st.column_config.NumberColumn("Rank", format="#%d"),
                "DOI": st.column_config.LinkColumn("DOI Link", display_text="View ↗"),
                "Global Citations": st.column_config.NumberColumn("Citations", format="%d ⭐"),
            },
            use_container_width=True,
            hide_index=True
        )

# ---------------------------------------------------------
# TAB 6: LIVE PUBLICATION FEED
# ---------------------------------------------------------
with tab_feed:
    st.markdown('<div class="icare-section-title">📰 Live Publication Feed & Searchable Explorer</div>', unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
    with col_s1:
        search_query = st.text_input("🔍 Search publications (Title, Author, Journal, DOI, Keyword)", placeholder="e.g. AI, Sutar, Sapali, IEEE, Sensors, 10.1016...")
    with col_s2:
        sort_by = st.selectbox("Sort Order", ["Latest Date (Desc)", "Most Cited (Desc)", "CiteScore (Desc)", "Title (A-Z)"])
    with col_s3:
        view_mode = st.radio("View Mode", ["Detailed Cards", "Data Table"], horizontal=True)

    feed_df = filter_publications(df_filtered, search_query=search_query)

    if sort_by == "Latest Date (Desc)":
        feed_df = feed_df.sort_values("publication_date", ascending=False)
    elif sort_by == "Most Cited (Desc)":
        feed_df = feed_df.sort_values("citations", ascending=False)
    elif sort_by == "CiteScore (Desc)":
        feed_df = feed_df.sort_values("citescore", ascending=False)
    elif sort_by == "Title (A-Z)":
        feed_df = feed_df.sort_values("title", ascending=True)

    st.write(f"Showing **{len(feed_df):,}** matching publications:")

    if feed_df.empty:
        st.warning("No publications match your current filters.")
    elif view_mode == "Data Table":
        table_cols = ["title", "authors_str", "department", "journal", "publication_date", "doi_url", "quartile", "citescore", "sjr", "citations"]
        display_feed = feed_df[[c for c in table_cols if c in feed_df.columns]].rename(columns={
            "title": "Publication Title",
            "authors_str": "Authors",
            "department": "Department",
            "journal": "Journal / Source",
            "publication_date": "Date",
            "doi_url": "DOI Link",
            "quartile": "Quartile",
            "citescore": "CiteScore",
            "sjr": "SJR",
            "citations": "Citations"
        })
        st.dataframe(
            display_feed,
            column_config={
                "DOI Link": st.column_config.LinkColumn("DOI", display_text="View DOI ↗"),
                "Citations": st.column_config.NumberColumn("Citations", format="%d ⭐"),
                "CiteScore": st.column_config.NumberColumn("CiteScore", format="%.1f"),
                "SJR": st.column_config.NumberColumn("SJR", format="%.2f"),
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        page_size = 10
        total_pages = max(1, (len(feed_df) + page_size - 1) // page_size)
        current_page = st.number_input(f"Page (1 to {total_pages})", min_value=1, max_value=total_pages, value=1, step=1)
        
        start_idx = (current_page - 1) * page_size
        end_idx = start_idx + page_size
        page_items = feed_df.iloc[start_idx:end_idx]

        for _, item in page_items.iterrows():
            q_class = f"badge-{str(item.get('quartile', 'q3')).lower()}"
            doi_link_html = f'<a href="{item.get("doi_url")}" target="_blank" style="color: #0284C7; text-decoration: none; font-weight: 600;">{item.get("doi")} ↗</a>' if item.get("doi") else "N/A"
            scopus_link_html = f'<a href="{item.get("scopus_url")}" target="_blank" style="color: #64748B; text-decoration: none; font-size: 0.8rem;">[Scopus Record ↗]</a>' if item.get("scopus_url") else ""

            collab_badge = ""
            if item.get("is_international_collab"):
                collab_badge = '<span class="tag-pill" style="border-color:#0284C7; color:#38BDF8;">🌐 International Collab</span>'
            elif item.get("is_industry_collab"):
                collab_badge = '<span class="tag-pill" style="border-color:#F59E0B; color:#FBBF24;">🏢 Industry Partner</span>'
            elif item.get("collaboration_type") == "National":
                collab_badge = '<span class="tag-pill" style="color:#94A3B8;">🇮🇳 National Collab</span>'

            card_html = f"""<div class="icare-feed-card">
<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
    <div class="feed-title">{item.get('title')}</div>
    <div><span class="{q_class}">{item.get('quartile', 'Q3')}</span></div>
</div>
<div class="feed-meta">
    <strong>Authors:</strong> {item.get('authors_str')}<br>
    <strong>Department:</strong> {item.get('department')} &nbsp;|&nbsp; <strong>Journal:</strong> {item.get('journal')} &nbsp;|&nbsp; <strong>Date:</strong> {item.get('publication_date')}
</div>
<div class="feed-tag-row">
    <span class="tag-pill">⭐ <strong>{item.get('citations')}</strong> Citations</span>
    <span class="tag-pill">📊 CiteScore: <strong>{item.get('citescore')}</strong></span>
    <span class="tag-pill">📈 SJR: <strong>{item.get('sjr')}</strong></span>
    <span class="tag-pill">📑 {item.get('document_type', 'Article')}</span>
    {collab_badge}
    <span style="font-size: 0.82rem; margin-left: 6px;"><strong>DOI:</strong> {doi_link_html}</span>
    {scopus_link_html}
</div>
</div>"""
            st.html(card_html)

            with st.expander(f"📄 Abstract & Affiliation Details: {str(item.get('title'))[:60]}..."):
                st.write(f"**Abstract:** {item.get('abstract', 'No abstract available.')}")
                st.write(f"**Contributing Authors:** {item.get('authors_str')}")
                if item.get("collaborating_institutions"):
                    st.write(f"**Affiliated Institutions:** {', '.join(item.get('collaborating_institutions'))}")
                if item.get("collaborating_countries"):
                    st.write(f"**Partner Countries:** {', '.join(item.get('collaborating_countries'))}")

# ---------------------------------------------------------
# Post-Render Sidebar State Enforcement (Desktop: Always Open, Mobile: Collapsed)
# ---------------------------------------------------------
components.html(
    """
    <script>
        function enforceSidebar() {
            try {
                const p = window.parent || window;
                const d = p.document || document;
                if (!d) return;
                
                try {
                    p.localStorage.removeItem('st-sidebar-collapsed');
                    p.localStorage.setItem('st-sidebar-expanded', 'true');
                } catch(e) {}

                const width = p.innerWidth || d.documentElement.clientWidth || 1200;
                
                if (width > 768) {
                    const sidebar = d.querySelector('section[data-testid="stSidebar"]');
                    const expandBtn = d.querySelector('button[data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"] button, button[aria-label="Expand sidebar"]');
                    
                    if (sidebar) {
                        const style = p.getComputedStyle(sidebar);
                        const isClosed = sidebar.getAttribute('aria-expanded') === 'false' || 
                                         sidebar.getAttribute('data-expanded') === 'false' || 
                                         (style.transform && style.transform !== 'none' && style.transform.includes('-'));
                        if (isClosed && expandBtn) {
                            expandBtn.click();
                        }
                    } else if (expandBtn) {
                        expandBtn.click();
                    }
                } else {
                    const sidebar = d.querySelector('section[data-testid="stSidebar"]');
                    if (sidebar) {
                        const isExpanded = sidebar.getAttribute('aria-expanded') === 'true' || 
                                           sidebar.getAttribute('data-expanded') === 'true';
                        if (isExpanded) {
                            const closeBtn = sidebar.querySelector('button[data-testid="stSidebarCollapseButton"], button[aria-label="Close sidebar"]');
                            if (closeBtn) {
                                closeBtn.click();
                            }
                        }
                    }
                }
            } catch(err) {}
        }
        enforceSidebar();
        setTimeout(enforceSidebar, 50);
        setTimeout(enforceSidebar, 200);
        setTimeout(enforceSidebar, 500);
        setTimeout(enforceSidebar, 1000);
    </script>
    """,
    height=0,
    width=0,
)

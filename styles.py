# COEP Scopus Live Dashboard - Production Release
import os
import base64

def get_base64_image(image_path: str) -> str:
    """Encodes an image file to a base64 Data URI."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(image_path)[1].lower()
            mime = "image/png" if ext == ".png" else "image/jpeg"
            return f"data:{mime};base64,{encoded}"
    return ""

def get_custom_css(theme: str = "dark") -> str:
    is_dark = theme == "dark"
    
    # Theme variables
    bg_main = "#070F1E" if is_dark else "#F1F5F9"
    bg_card = "#0D1B2E" if is_dark else "#FFFFFF"
    bg_card_secondary = "#13233D" if is_dark else "#F8FAFC"
    border_color = "#1E3250" if is_dark else "#E2E8F0"
    border_hover = "#00D2FF" if is_dark else "#2563EB"
    
    text_primary = "#FFFFFF" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#94A3B8"
    
    hero_bg = "linear-gradient(135deg, #0B1C33 0%, #102747 60%, #173764 100%)" if is_dark else "linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)"
    nav_active_bg = "linear-gradient(90deg, #0284C7 0%, #0369A1 100%)" if is_dark else "linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%)"
    
    # Sidebar Palette
    sidebar_bg = "#071224" if is_dark else "#FFFFFF"
    sidebar_title_color = "#FFFFFF" if is_dark else "#0A192F"
    sidebar_section_hdr = "#00D2FF" if is_dark else "#0284C7"
    sidebar_label_color = "#F8FAFC" if is_dark else "#0F172A"
    sidebar_caption_color = "#38BDF8" if is_dark else "#0284C7"
    sidebar_input_bg = "#0E1E36" if is_dark else "#FFFFFF"
    sidebar_border = "#1E3A5F" if is_dark else "#CBD5E1"
    sidebar_input_text = "#FFFFFF" if is_dark else "#0F172A"

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Cinzel:wght@700&display=swap');

        :root {{
            --primary-color: #0284C7;
            --background-color: {bg_main};
            --secondary-background-color: {sidebar_input_bg};
            --text-color: {text_primary};
        }}

        /* App Background */
        .stApp {{
            background-color: {bg_main} !important;
            color: {text_primary} !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        /* Clean Streamlit Header */
        header[data-testid="stHeader"] {{
            background-color: transparent !important;
        }}

        /* ========================================================= */
        /* SIDEBAR STYLING - HIGH CONTRAST & VIBRANT */
        /* ========================================================= */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div,
        [data-testid="stSidebarContent"],
        [data-testid="stSidebarUserContent"],
        [data-testid="stSidebarNav"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {border_color} !important;
        }}

        /* Sidebar Brand Box Component */
        .sidebar-brand-box {{
            background: {'linear-gradient(135deg, rgba(2, 132, 199, 0.15) 0%, rgba(14, 30, 54, 0.6) 100%)' if is_dark else 'linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)'};
            border: 1px solid {'#0284C7' if is_dark else '#93C5FD'};
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 16px;
        }}

        .sidebar-brand-title {{
            font-size: 1.15rem;
            font-weight: 800;
            color: {sidebar_title_color};
            letter-spacing: -0.01em;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }}

        .sidebar-brand-sub {{
            font-size: 0.76rem;
            font-weight: 700;
            color: {sidebar_caption_color};
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}

        .sidebar-section-hdr {{
            font-size: 0.82rem;
            font-weight: 800;
            color: {sidebar_section_hdr};
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-top: 14px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        /* Universal Sidebar Text Overrides */
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {{
            color: {sidebar_label_color} !important;
        }}

        [data-testid="stSidebar"] .sidebar-brand-title {{
            color: {sidebar_title_color} !important;
            font-weight: 800 !important;
        }}

        [data-testid="stSidebar"] .sidebar-brand-sub {{
            color: {sidebar_caption_color} !important;
            font-weight: 700 !important;
        }}

        [data-testid="stSidebar"] .sidebar-section-hdr {{
            color: {sidebar_section_hdr} !important;
            font-weight: 800 !important;
        }}

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] label p,
        [data-testid="stSidebar"] label span,
        [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {{
            color: {sidebar_label_color} !important;
            font-weight: 800 !important;
            font-size: 0.92rem !important;
        }}

        /* React-Aria Selectbox & MultiSelect Emotion containers */
        html body div.stApp div[class*="e1j154pq"],
        html body div.stApp div[class*="e1j154pq0"],
        html body div.stApp div[class*="e1j154pq"] > div,
        html body div.stApp div[data-testid="stMultiSelect"] div,
        html body div.stApp div[data-testid="stSelectbox"] div,
        html body div.stApp div[data-baseweb="select"] div,
        .stApp [data-testid="stSidebar"] div:has(> input),
        .stApp [data-testid="stSidebar"] div[class*="e1j154pq0"],
        .stApp div[class*="e1j154pq0"],
        .stApp [class*="esagd7"],
        .stApp [data-testid="stSidebar"] div[class*="e1j154pq"],
        .stApp div[data-testid="stMultiSelect"] div[class*="e1j154pq"],
        .stApp div[data-testid="stSelectbox"] div[class*="e1j154pq"],
        .stApp .react-aria-ComboBox,
        .stApp div[class*="e1j154pq0"],
        .stApp div[class*="e1j154pq1"],
        .stApp div[class*="e1j154pq2"],
        .stApp div[class*="e1j154pq3"] {{
            background-color: {'#0E1E36' if is_dark else '#FFFFFF'} !important;
            border-color: {'#1E3A5F' if is_dark else '#CBD5E1'} !important;
            color: {'#CBD5E1' if is_dark else '#0F172A'} !important;
        }}

        .stApp button[class*="e1j154pq"],
        .stApp [data-testid="stSidebar"] button[class*="e1j154pq"] {{
            background-color: transparent !important;
            border: none !important;
            color: {'#94A3B8' if is_dark else '#475569'} !important;
        }}

        .stApp button[class*="e1j154pq"] svg,
        .stApp [data-testid="stSidebar"] button[class*="e1j154pq"] svg {{
            fill: {'#94A3B8' if is_dark else '#475569'} !important;
            stroke: {'#94A3B8' if is_dark else '#475569'} !important;
        }}

        /* Universal Inputs & Selectboxes (Sidebar & Main Dashboard Area) */
        /* Complete Removal of Streamlit Default 3-Dots Menu, Deploy Button, & Footer while PRESERVING Expand Sidebar Button */
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

        /* Hide expand button completely whenever sidebar is already expanded */
        section[data-testid="stSidebar"][aria-expanded="true"] ~ * button[data-testid="stExpandSidebarButton"],
        section[data-testid="stSidebar"][aria-expanded="true"] ~ button[data-testid="stExpandSidebarButton"],
        section[data-testid="stSidebar"][aria-expanded="true"] + * [data-testid="stExpandSidebarButton"],
        body:has(section[data-testid="stSidebar"][aria-expanded="true"]) button[data-testid="stExpandSidebarButton"],
        html:has(section[data-testid="stSidebar"][aria-expanded="true"]) button[data-testid="stExpandSidebarButton"] {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }}

        button[data-testid="stExpandSidebarButton"] *,
        button[data-testid="stExpandSidebarButton"] svg,
        button[data-testid="stExpandSidebarButton"] span {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
        }}
        html body div.stApp [data-testid="stSidebar"] [data-testid="stMultiSelect"] *,
        html body div.stApp [data-testid="stSidebar"] [data-testid="stSelectbox"] *,
        html body div.stApp div[data-testid="stSelectbox"] *,
        html body div.stApp div[data-testid="stMultiSelect"] *,
        html body div.stApp div[data-baseweb="select"] *,
        html body div.stApp div[data-baseweb="input"] *,
        html body div.stApp div[data-testid="stTextInput"] *,
        html body div.stApp input,
        html body div.stApp textarea,
        .stApp [data-testid="stSidebar"] [data-testid="stMultiSelect"] *,
        .stApp [data-testid="stSidebar"] [data-testid="stSelectbox"] *,
        .stApp div[data-testid="stSelectbox"] *,
        .stApp div[data-testid="stMultiSelect"] *,
        .stApp div[data-baseweb="select"] *,
        .stApp div[data-baseweb="input"] *,
        .stApp div[data-testid="stTextInput"] *,
        .stApp input {{
            background-color: {'#0E1E36' if is_dark else '#FFFFFF'} !important;
            color: {'#FFFFFF' if is_dark else '#0F172A'} !important;
            -webkit-text-fill-color: {'#FFFFFF' if is_dark else '#0F172A'} !important;
        }}

        /* High-Specificity Placeholders in Dark & Light Mode */
        html body div.stApp input::placeholder,
        html body div.stApp textarea::placeholder,
        html body div.stApp [data-testid="stSidebar"] input::placeholder,
        html body div.stApp div[data-testid="stMultiSelect"] input::placeholder,
        html body div.stApp div[data-testid="stSelectbox"] input::placeholder,
        html body div.stApp div[data-baseweb="select"] input::placeholder,
        html body div.stApp div[class*="e1j154pq"] input::placeholder,
        .stApp input::placeholder,
        [data-testid="stSidebar"] input::placeholder,
        div[data-testid="stMultiSelect"] input::placeholder,
        div[data-testid="stSelectbox"] input::placeholder,
        div[data-baseweb="select"] input::placeholder,
        .react-aria-ComboBox input::placeholder,
        div[class*="e1j154pq"] input::placeholder,
        input::placeholder {{
            color: {'#CBD5E1' if is_dark else '#475569'} !important;
            -webkit-text-fill-color: {'#CBD5E1' if is_dark else '#475569'} !important;
            opacity: 1 !important;
            font-weight: 500 !important;
        }}

        html body div.stApp input::-webkit-input-placeholder,
        html body div.stApp [data-testid="stSidebar"] input::-webkit-input-placeholder,
        html body div.stApp div[data-testid="stMultiSelect"] input::-webkit-input-placeholder,
        [data-testid="stSidebar"] input::-webkit-input-placeholder,
        input::-webkit-input-placeholder {{
            color: {'#CBD5E1' if is_dark else '#475569'} !important;
            -webkit-text-fill-color: {'#CBD5E1' if is_dark else '#475569'} !important;
            opacity: 1 !important;
            font-weight: 500 !important;
        }}

        input::-moz-placeholder {{
            color: {'#CBD5E1' if is_dark else '#475569'} !important;
            opacity: 1 !important;
        }}

        div[data-baseweb="select"] div[aria-hidden="true"],
        div[data-baseweb="select"] span[aria-hidden="true"],
        div[data-baseweb="select"] p[aria-hidden="true"],
        div[data-baseweb="select"] div[role="combobox"] {{
            color: {'#CBD5E1' if is_dark else '#475569'} !important;
            -webkit-text-fill-color: {'#CBD5E1' if is_dark else '#475569'} !important;
            opacity: 1 !important;
        }}

        .stApp [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="select"] > div,
        .stApp [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        .stApp div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
        .stApp div[data-testid="stMultiSelect"] [data-baseweb="select"] > div,
        .stApp div[data-testid="stTextInput"] [data-baseweb="input"] {{
            background-color: {'#0E1E36' if is_dark else '#FFFFFF'} !important;
            border: 1.5px solid {'#1E3A5F' if is_dark else '#CBD5E1'} !important;
            border-radius: 8px !important;
        }}

        .stApp div[data-baseweb="select"] svg,
        .stApp [data-testid="stSidebar"] [data-baseweb="select"] svg,
        .stApp div[data-baseweb="select"] path,
        .stApp [data-testid="stSidebar"] [data-baseweb="select"] path {{
            background-color: transparent !important;
            fill: {'#94A3B8' if is_dark else '#475569'} !important;
            color: {'#94A3B8' if is_dark else '#475569'} !important;
        }}

        /* Dropdown Popover Menus */
        div[data-baseweb="popover"],
        div[data-baseweb="menu"],
        ul[role="listbox"],
        li[role="option"],
        li[role="option"] * {{
            background-color: {'#0E1E36' if is_dark else '#FFFFFF'} !important;
            color: {'#FFFFFF' if is_dark else '#0F172A'} !important;
        }}

        li[role="option"]:hover,
        li[role="option"][aria-selected="true"],
        li[role="option"]:hover *,
        li[role="option"][aria-selected="true"] * {{
            background-color: {'#0284C7' if is_dark else '#EFF6FF'} !important;
            color: {'#FFFFFF' if is_dark else '#0284C7'} !important;
        }}

        /* High-Contrast Plotly Text in Light & Dark Mode */
        div.stPlotlyChart svg text,
        div.stPlotlyChart svg text *,
        div.stPlotlyChart svg tspan,
        .js-plotly-plot svg text,
        .js-plotly-plot svg text *,
        .js-plotly-plot svg tspan,
        .js-plotly-plot text,
        .js-plotly-plot tspan,
        svg.main-svg text,
        svg.main-svg tspan {{
            fill: {'#FFFFFF' if is_dark else '#0F172A'} !important;
            color: {'#FFFFFF' if is_dark else '#0F172A'} !important;
        }}

        .js-plotly-plot .gridlayer path,
        .js-plotly-plot .zerolinelayer path {{
            stroke: {'rgba(255, 255, 255, 0.1)' if is_dark else 'rgba(15, 23, 42, 0.12)'} !important;
        }}

        .stApp [data-testid="stSidebar"] [data-baseweb="input"] button {{
            background-color: transparent !important;
            color: {'#94A3B8' if is_dark else '#64748B'} !important;
            border: none !important;
        }}

        .stApp [data-testid="stSidebar"] [data-baseweb="input"] button:hover {{
            color: {'#38BDF8' if is_dark else '#0284C7'} !important;
        }}

        /* Multiselect selected tags / chips */
        div[data-baseweb="tag"] {{
            background-color: #0284C7 !important;
            color: #FFFFFF !important;
        }}
        div[data-baseweb="tag"] span {{
            color: #FFFFFF !important;
        }}

        /* Sidebar Mode Toggle & Action Buttons */
        [data-testid="stSidebar"] button[kind="primary"],
        [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"],
        [data-testid="stSidebar"] button[data-testid="baseButton-primary"] {{
            background: {nav_active_bg} !important;
            background-color: #0284C7 !important;
            color: #FFFFFF !important;
            border: 1.5px solid #0284C7 !important;
            border-radius: 8px !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4) !important;
            transition: all 0.2s ease !important;
        }}

        [data-testid="stSidebar"] button[kind="primary"] *,
        [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] *,
        [data-testid="stSidebar"] button[data-testid="baseButton-primary"] *,
        [data-testid="stSidebar"] button[kind="primary"] p,
        [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] p,
        [data-testid="stSidebar"] button[data-testid="baseButton-primary"] p {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-weight: 800 !important;
        }}

        [data-testid="stSidebar"] button[kind="secondary"],
        [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"],
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {{
            background-color: {'#0E1E36' if is_dark else '#F8FAFC'} !important;
            color: {'#CBD5E1' if is_dark else '#1E293B'} !important;
            border: 1.5px solid {sidebar_border} !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            transition: all 0.2s ease !important;
        }}

        [data-testid="stSidebar"] button[kind="secondary"] *,
        [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] *,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] *,
        [data-testid="stSidebar"] button[kind="secondary"] p,
        [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] p,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] p {{
            color: {'#CBD5E1' if is_dark else '#1E293B'} !important;
            -webkit-text-fill-color: {'#CBD5E1' if is_dark else '#1E293B'} !important;
            font-weight: 700 !important;
        }}

        /* Slider track styling */
        div[data-testid="stSlider"] [role="slider"] {{
            background-color: #00D2FF !important;
            border: 2px solid #FFFFFF !important;
        }}
        div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {{
            background-color: #00D2FF !important;
        }}
        div[data-testid="stSlider"] div[data-testid="stMarkdownContainer"] p {{
            color: {'#38BDF8' if is_dark else '#0284C7'} !important;
            font-weight: 700 !important;
        }}

        /* Calibrated Top Spacing (~14px) for Desktop & Mobile */
        .block-container {{
            padding-top: 14px !important;
            padding-bottom: 2rem !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
        [data-testid="stSidebarContent"] {{
            padding-top: 14px !important;
        }}

        /* ========================================================= */
        /* TOP NAVBAR & HERO DOSSIER */
        /* ========================================================= */
        .icare-topbar {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 14px;
            padding: 12px 20px;
            margin: 0 0 20px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,{'0.25' if is_dark else '0.04'});
        }}

        .icare-brand-group {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .icare-logo-badge {{
            background: {'#FFFFFF' if is_dark else '#0A192F'};
            color: {'#0A192F' if is_dark else '#FFFFFF'};
            font-weight: 900;
            font-size: 1.15rem;
            padding: 4px 12px;
            border-radius: 8px;
            letter-spacing: 0.08em;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}

        .icare-intel-badge {{
            background: #0284C7;
            color: #FFFFFF;
            font-size: 0.72rem;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 6px;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }}

        .icare-subtext {{
            font-size: 0.82rem;
            color: {text_secondary};
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .icare-actions-group {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .icare-pill-btn {{
            background: {bg_card_secondary};
            border: 1px solid {border_color};
            color: {text_primary};
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            text-decoration: none;
            transition: all 0.2s ease;
        }}

        .icare-pill-btn:hover {{
            border-color: {border_hover};
            color: #00D2FF;
        }}

        .icare-user-badge {{
            background: {'rgba(212, 175, 55, 0.15)' if is_dark else '#FEF3C7'};
            border: 1px solid {'#D4AF37' if is_dark else '#F59E0B'};
            color: {'#FBBF24' if is_dark else '#B45309'};
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
        }}

        /* Secondary Breadcrumb Bar */
        .icare-subbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid {border_color};
        }}

        .inst-tag {{
            background: {'rgba(245, 158, 11, 0.18)' if is_dark else '#FEF3C7'};
            border: 1px solid {'#F59E0B' if is_dark else '#FDE68A'};
            color: {'#FBBF24' if is_dark else '#B45309'};
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-left: 8px;
        }}

        /* Hero Dossier Card */
        .icare-hero {{
            background: {hero_bg};
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 24px 28px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,{'0.2' if is_dark else '0.04'});
        }}

        .icare-hero::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #00D2FF, #00F5D4, #FFAA00, #A855F7);
        }}

        .hero-badge-group {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 12px;
        }}

        .hero-pill {{
            background: {bg_card};
            border: 1px solid {border_color};
            color: {text_primary};
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        .hero-pill-gold {{
            background: {'rgba(245, 158, 11, 0.15)' if is_dark else '#FEF3C7'};
            border: 1px solid #F59E0B;
            color: {'#FBBF24' if is_dark else '#B45309'};
        }}

        .hero-pill-cyan {{
            background: {'rgba(2, 132, 199, 0.18)' if is_dark else '#E0F2FE'};
            border: 1px solid #0284C7;
            color: {'#38BDF8' if is_dark else '#0369A1'};
        }}

        .hero-title {{
            font-size: 1.85rem;
            font-weight: 800;
            color: {text_primary};
            letter-spacing: -0.02em;
            margin-bottom: 4px;
        }}

        .hero-subtitle {{
            font-size: 0.95rem;
            color: {text_secondary};
            margin-bottom: 0;
        }}

        .hero-rank-box {{
            text-align: right;
        }}

        .hero-rank-label {{
            font-size: 0.78rem;
            font-weight: 700;
            color: {text_secondary};
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .hero-rank-val {{
            font-size: 2.3rem;
            font-weight: 900;
            color: {'#00D2FF' if is_dark else '#0284C7'};
            line-height: 1.1;
        }}

        /* Action Toolbar Title */
        .toolbar-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: {text_primary};
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 6px;
        }}

        /* Download Action Buttons (Excel, BibTeX, CSV) */
        .stApp div[data-testid="stDownloadButton"] > button,
        .stApp div.stDownloadButton > button,
        .stApp .stDownloadButton > button {{
            background: #0284C7 !important;
            background-color: #0284C7 !important;
            color: #FFFFFF !important;
            border: 1px solid #0284C7 !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            font-size: 0.86rem !important;
            padding: 8px 14px !important;
            box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3) !important;
        }}

        .stApp div[data-testid="stDownloadButton"] > button *,
        .stApp div.stDownloadButton > button *,
        .stApp .stDownloadButton > button * {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }}

        .stApp div[data-testid="stDownloadButton"] > button:hover,
        .stApp div.stDownloadButton > button:hover,
        .stApp .stDownloadButton > button:hover {{
            background: #0369A1 !important;
            background-color: #0369A1 !important;
            border-color: #0369A1 !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);
        }}

        /* Streamlit Primary Button override */
        button[data-testid="baseButton-primary"],
        button[data-testid="stBaseButton-primary"],
        button[kind="primary"],
        .stButton > button[kind="primary"] {{
            background-color: #0284C7 !important;
            border-color: #0284C7 !important;
            color: #FFFFFF !important;
        }}
        button[data-testid="baseButton-primary"] p,
        button[data-testid="stBaseButton-primary"] p {{
            color: #FFFFFF !important;
        }}

        /* KPI Metric Cards */
        .icare-kpi-card {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 14px;
            padding: 18px 16px;
            position: relative;
            transition: all 0.25s ease-in-out;
            box-shadow: 0 4px 12px rgba(0,0,0,{'0.12' if is_dark else '0.04'});
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }}

        .icare-kpi-card:hover {{
            transform: translateY(-4px);
            border-color: {border_hover};
            box-shadow: 0 12px 24px rgba(0,0,0,{'0.25' if is_dark else '0.08'});
        }}

        .kpi-header-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 8px;
        }}

        .icare-kpi-title {{
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {text_secondary};
        }}

        .kpi-icon-badge {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }}

        .icon-blue {{ background: {'rgba(37, 99, 235, 0.2)' if is_dark else '#DBEAFE'}; color: {'#60A5FA' if is_dark else '#1D4ED8'}; }}
        .icon-orange {{ background: {'rgba(245, 158, 11, 0.2)' if is_dark else '#FEF3C7'}; color: {'#FBBF24' if is_dark else '#D97706'}; }}
        .icon-teal {{ background: {'rgba(16, 185, 129, 0.2)' if is_dark else '#D1FAE5'}; color: {'#34D399' if is_dark else '#059669'}; }}
        .icon-purple {{ background: {'rgba(139, 92, 246, 0.2)' if is_dark else '#EDE9FE'}; color: {'#A78BFA' if is_dark else '#7C3AED'}; }}
        .icon-rose {{ background: {'rgba(244, 63, 94, 0.2)' if is_dark else '#FFE4E6'}; color: {'#FB7185' if is_dark else '#E11D48'}; }}

        .icare-kpi-value {{
            font-size: 1.85rem;
            font-weight: 800;
            color: {text_primary};
            line-height: 1.1;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }}

        .kpi-footer-pill {{
            font-size: 0.76rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            width: fit-content;
        }}

        .pill-blue {{ background: {'rgba(37, 99, 235, 0.15)' if is_dark else '#EFF6FF'}; color: {'#38BDF8' if is_dark else '#1E40AF'}; }}
        .pill-green {{ background: {'rgba(16, 185, 129, 0.15)' if is_dark else '#ECFDF5'}; color: {'#34D399' if is_dark else '#065F46'}; }}
        .pill-gold {{ background: {'rgba(245, 158, 11, 0.15)' if is_dark else '#FFFBEB'}; color: {'#FBBF24' if is_dark else '#92400E'}; }}
        .pill-purple {{ background: {'rgba(139, 92, 246, 0.15)' if is_dark else '#F5F3FF'}; color: {'#C084FC' if is_dark else '#5B21B6'}; }}
        .pill-rose {{ background: {'rgba(244, 63, 94, 0.15)' if is_dark else '#FFF1F2'}; color: {'#FB7185' if is_dark else '#9F1239'}; }}

        /* Tab Bar Styling & Scroll Button Removal */
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
            justify-content: flex-start !important;
            align-items: center !important;
            width: 100% !important;
            gap: 4px !important;
            background-color: {'#0D1B2E' if is_dark else '#F1F5F9'} !important;
            padding: 5px 6px !important;
            border-radius: 12px !important;
            border: 1.5px solid {border_color} !important;
            margin-bottom: 24px !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            scrollbar-width: none !important;
        }}

        div[data-testid="stTab"],
        div[role="tab"],
        button[role="tab"],
        button[data-testid="stTab"],
        div[data-baseweb="tab-list"] button[data-baseweb="tab"],
        div[data-testid="stTabs"] [role="tab"] {{
            flex: 1 1 auto !important;
            min-width: max-content !important;
            display: inline-flex !important;
            justify-content: center !important;
            align-items: center !important;
            text-align: center !important;
            border-radius: 8px !important;
            padding: 7px 11px !important;
            border: none !important;
            background: transparent !important;
            background-color: transparent !important;
            transition: all 0.2s ease !important;
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
            color: {'#94A3B8' if is_dark else '#1E293B'} !important;
            -webkit-text-fill-color: {'#94A3B8' if is_dark else '#1E293B'} !important;
            font-weight: 700 !important;
            font-size: 0.84rem !important;
            opacity: 1 !important;
            white-space: nowrap !important;
            margin: 0 !important;
        }}

        div[data-testid="stTab"]:hover *,
        div[role="tab"]:hover *,
        button[role="tab"]:hover *,
        button[data-testid="stTab"]:hover *,
        div[data-testid="stTabs"] [role="tab"]:hover * {{
            color: {'#38BDF8' if is_dark else '#0284C7'} !important;
            -webkit-text-fill-color: {'#38BDF8' if is_dark else '#0284C7'} !important;
        }}

        div[data-testid="stTab"][aria-selected="true"],
        div[role="tab"][aria-selected="true"],
        button[role="tab"][aria-selected="true"],
        button[data-testid="stTab"][aria-selected="true"],
        div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
            background: {nav_active_bg} !important;
            background-color: {nav_active_bg} !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35) !important;
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

        /* Publication Feed Cards */
        .icare-feed-card {{
            background: {bg_card};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 14px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 6px rgba(0,0,0,{'0.1' if is_dark else '0.02'});
        }}

        .icare-feed-card:hover {{
            border-color: {border_hover};
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,{'0.25' if is_dark else '0.06'});
        }}

        .feed-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: {text_primary};
            margin-bottom: 6px;
            line-height: 1.4;
        }}

        .feed-meta {{
            font-size: 0.86rem;
            color: {text_secondary};
            margin-bottom: 10px;
        }}

        .feed-tag-row {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .tag-pill {{
            background: {bg_card_secondary};
            color: {text_secondary};
            border: 1px solid {border_color};
            font-size: 0.78rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 6px;
        }}

        /* Badges for Quartiles */
        .badge-q1 {{
            background-color: {'rgba(16, 185, 129, 0.2)' if is_dark else '#DCFCE7'};
            color: {'#34D399' if is_dark else '#15803D'};
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 9999px;
            border: 1px solid {'#10B981' if is_dark else '#86EFAC'};
            font-size: 0.78rem;
        }}
        .badge-q2 {{
            background-color: {'rgba(59, 130, 246, 0.2)' if is_dark else '#DBEAFE'};
            color: {'#60A5FA' if is_dark else '#1D4ED8'};
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 9999px;
            border: 1px solid {'#3B82F6' if is_dark else '#93C5FD'};
            font-size: 0.78rem;
        }}
        .badge-q3 {{
            background-color: {'rgba(245, 158, 11, 0.2)' if is_dark else '#FEF3C7'};
            color: {'#FBBF24' if is_dark else '#B45309'};
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 9999px;
            border: 1px solid {'#F59E0B' if is_dark else '#FDE68A'};
            font-size: 0.78rem;
        }}
        .badge-q4 {{
            background-color: {'rgba(239, 68, 68, 0.2)' if is_dark else '#FEE2E2'};
            color: {'#F87171' if is_dark else '#B91C1C'};
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 9999px;
            border: 1px solid {'#EF4444' if is_dark else '#FCA5A5'};
            font-size: 0.78rem;
        }}

        /* Author Intelligence & Dossier Styling */
        .author-dossier-card {{
            background: {bg_card};
            border: 1.5px solid {border_color};
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(0,0,0,{'0.18' if is_dark else '0.06'});
        }}

        .author-dossier-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
            padding-bottom: 18px;
            border-bottom: 1px solid {border_color};
            margin-bottom: 20px;
        }}

        .author-avatar-circle {{
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0284C7, #2563EB);
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 800;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
        }}

        .author-metric-chip {{
            background: {'rgba(14, 30, 54, 0.8)' if is_dark else '#F1F5F9'};
            border: 1px solid {border_color};
            border-radius: 10px;
            padding: 10px 16px;
            text-align: center;
            min-width: 110px;
        }}

        .author-metric-value {{
            font-size: 1.35rem;
            font-weight: 800;
            color: {'#38BDF8' if is_dark else '#0284C7'};
            line-height: 1.2;
        }}

        .author-metric-label {{
            font-size: 0.72rem;
            font-weight: 700;
            color: {text_secondary};
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        /* Podium Cards for Top 3 Authors */
        .podium-card {{
            background: {bg_card};
            border-radius: 14px;
            padding: 20px 16px;
            text-align: center;
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 4px 14px rgba(0,0,0,{'0.15' if is_dark else '0.05'});
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .podium-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 24px rgba(0,0,0,{'0.25' if is_dark else '0.10'});
        }}

        .podium-gold {{
            border: 2px solid #F59E0B;
            background: {'linear-gradient(180deg, rgba(245, 158, 11, 0.12) 0%, #0B192C 100%)' if is_dark else 'linear-gradient(180deg, #FFFBEB 0%, #FFFFFF 100%)'};
        }}

        .podium-silver {{
            border: 2px solid #94A3B8;
            background: {'linear-gradient(180deg, rgba(148, 163, 184, 0.12) 0%, #0B192C 100%)' if is_dark else 'linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%)'};
        }}

        .podium-bronze {{
            border: 2px solid #D97706;
            background: {'linear-gradient(180deg, rgba(217, 119, 6, 0.12) 0%, #0B192C 100%)' if is_dark else 'linear-gradient(180deg, #FFF7ED 0%, #FFFFFF 100%)'};
        }}

        /* ========================================================= */
        /* DESKTOP VIEWPORT (min-width: 769px): SIDEBAR ALWAYS OPEN */
        /* ========================================================= */
        @media (min-width: 769px) {{
            section[data-testid="stSidebar"],
            section[data-testid="stSidebar"][aria-expanded="false"],
            section[data-testid="stSidebar"][aria-expanded="true"],
            [data-testid="stSidebar"] {{
                transform: none !important;
                margin-left: 0 !important;
                left: 0 !important;
                min-width: 336px !important;
                max-width: 336px !important;
                width: 336px !important;
                visibility: visible !important;
                display: flex !important;
                flex-direction: column !important;
                opacity: 1 !important;
                position: relative !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
            [data-testid="stSidebarContent"] {{
                display: flex !important;
                flex-direction: column !important;
                visibility: visible !important;
                opacity: 1 !important;
                width: 100% !important;
            }}

            /* Remove collapse button and sidebar header on desktop so sidebar is permanently locked open */
            [data-testid="stSidebarHeader"],
            [data-testid="stSidebarHeader"] *,
            section[data-testid="stSidebar"] [data-testid="stSidebarHeader"],
            section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] *,
            section[data-testid="stSidebar"] button[kind="headerNoPadding"],
            section[data-testid="stSidebar"] button[kind="headerNoPadding"] *,
            section[data-testid="stSidebar"] button[data-testid*="headerNoPadding"],
            section[data-testid="stSidebar"] button[data-testid*="headerNoPadding"] *,
            section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
            section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] *,
            button[data-testid="stSidebarCollapseButton"],
            [data-testid="stSidebarCollapseButton"],
            button[data-testid="stExpandSidebarButton"],
            [data-testid="collapsedControl"] {{
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                pointer-events: none !important;
                width: 0 !important;
                height: 0 !important;
                min-height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
        }}

        /* ========================================================= */
        /* MOBILE RESPONSIVE LAYER (Strictly Scoped <= 768px & <= 480px) */
        /* ========================================================= */
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
                pointer-events: auto !important;
                cursor: pointer !important;
            }}

            button[data-testid="stExpandSidebarButton"] * {{
                color: #FFFFFF !important;
                fill: #FFFFFF !important;
                stroke: #FFFFFF !important;
            }}

            [data-testid="stSidebarHeader"],
            section[data-testid="stSidebar"] [data-testid="stSidebarHeader"],
            button[data-testid="stSidebarCollapseButton"],
            [data-testid="stSidebarCollapseButton"],
            section[data-testid="stSidebar"] button[kind="headerNoPadding"],
            section[data-testid="stSidebar"] button[data-testid*="headerNoPadding"] {{
                display: flex !important;
                visibility: visible !important;
                pointer-events: auto !important;
                cursor: pointer !important;
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

            /* Topbar Mobile */
            .icare-topbar {{
                margin: 0 0 16px 0 !important;
                padding: 12px 14px !important;
                border-radius: 12px !important;
                flex-direction: column !important;
                align-items: flex-start !important;
                gap: 12px !important;
            }}

            .icare-brand-group {{
                width: 100% !important;
                justify-content: space-between !important;
                flex-wrap: wrap !important;
            }}

            /* Hero Banner Mobile */
            .icare-hero {{
                padding: 18px 14px !important;
                margin-bottom: 18px !important;
            }}

            .hero-title {{
                font-size: 1.35rem !important;
                line-height: 1.25 !important;
            }}

            .hero-subtitle {{
                font-size: 0.82rem !important;
            }}

            .hero-rank-box {{
                text-align: left !important;
                margin-top: 12px !important;
                width: 100% !important;
                border-top: 1px solid {border_color} !important;
                padding-top: 10px !important;
            }}

            .hero-rank-val {{
                font-size: 1.9rem !important;
            }}

            /* Tab Bar Mobile: Touch Horizontal Scroll */
            div[data-baseweb="tab-list"],
            div[data-testid="stTabs"] div[role="tablist"],
            div[data-testid="stTabs"] [role="tablist"],
            div[data-testid="stTabs"] [data-baseweb="tab-list"] {{
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                justify-content: flex-start !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
                scrollbar-width: none !important;
                gap: 6px !important;
                padding: 4px 6px !important;
                width: 100% !important;
            }}

            div[data-baseweb="tab-list"]::-webkit-scrollbar,
            div[data-testid="stTabs"] div[role="tablist"]::-webkit-scrollbar {{
                display: none !important;
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
                white-space: nowrap !important;
            }}

            /* Action Toolbar & Download Buttons */
            .toolbar-title {{
                font-size: 0.92rem !important;
                margin-bottom: 8px !important;
            }}

            /* KPI Cards Mobile */
            .icare-kpi-card {{
                padding: 14px 12px !important;
            }}

            .icare-kpi-value {{
                font-size: 1.5rem !important;
            }}

            /* Author Dossier Card Mobile */
            .author-dossier-card {{
                padding: 16px 14px !important;
            }}

            .author-dossier-header {{
                flex-direction: column !important;
                align-items: flex-start !important;
                gap: 12px !important;
            }}

            /* Feed Card Mobile */
            .icare-feed-card {{
                padding: 14px 14px !important;
            }}

            .feed-title {{
                font-size: 0.95rem !important;
            }}
        }}

        @media (max-width: 480px) {{
            .hero-title {{
                font-size: 1.20rem !important;
            }}

            .hero-badge-group {{
                gap: 4px !important;
            }}

            .hero-pill {{
                font-size: 0.72rem !important;
                padding: 3px 8px !important;
            }}

            .icare-kpi-value {{
                font-size: 1.35rem !important;
            }}
        /* ========================================================= */
        /* AI RESEARCH COPILOT & CHATBOT STYLES */
        /* ========================================================= */
        .ai-copilot-header {{
            background: {'linear-gradient(135deg, rgba(2, 132, 199, 0.18) 0%, rgba(14, 30, 54, 0.75) 100%)' if is_dark else 'linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)'};
            border: 1px solid {'#0284C7' if is_dark else '#93C5FD'};
            border-radius: 14px;
            padding: 18px 22px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .ai-badge-title {{
            font-size: 1.15rem;
            font-weight: 800;
            color: {'#FFFFFF' if is_dark else '#0F172A'};
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .ai-badge-sub {{
            font-size: 0.82rem;
            color: {'#38BDF8' if is_dark else '#0284C7'};
            font-weight: 600;
            margin-top: 2px;
        }}

        .ai-quick-prompts-label {{
            font-size: 0.82rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {'#94A3B8' if is_dark else '#64748B'};
            margin-bottom: 8px;
        }}

        /* Streamlit Chat Elements Theme Overrides */
        [data-testid="stChatMessage"] {{
            background-color: {'#0D1B2E' if is_dark else '#FFFFFF'} !important;
            border: 1px solid {'#1E3250' if is_dark else '#E2E8F0'} !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            margin-bottom: 12px !important;
            box-shadow: {'0 4px 12px rgba(0,0,0,0.25)' if is_dark else '0 2px 8px rgba(0,0,0,0.05)'} !important;
        }}

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {{
                line-height: 1.6 !important;
            }}

            [data-testid="stChatInput"] {{
                background-color: {'#0E1E36' if is_dark else '#FFFFFF'} !important;
                border-color: {'#1E3A5F' if is_dark else '#CBD5E1'} !important;
                border-radius: 12px !important;
            }}

            [data-testid="stChatInput"] textarea {{
                color: {'#FFFFFF' if is_dark else '#0F172A'} !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }}

            /* ========================================================= */
            /* EXECUTIVE BRIEFING & BENCHMARK STYLES */
            /* ========================================================= */
            .executive-briefing-box {{
                background: {'linear-gradient(180deg, #0D1B2E 0%, #08111E 100%)' if is_dark else 'linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%)'};
                border: 1px solid {'#1E3A5F' if is_dark else '#CBD5E1'};
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 24px;
                box-shadow: {'0 8px 30px rgba(0, 0, 0, 0.4)' if is_dark else '0 4px 20px rgba(0, 0, 0, 0.08)'};
            }}

            .executive-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid {'#1E3A5F' if is_dark else '#E2E8F0'};
                padding-bottom: 16px;
                margin-bottom: 20px;
                flex-wrap: wrap;
                gap: 12px;
            }}

            .executive-title {{
                font-size: 1.45rem;
                font-weight: 800;
                color: {'#FFFFFF' if is_dark else '#0F172A'};
                letter-spacing: -0.02em;
            }}

            .executive-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 14px;
                margin-bottom: 22px;
            }}

            .executive-stat-card {{
                background: {'rgba(15, 23, 42, 0.6)' if is_dark else '#F1F5F9'};
                border: 1px solid {'rgba(255, 255, 255, 0.08)' if is_dark else '#E2E8F0'};
                border-radius: 10px;
                padding: 12px 14px;
                text-align: center;
            }}

            .executive-stat-val {{
                font-size: 1.35rem;
                font-weight: 800;
                color: {'#38BDF8' if is_dark else '#0284C7'};
            }}

            .executive-stat-lbl {{
                font-size: 0.75rem;
                font-weight: 700;
                color: {'#94A3B8' if is_dark else '#64748B'};
                text-transform: uppercase;
                letter-spacing: 0.04em;
                margin-top: 2px;
            }}

            /* ========================================================= */
            /* PRINT MEDIA OPTIMIZATIONS (Page-as-it-is Print) */
            /* ========================================================= */
            @media print {{
                * {{
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    color-adjust: exact !important;
                }}
                header[data-testid="stHeader"],
                footer,
                #MainMenu,
                .stDeployButton,
                button[data-testid="stExpandSidebarButton"],
                section[data-testid="stSidebar"] {{
                    display: none !important;
                }}
                .main .block-container {{
                    padding: 12px 16px !important;
                    margin: 0 !important;
                    max-width: 100% !important;
                }}
                .icare-topbar, .icare-hero, .icare-kpi-card, .icare-section-title, .stPlotlyChart, .icare-feed-card, .executive-briefing-box {{
                    break-inside: avoid !important;
                    page-break-inside: avoid !important;
                }}

                /* Targeted Author Profile Print Isolation */
                body.print-author-only-mode .icare-topbar,
                body.print-author-only-mode .icare-hero,
                body.print-author-only-mode .report-toolbar-box,
                body.print-author-only-mode .podium-card,
                body.print-author-only-mode .tab5-top-leaderboard,
                body.print-author-only-mode div[data-testid="stTabs"] > div:first-child,
                body.print-author-only-mode div[data-baseweb="tab-list"],
                body.print-author-only-mode [data-testid="stSelectbox"],
                body.print-author-only-mode [data-testid="stButton"],
                body.print-author-only-mode [data-testid="stDownloadButton"],
                body.print-author-only-mode [data-testid="stRadio"] {{
                    display: none !important;
                }}
                body.print-author-only-mode .author-print-banner {{
                    display: block !important;
                    margin-bottom: 20px !important;
                }}
            }}
        }}
    </style>
    """


def render_icare_topbar(theme: str = "dark") -> str:
    """Renders the top navigation bar with authentic ICARE and COEP logos."""
    is_dark = theme == "dark"
    icare_b64 = get_base64_image("assets/icare_logo.jpg")
    coep_b64 = get_base64_image("assets/coep_logo.png")
    
    icare_img_html = f'<img src="{icare_b64}" alt="ICARE Ratings & Rankings" style="height: 42px; border-radius: 6px; background: #FFFFFF; padding: 3px 8px; object-fit: contain; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">' if icare_b64 else '<div class="icare-logo-badge"><span style="color: #0284C7;">I</span>CARE</div>'
    
    coep_img_html = f'<img src="{coep_b64}" alt="COEP Logo" style="height: 48px; object-fit: contain; background: #FFFFFF; border-radius: 6px; padding: 2px 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">' if coep_b64 else '🏛️'
    
    return f"""
    <div class="icare-topbar">
        <div class="icare-brand-group">
            {icare_img_html}
            <div class="icare-intel-badge">PORTAL INTELLIGENCE</div>
            <div class="icare-subtext">
                <span>📈 COEP Live Scopus Intelligence Dashboard</span>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="display: flex; flex-direction: column; text-align: right;">
                <span style="font-weight: 800; font-size: 1rem; color: {'#FFFFFF' if is_dark else '#0F172A'}; letter-spacing: -0.01em;">COEP Technological University</span>
                <span style="font-size: 0.78rem; color: #0284C7; font-weight: 700;">IR-E-U-1257 • Pune, Maharashtra</span>
            </div>
            {coep_img_html}
        </div>
    </div>
    """


def render_icare_hero(total_pubs: int, total_cites: int, theme: str = "dark") -> str:
    """Renders the top institutional hero banner matching the ICARE portal."""
    is_dark = theme == "dark"
    return f"""
    <div class="icare-hero">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
            <div>
                <div class="hero-badge-group">
                    <span class="hero-pill hero-pill-gold">🏆 Scopus Research Dossier</span>
                    <span class="hero-pill">🏛️ State Technological University (Estd. 1854)</span>
                    <span class="hero-pill hero-pill-cyan">⭐ NAAC A+ (CGPA 3.42)</span>
                    <span class="hero-pill" style="border-color: #0284C7; color: {'#38BDF8' if is_dark else '#0284C7'};">📜 NIRF Category: Engineering</span>
                </div>
                <div class="hero-title">COEP Live Scopus Intelligence Dashboard</div>
                <div class="hero-subtitle">COEP Technological University, Pune • Elsevier Scopus Bibliometrics & Global Research Impact</div>
            </div>
            <div class="hero-rank-box">
                <div class="hero-rank-label">TOTAL SCOPUS OUTPUT</div>
                <div class="hero-rank-val">#{total_pubs:,}</div>
                <div style="font-size: 0.84rem; color: {'#94A3B8' if is_dark else '#475569'}; font-weight: 700;">{total_cites:,} Citations Accrued</div>
            </div>
        </div>
    </div>
    """


def render_icare_kpi_card(title: str, value: str, subtitle: str = "", icon: str = "📊", color_theme: str = "blue") -> str:
    """Renders a styled ICARE metric card with colored top accent, icon, and sub-pill."""
    return f"""
    <div class="icare-kpi-card">
        <div>
            <div class="kpi-header-row">
                <div class="icare-kpi-title">{title}</div>
                <div class="kpi-icon-badge icon-{color_theme}">{icon}</div>
            </div>
            <div class="icare-kpi-value">{value}</div>
        </div>
        {f'<div class="kpi-footer-pill pill-{color_theme}">{subtitle}</div>' if subtitle else ''}
    </div>
    """


def get_plotly_theme(theme: str = "dark") -> dict:
    """Returns matching color palette and transparent backgrounds for Plotly charts."""
    is_dark = theme == "dark"
    font_color = "#FFFFFF" if is_dark else "#0F172A"
    return {
        "template": "plotly_dark" if is_dark else "plotly_white",
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": font_color, "family": "Plus Jakarta Sans"},
    }


def style_plotly_fig(fig, theme: str = "dark"):
    """Applies high-contrast dark or light styling to any Plotly figure."""
    is_dark = theme == "dark"
    font_color = "#FFFFFF" if is_dark else "#0F172A"
    grid_color = "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(15, 23, 42, 0.08)"
    zeroline_color = "rgba(255, 255, 255, 0.15)" if is_dark else "rgba(15, 23, 42, 0.15)"
    
    fig.update_layout(
        template="plotly_dark" if is_dark else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=font_color, family="Plus Jakarta Sans", size=12),
        legend=dict(
            font=dict(color=font_color, family="Plus Jakarta Sans", size=11),
            title=dict(font=dict(color=font_color, family="Plus Jakarta Sans", size=12))
        ),
        hoverlabel=dict(
            font_color="#FFFFFF" if is_dark else "#0F172A",
            font_family="Plus Jakarta Sans"
        ),
        xaxis=dict(
            color=font_color,
            tickfont=dict(color=font_color, family="Plus Jakarta Sans", size=11),
            title=dict(font=dict(color=font_color, family="Plus Jakarta Sans", size=12)),
            gridcolor=grid_color,
            zerolinecolor=zeroline_color
        ),
        yaxis=dict(
            color=font_color,
            tickfont=dict(color=font_color, family="Plus Jakarta Sans", size=11),
            title=dict(font=dict(color=font_color, family="Plus Jakarta Sans", size=12)),
            gridcolor=grid_color,
            zerolinecolor=zeroline_color
        )
    )
    if hasattr(fig.layout, 'yaxis2') and fig.layout.yaxis2:
        fig.update_layout(
            yaxis2=dict(
                color=font_color,
                tickfont=dict(color=font_color, family="Plus Jakarta Sans", size=11),
                title=dict(font=dict(color=font_color, family="Plus Jakarta Sans", size=12)),
                gridcolor=grid_color,
            )
        )
    return fig

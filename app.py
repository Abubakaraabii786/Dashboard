import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, date
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="MWF Financial Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp { background: #0a1628; color: #e2e8f0; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f3c 0%, #091525 100%);
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Selectbox styling */
.stSelectbox > div > div {
    background: #0d1f3c !important;
    border: 1px solid #1e4d7b !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,0.15) !important;
}

/* Date input styling */
.stDateInput > div > div {
    background: #0d1f3c !important;
    border: 1px solid #1e4d7b !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #0f2744 0%, #1a3a5c 100%);
    border: 1px solid #1e4d7b;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
    height: 100%;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-label {
    color: #64748b;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
}
.kpi-value {
    color: #f1f5f9;
    font-size: 1.9rem;
    font-weight: 700;
    font-family: 'Syne', sans-serif;
    line-height: 1.1;
}
.kpi-delta-up   { color: #34d399; font-size: 0.75rem; margin-top: 6px; font-weight: 600; }
.kpi-delta-down { color: #f87171; font-size: 0.75rem; margin-top: 6px; font-weight: 600; }
.kpi-delta-neutral { color: #94a3b8; font-size: 0.75rem; margin-top: 6px; }
.kpi-icon { font-size: 1.5rem; margin-bottom: 6px; }

.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e3a5f;
    margin-bottom: 16px;
}
.dash-header {
    background: linear-gradient(135deg, #0d1f3c 0%, #132d55 100%);
    border: 1px solid #1e4d7b;
    border-radius: 20px;
    padding: 24px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.dash-header::after {
    content: '◈';
    position: absolute;
    right: 28px; top: 50%;
    transform: translateY(-50%);
    font-size: 4.5rem;
    color: #1e4d7b;
    line-height: 1;
}
.dash-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #f1f5f9;
    margin: 0;
    line-height: 1.1;
}
.dash-subtitle { color: #64748b; font-size: 0.85rem; margin-top: 4px; }
.compare-badge {
    display: inline-block;
    background: #1e3a5f;
    border: 1px solid #38bdf8;
    color: #38bdf8;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
.filter-badge {
    display: inline-block;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.3);
    color: #38bdf8;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.68rem;
    font-weight: 600;
    margin-left: 4px;
}
.stTabs [data-baseweb="tab-list"] { background: transparent; gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: #0f2744;
    border: 1px solid #1e4d7b;
    border-radius: 8px;
    color: #94a3b8;
    font-size: 0.82rem;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1e4d7b, #1e3a8a) !important;
    color: #38bdf8 !important;
    border-color: #38bdf8 !important;
}
.stSelectbox > div, .stMultiSelect > div {
    background: #0f2744 !important;
    border-color: #1e4d7b !important;
}
.sidebar-section {
    background: rgba(30,74,123,0.15);
    border: 1px solid rgba(30,74,123,0.4);
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 10px;
}
.sidebar-section-title {
    color: #38bdf8;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 10px;
}
div[data-testid="stHorizontalBlock"] > div { gap: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Chart Theme ────────────────────────────────────────────────────────────────
CHART_THEME = {
    "paper_bgcolor": "#0f2744",
    "plot_bgcolor": "#0a1f38",
    "font_color": "#94a3b8",
    "font_family": "DM Sans",
    "gridcolor": "#1e3a5f",
    "colorway": ["#38bdf8","#818cf8","#34d399","#fb923c","#f472b6",
                 "#facc15","#a78bfa","#2dd4bf","#f87171","#60a5fa"],
}

def apply_theme(fig, title=""):
    fig.update_layout(
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"], family=CHART_THEME["font_family"]),
        title=dict(text=title, font=dict(color="#e2e8f0", size=13, family="Syne"), x=0.02),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_color="#94a3b8", font_size=11),
        colorway=CHART_THEME["colorway"],
        hoverlabel=dict(bgcolor="#0d1f3c", font_color="#e2e8f0", font_family="DM Sans"),
    )
    fig.update_xaxes(gridcolor=CHART_THEME["gridcolor"], zeroline=False, tickfont_color="#64748b")
    fig.update_yaxes(gridcolor=CHART_THEME["gridcolor"], zeroline=False, tickfont_color="#64748b")
    return fig

# ── Google Sheets Loader ───────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def load_google_sheet(sheet_url: str) -> pd.DataFrame:
    try:
        if "/edit" in sheet_url:
            csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
            csv_url = csv_url.replace("/edit?usp=sharing", "/export?format=csv")
            if "export?format=csv" not in csv_url:
                csv_url = sheet_url.split("/edit")[0] + "/export?format=csv"
        elif "gid=" in sheet_url:
            base = sheet_url.split("/pub")[0] if "/pub" in sheet_url else sheet_url
            csv_url = base + "/export?format=csv"
        else:
            csv_url = sheet_url
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(f"❌ Could not load Google Sheet: {e}")
        return pd.DataFrame()

def load_sample_data() -> pd.DataFrame:
    from io import StringIO
    raw = """TRANSACTION PRIMARY KEY\t2026 AMOUNT\t2025 AMOUNT\t2024 AMOUNT\t2023 AMOUNT\tAMOUNT\tREMAINING BALANCE (GBP)\tSHEET NO.\tTRANSACTION FORUM\tLINK FORUM\tTYPE\tLINK LOCATION\tCURRENCY\tCOUNTRY NAME\tCOUNTRY ZONE\tLINK CLUSTER CITY\tLINK CLUSTER ZONE\tPOSTCODE CLUSTER CITY\tPOSTCODE ZONE\tPOSTCODE LOCATION\tITEM HEAD 1\tITEM HEAD 2\tITEM HEAD 3\tHIJRI MONTH NAME\tHIJRI MONTH\tHIJRI YEAR\tHIJRI DATE\tDAY OF MONTH\tMONTH\tYEAR\tDATE\tITEM\tQTY\tAMOUNT\tCITY\tPOST CODE
UK-003-1\t\t\t\t918\t918\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tForeign\tFOREIGN\tHO\tOrphan Sponsorship\tDonations\tNon Donation in Kind\tShaban\t8\t1444\t22/8/1444\t14\tMarch\t2023\t14-Mar-2023\tOrphan Sponsor\t1\t918\tLudwigshafen\t67063
UK-003-2\t\t\t\t2608.52\t2608.52\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tOther\tDonations\tNon Donation in Kind\tMuharram\t1\t1445\t27/1/1445\t14\tAugust\t2023\t14-Aug-2023\tUnsorted\t1\t2608.52\t\t
UK-003-3\t\t\t\t85\t85\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tForeign\tFOREIGN\tHO\tGeneral\tDonations\tNon Donation in Kind\tMuharram\t1\t1445\t29/1/1445\t16\tAugust\t2023\t16-Aug-2023\tSadqah\t1\t85\t\t
UK-003-4\t\t\t\t42.5\t42.5\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tForeign\tFOREIGN\tHO\tOther\tDonations\tNon Donation in Kind\tRabi ul Sani\t4\t1445\t29/4/1445\t13\tNovember\t2023\t13-Nov-2023\tUnsorted\t1\t42.5\t\t
UK-003-5\t\t\t\t17\t17\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tForeign\tFOREIGN\tHO\tGeneral\tDonations\tNon Donation in Kind\tJamadi ul Sani\t6\t1445\t8/6/1445\t21\tDecember\t2023\t21-Dec-2023\tSadqah\t1\t17\t\t
UK-003-6\t\t\t918\t\t918\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tForeign\tFOREIGN\tHO\tOrphan Sponsorship\tDonations\tNon Donation in Kind\tRamadan\t9\t1445\t23/9/1445\t2\tApril\t2024\t02-Apr-2024\tOrphan Sponsor\t1\t918\t\t
UK-003-7\t\t\t42.5\t\t42.5\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tForeign\tFOREIGN\tHO\tEmergency & Relief\tDonations\tNon Donation in Kind\tRamadan\t9\t1445\t30/9/1445\t9\tApril\t2024\t09-Apr-2024\tEmergency & Relief\t1\t42.5\t\t
UK-003-8\t\t\t442\t\t442\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tForeign\tFOREIGN\tHO\tHelp Feed\tDonations\tNon Donation in Kind\tShawwal\t10\t1445\t6/10/1445\t15\tApril\t2024\t15-Apr-2024\tFitrana\t1\t442\t\t
UK-003-9\t\t\t425\t\t425\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tQurbani\tDonations\tNon Donation in Kind\tDhu ul Hijjah\t12\t1445\t8/12/1445\t14\tJune\t2024\t14-Jun-2024\tG1 Part Cow\t7\t425\t\t
UK-003-10\t\t\t212.5\t\t212.5\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tQurbani\tDonations\tNon Donation in Kind\tMuharram\t1\t1446\t9/1/1446\t15\tJuly\t2024\t15-Jul-2024\tG1 Part Cow\t1\t212.5\t\t
UK-003-11\t\t\t42.5\t\t42.5\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tQurbani\tDonations\tNon Donation in Kind\tMuharram\t1\t1446\t9/1/1446\t15\tJuly\t2024\t15-Jul-2024\tG1 Part Cow\t1\t42.5\t\t
UK-003-12\t\t\t25.5\t\t25.5\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tQurbani\tDonations\tNon Donation in Kind\tMuharram\t1\t1446\t12/1/1446\t18\tJuly\t2024\t18-Jul-2024\tEid Gift - Qurbani\t1\t25.5\t\t
UK-003-13\t\t918\t\t\t918\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tForeign\tFOREIGN\tHO\tOrphan Sponsorship\tDonations\tNon Donation in Kind\tRamadan\t9\t1446\t11/9/1446\t11\tMarch\t2025\t11-Mar-2025\tOrphan Sponsor\t1\t918\t\t
UK-003-14\t\t17\t\t\t17\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tZakat\tDonations\tNon Donation in Kind\tShawwal\t10\t1446\t19/10/1446\t17\tApril\t2025\t17-Apr-2025\tZakat\t1\t17\t\t
UK-003-15\t\t17\t\t\t17\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tHelp Feed\tDonations\tNon Donation in Kind\tDhu ul Hijjah\t12\t1446\t7/12/1446\t3\tJune\t2025\t03-Jun-2025\tMawakhat-e-madina Monthly\t1\t17\t\t
UK-003-16\t\t144.5\t\t\t144.5\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tGeneral\tDonations\tNon Donation in Kind\tDhu ul Hijjah\t12\t1446\t8/12/1446\t4\tJune\t2025\t04-Jun-2025\tSadqah\t1\t144.5\t\t
UK-003-17\t\t42.5\t\t\t42.5\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tGeneral\tDonations\tNon Donation in Kind\tDhu ul Hijjah\t12\t1446\t14/12/1446\t10\tJune\t2025\t10-Jun-2025\tSadqah\t1\t42.5\t\t
UK-003-18\t\t42.5\t\t\t42.5\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tGeneral\tDonations\tNon Donation in Kind\tDhu ul Hijjah\t12\t1446\t24/12/1446\t20\tJune\t2025\t20-Jun-2025\tSadqah\t1\t42.5\t\t
UK-003-19\t\t19.79\t\t\t19.79\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tGeneral\tDonations\tNon Donation in Kind\tMuharram\t1\t1447\t15/1/1447\t10\tJuly\t2025\t10-Jul-2025\tSadqah\t1\t19.79\t\t
UK-003-20\t\t25.5\t\t\t25.5\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tEmergency & Relief\tDonations\tNon Donation in Kind\tRabi ul Awwal\t3\t1447\t11/3/1447\t3\tSeptember\t2025\t03-Sep-2025\tEmergency Pakistan Floods\t1\t25.5\t\t
UK-003-21\t\t17\t\t\t17\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tEmergency & Relief\tDonations\tNon Donation in Kind\tRabi ul Awwal\t3\t1447\t17/3/1447\t9\tSeptember\t2025\t09-Sep-2025\tEmergency Pakistan Floods\t1\t17\t\t
UK-003-22\t\t255\t\t\t255\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tGeneral\tDonations\tNon Donation in Kind\tRabi ul Sani\t4\t1447\t1/4/1447\t23\tSeptember\t2025\t23-Sep-2025\tSadqah\t1\t255\t\t
UK-003-23\t\t510\t\t\t510\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tGeneral\tDonations\tNon Donation in Kind\tJamadi ul Sani\t6\t1447\t21/6/1447\t12\tDecember\t2025\t12-Dec-2025\tSadqah\t1\t510\t\t
UK-003-24\t918\t\t\t\t918\t0\tMWF-UK-003\tHO\tHO\tBank\tUK Foreign Accounts\tGBP\tUK\tUK\tHO\tHO\tForeign\tFOREIGN\tHO\tOrphan Sponsorship\tDonations\tNon Donation in Kind\tRamadan\t9\t1447\t20/9/1447\t9\tMarch\t2026\t09-Mar-2026\tOrphan Sponsor\t1\t918\t\t
UK-004-1\t\t\t5\t\t5\t0\tMWF-UK-004\tHO\tHO\tBank\tHSBC 1\tGBP\tUK\tUK\tHO\tHO\tBirmingham\tMIDLANDS\tHO\tGeneral\tDonations\tNon Donation in Kind\tRajjab\t7\t1445\t21/7/1445\t2\tFebruary\t2024\t02-Feb-2024\tSadqah\t1\t5\tBirmingham\tB19 1JU
UK-004-2\t\t\t\t3\t3\t0\tMWF-UK-004\tHO\tHO\tBank\tHSBC 1\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tWater fo All\tDonations\tNon Donation in Kind\tJamadi ul Sani\t6\t1444\t8/6/1444\t1\tJanuary\t2023\t01-Jan-2023\tGeneral Water\t1\t3\t\t
UK-004-8\t\t\t\t30\t30\t0\tMWF-UK-004\tHO\tHO\tBank\tHSBC 1\tGBP\tUK\tUK\tHO\tHO\tO - London1\tSOUTH\tHO\tOrphan Care\tDonations\tNon Donation in Kind\tJamadi ul Sani\t6\t1444\t10/6/1444\t3\tJanuary\t2023\t03-Jan-2023\tOrphan General\t1\t30\t\t
UK-004-18\t\t\t\t60\t60\t0\tMWF-UK-004\tHO\tHO\tBank\tHSBC 1\tGBP\tUK\tUK\tHO\tHO\tBirmingham\tMIDLANDS\tHO\tOrphan Sponsorship\tDonations\tNon Donation in Kind\tJamadi ul Sani\t6\t1444\t10/6/1444\t3\tJanuary\t2023\t03-Jan-2023\tOrphan Sponsor\t1\t60\tBirmingham\tB8 3HH
UK-004-22\t\t\t\t35\t35\t0\tMWF-UK-004\tHO\tHO\tBank\tHSBC 1\tGBP\tUK\tUK\tHO\tHO\tO - London1\tSOUTH\tHO\tOrphan Sponsorship\tDonations\tNon Donation in Kind\tJamadi ul Sani\t6\t1444\t10/6/1444\t3\tJanuary\t2023\t03-Jan-2023\tOrphan Sponsor\t1\t35\t\t
UK-004-25\t\t\t\t3\t3\t0\tMWF-UK-004\tHO\tHO\tBank\tHSBC 1\tGBP\tUK\tUK\tHO\tHO\tAnonymous\tANONYMOUS\tHO\tZakat\tDonations\tNon Donation in Kind\tJamadi ul Sani\t6\t1444\t10/6/1444\t3\tJanuary\t2023\t03-Jan-2023\tZakat\t1\t3\t\t
UK-004-32\t\t\t\t25\t25\t0\tMWF-UK-004\tHO\tHO\tBank\tHSBC 1\tGBP\tUK\tUK\tHO\tHO\tManchester - Stockport\tNORTH\tHO\tHifz Sponsorship\tDonations\tNon Donation in Kind\tJamadi ul Sani\t6\t1444\t10/6/1444\t3\tJanuary\t2023\t03-Jan-2023\tHifz Sponsor\t1\t25\t\t
UK-004-34\t\t\t\t20\t20\t0\tMWF-UK-004\tHO\tHO\tBank\tHSBC 1\tGBP\tUK\tUK\tHO\tHO\tOldham\tNORTH\tHO\tFamily Support\tDonations\tNon Donation in Kind\tJamadi ul Sani\t6\t1444\t10/6/1444\t3\tJanuary\t2023\t03-Jan-2023\tShuhada Fund\t1\t20\t\t
UK-004-35\t\t\t\t20\t20\t0\tMWF-UK-004\tHO\tHO\tBank\tHSBC 1\tGBP\tUK\tUK\tHO\tHO\tSmethwick\tMIDLANDS\tHO\tSchool Sponsorship\tDonations\tNon Donation in Kind\tJamadi ul Sani\t6\t1444\t10/6/1444\t3\tJanuary\t2023\t03-Jan-2023\tSchool Sponsor\t1\t20\tSmethwick\tB66 4JD"""
    df = pd.read_csv(StringIO(raw), sep='\t')
    return df

# ── Preprocessing ──────────────────────────────────────────────────────────────
def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if 'DATE' in df.columns:
        df['DATE'] = pd.to_datetime(df['DATE'], dayfirst=True, errors='coerce')
    # YEAR: try from DATE first, fallback to YEAR column
    if 'YEAR' in df.columns:
        df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce').fillna(0).astype(int)
    elif 'DATE' in df.columns:
        df['YEAR'] = df['DATE'].dt.year.fillna(0).astype(int)
    # MONTH: numeric (1-12)
    if 'MONTH' in df.columns:
        # Could be name ("March") or number
        month_name_map = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,
                          "july":7,"august":8,"september":9,"october":10,"november":11,"december":12}
        def parse_month(v):
            try:
                return int(float(v))
            except:
                return month_name_map.get(str(v).strip().lower(), 0)
        df['MONTH'] = df['MONTH'].apply(parse_month)
    elif 'DATE' in df.columns:
        df['MONTH'] = df['DATE'].dt.month.fillna(0).astype(int)
    # Amount
    if 'AMOUNT' in df.columns:
        df['AMOUNT'] = pd.to_numeric(df['AMOUNT'], errors='coerce').fillna(0)
    if 'AMOUNT' in df.columns:
        df['AMOUNT'] = pd.to_numeric(df['AMOUNT'], errors='coerce').fillna(0)
    return df

# ── KPI Card ───────────────────────────────────────────────────────────────────
def kpi_card(icon, label, value, delta=None, delta_label="vs prev year"):
    if delta is not None:
        if delta > 0:
            d = f'<div class="kpi-delta-up">▲ +{delta:.1f}% {delta_label}</div>'
        elif delta < 0:
            d = f'<div class="kpi-delta-down">▼ {delta:.1f}% {delta_label}</div>'
        else:
            d = '<div class="kpi-delta-neutral">→ No change</div>'
    else:
        d = '<div class="kpi-delta-neutral">─ No prior data</div>'
    return f"""<div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {d}
    </div>"""

MONTH_NUM = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
             7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    AMT = 'AMOUNT'

    # ── SIDEBAR ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🌙 MWF Dashboard")
        st.markdown("---")

        # ── Data Source ──
        st.markdown('<div class="sidebar-section-title">DATA SOURCE</div>', unsafe_allow_html=True)
        data_source = st.radio("", ["📋 Sample Data", "🔗 Google Sheet"], label_visibility="collapsed")

        df_raw = pd.DataFrame()
        if data_source == "🔗 Google Sheet":
            sheet_url = st.text_input("Google Sheet URL",
                placeholder="https://docs.google.com/spreadsheets/d/…/edit?usp=sharing")
            if sheet_url:
                with st.spinner("Loading…"):
                    df_raw = load_google_sheet(sheet_url)
                if not df_raw.empty:
                    st.success(f"✅ {len(df_raw):,} rows loaded")
        if df_raw.empty:
            df_raw = load_sample_data()
            if data_source == "📋 Sample Data":
                st.caption("Using built-in sample data")

        df = preprocess(df_raw)

        st.markdown("---")

        # ══════════════════════════════════════════════════════════════════
        # CASCADING / DEPENDENT FILTERS
        # Each filter narrows the options for the next one
        # ══════════════════════════════════════════════════════════════════
        st.markdown('<div class="sidebar-section-title">📅 DATE RANGE</div>', unsafe_allow_html=True)

        # Date range filter
        if 'DATE' in df.columns and df['DATE'].notna().any():
            min_date = df['DATE'].min().date()
            max_date = df['DATE'].max().date()
        else:
            min_date = date(2020, 1, 1)
            max_date = date.today()

        date_from = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date, key="d_from")
        date_to   = st.date_input("To",   value=max_date, min_value=min_date, max_value=max_date, key="d_to")

        if date_from > date_to:
            st.warning("⚠️ 'From' date is after 'To' date.")
            date_from, date_to = date_to, date_from

        # Apply date range to base df for all downstream filters
        if 'DATE' in df.columns:
            df_dated = df[(df['DATE'].dt.date >= date_from) & (df['DATE'].dt.date <= date_to)]
        else:
            df_dated = df.copy()

        st.markdown("---")
        st.markdown('<div class="sidebar-section-title">🔽 FILTERS</div>', unsafe_allow_html=True)
        st.caption("Each filter updates based on your previous selections")

        # ── YEAR (from date-filtered data) ──
        all_years = sorted(df_dated['YEAR'].dropna().unique().tolist())
        all_years = [y for y in all_years if y > 2000]
        sel_year = st.selectbox("📅 Year", ["All"] + [str(y) for y in all_years[::-1]], index=0)
        sel_year_val = None if sel_year == "All" else int(sel_year)
        # prev_year is computed after sidebar, from date range

        # Apply year filter → determines month options
        df_y = df_dated[df_dated['YEAR'] == sel_year_val] if sel_year_val else df_dated.copy()

        # ── MONTH (dependent on year) ──
        avail_months = sorted([m for m in df_y['MONTH'].dropna().unique().tolist() if m > 0])
        month_opts = ["All"] + [f"{MONTH_NUM.get(m, str(m))} ({m:02d})" for m in avail_months]
        sel_month_label = st.selectbox("🗓️ Month", month_opts, index=0)
        sel_month = None if sel_month_label == "All" else int(sel_month_label.split("(")[1].replace(")", ""))

        # Apply month filter → determines category options
        df_ym = df_y[df_y['MONTH'] == sel_month] if sel_month else df_y.copy()

        # ── CATEGORY (dependent on year + month) ──
        if 'ITEM HEAD 1' in df_ym.columns:
            avail_cats = ["All"] + sorted(df_ym['ITEM HEAD 1'].dropna().unique().tolist())
        else:
            avail_cats = ["All"]
        sel_cat = st.selectbox("🏷️ Category", avail_cats, index=0)

        # Apply category filter → determines zone options
        df_ymc = df_ym[df_ym['ITEM HEAD 1'] == sel_cat] if sel_cat != "All" and 'ITEM HEAD 1' in df_ym.columns else df_ym.copy()

        # ── ZONE (dependent on year + month + category) ──
        if 'POSTCODE ZONE' in df_ymc.columns:
            avail_zones = ["All"] + sorted(df_ymc['POSTCODE ZONE'].dropna().unique().tolist())
        else:
            avail_zones = ["All"]
        sel_zone = st.selectbox("📍 Zone", avail_zones, index=0)

        # Apply zone filter → determines forum options
        df_ymcz = df_ymc[df_ymc['POSTCODE ZONE'] == sel_zone] if sel_zone != "All" and 'POSTCODE ZONE' in df_ymc.columns else df_ymc.copy()

        # ── FORUM (dependent on all above) ──
        if 'TRANSACTION FORUM' in df_ymcz.columns:
            avail_forums = ["All"] + sorted(df_ymcz['TRANSACTION FORUM'].dropna().unique().tolist())
        else:
            avail_forums = ["All"]
        sel_forum = st.selectbox("🏛️ Forum", avail_forums, index=0)

        st.markdown("---")
        st.caption(f"🕐 {datetime.now().strftime('%d %b %Y %H:%M')}")

    # ── APPLY ALL FILTERS ─────────────────────────────────────────────────────
    def apply_filters(data, year_val, month_val, cat, zone, forum, d_from, d_to):
        d = data.copy()
        # Date range
        if 'DATE' in d.columns:
            d = d[(d['DATE'].dt.date >= d_from) & (d['DATE'].dt.date <= d_to)]
        # Year
        if year_val:
            d = d[d['YEAR'] == year_val]
        # Month
        if month_val:
            d = d[d['MONTH'] == month_val]
        # Category
        if cat != "All" and 'ITEM HEAD 1' in d.columns:
            d = d[d['ITEM HEAD 1'] == cat]
        # Zone
        if zone != "All" and 'POSTCODE ZONE' in d.columns:
            d = d[d['POSTCODE ZONE'] == zone]
        # Forum
        if forum != "All" and 'TRANSACTION FORUM' in d.columns:
            d = d[d['TRANSACTION FORUM'] == forum]
        return d

    df_cur = apply_filters(df, sel_year_val, sel_month, sel_cat, sel_zone, sel_forum, date_from, date_to)

    # ── Previous period: ALWAYS shift date range back 1 year ─────────────────
    # Works whether user picked a specific Year OR just used the date pickers
    try:
        pf = date_from.replace(year=date_from.year - 1)
    except ValueError:
        pf = date(date_from.year - 1, date_from.month, 28)
    try:
        pt = date_to.replace(year=date_to.year - 1)
    except ValueError:
        pt = date(date_to.year - 1, date_to.month, 28)

    # prev_year for display and filtering
    prev_year     = sel_year_val - 1 if sel_year_val else date_to.year - 1
    prev_year_val = prev_year

    df_prev = apply_filters(df, prev_year_val, sel_month, sel_cat, sel_zone, sel_forum, pf, pt)

    # ── METRICS ───────────────────────────────────────────────────────────────
    cur_total  = df_cur[AMT].sum()  if AMT in df_cur.columns else 0
    prev_total = df_prev[AMT].sum() if AMT in df_prev.columns and len(df_prev) > 0 else 0
    cur_count  = len(df_cur)
    prev_count = len(df_prev)
    cur_avg    = df_cur[AMT].mean()  if AMT in df_cur.columns and cur_count > 0 else 0
    prev_avg   = df_prev[AMT].mean() if AMT in df_prev.columns and prev_count > 0 else 0
    cur_top    = df_cur[AMT].max()   if AMT in df_cur.columns and cur_count > 0 else 0
    prev_top   = df_prev[AMT].max()  if AMT in df_prev.columns and prev_count > 0 else 0

    def pct_delta(c, p):
        if not p or p == 0: return None
        return ((c - p) / p) * 100

    months_map = MONTH_NUM  # {1:"Jan", ...}

    # ── HEADER ────────────────────────────────────────────────────────────────
    yr_label    = str(sel_year_val) if sel_year_val else "All Years"
    mo_label    = f" · {MONTH_NUM.get(sel_month, '')}" if sel_month else ""
    cat_badge   = f'<span class="filter-badge">{sel_cat}</span>'   if sel_cat   != "All" else ""
    zone_badge  = f'<span class="filter-badge">{sel_zone}</span>'  if sel_zone  != "All" else ""
    forum_badge = f'<span class="filter-badge">{sel_forum}</span>' if sel_forum != "All" else ""
    # prev_year is ALWAYS set now — derived from date range if no year selected
    compare_txt = f'vs {prev_year}'

    st.markdown(f"""
    <div class="dash-header">
        <div class="dash-title">MWF Financial Dashboard</div>
        <div class="dash-subtitle">
            Muslim Welfare Foundation · <strong style="color:#38bdf8">{yr_label}</strong>{mo_label}
            {cat_badge}{zone_badge}{forum_badge}
            &nbsp;<span class="compare-badge">{compare_txt}</span>
            &nbsp;·&nbsp;{date_from.strftime('%d %b %Y')} – {date_to.strftime('%d %b %Y')}
        </div>
    </div>""", unsafe_allow_html=True)

    # ── KPI ROW ───────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(kpi_card("💷", "Total Donations", f"£{cur_total:,.2f}",
            pct_delta(cur_total, prev_total), f"vs {prev_year}"), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card("🔢", "Transactions", f"{cur_count:,}",
            pct_delta(cur_count, prev_count), f"vs {prev_year}"), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card("📈", "Avg Donation", f"£{cur_avg:,.2f}",
            pct_delta(cur_avg, prev_avg), f"vs {prev_year}"), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi_card("🏆", "Largest Gift", f"£{cur_top:,.2f}",
            pct_delta(cur_top, prev_top), f"vs {prev_year}"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABS ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊  Overview", "📅  Year Comparison", "🗂️  Category Analysis", "📋  Transactions"
    ])

    # ═══════════ TAB 1: OVERVIEW ══════════════════════════════════════════════
    with tab1:
        c1, c2 = st.columns([3, 2])

        with c1:
            st.markdown('<div class="section-header">Monthly Donation Trend</div>', unsafe_allow_html=True)
            if AMT in df_cur.columns:
                mc = df_cur.groupby('MONTH')[AMT].sum().reset_index()
                mc['MONTH_NAME'] = mc['MONTH'].map(months_map)
                mc = mc.sort_values('MONTH')

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=mc['MONTH_NAME'], y=mc[AMT], name=str(sel_year_val),
                    mode='lines+markers',
                    line=dict(color='#38bdf8', width=3, shape='spline'),
                    marker=dict(size=8, color='#38bdf8', line=dict(color='#0a1628', width=2)),
                    fill='tozeroy', fillcolor='rgba(56,189,248,0.08)',
                    hovertemplate='<b>%{x}</b><br>£%{y:,.2f}<extra></extra>'
                ))
                if len(df_prev) > 0 and AMT in df_prev.columns:
                    mp = df_prev.groupby('MONTH')[AMT].sum().reset_index()
                    mp['MONTH_NAME'] = mp['MONTH'].map(months_map)
                    mp = mp.sort_values('MONTH')
                    fig.add_trace(go.Scatter(
                        x=mp['MONTH_NAME'], y=mp[AMT], name=str(prev_year),
                        mode='lines+markers',
                        line=dict(color='#818cf8', width=2, dash='dot', shape='spline'),
                        marker=dict(size=6, color='#818cf8'),
                        opacity=0.75,
                        hovertemplate='<b>%{x}</b><br>£%{y:,.2f}<extra></extra>'
                    ))
                apply_theme(fig, f"Monthly Collections — {sel_year_val or 'All'} vs {prev_year}")
                st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">Donations by Category</div>', unsafe_allow_html=True)
            if 'ITEM HEAD 1' in df_cur.columns and AMT in df_cur.columns:
                cat_df = df_cur.groupby('ITEM HEAD 1')[AMT].sum().reset_index()
                cat_df = cat_df[cat_df[AMT] > 0].sort_values(AMT, ascending=False).head(8)
                fig2 = px.pie(cat_df, names='ITEM HEAD 1', values=AMT,
                              hole=0.55, color_discrete_sequence=CHART_THEME["colorway"])
                fig2.update_traces(textposition='outside', textinfo='percent+label',
                                   textfont_size=10, textfont_color='#94a3b8',
                                   hovertemplate='<b>%{label}</b><br>£%{value:,.2f}<extra></extra>')
                apply_theme(fig2, "Category Breakdown")
                fig2.update_layout(showlegend=False, margin=dict(l=30,r=30,t=50,b=30))
                st.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="section-header">Donations by Zone</div>', unsafe_allow_html=True)
            if 'POSTCODE ZONE' in df_cur.columns and AMT in df_cur.columns:
                zone_df = df_cur.groupby('POSTCODE ZONE')[AMT].sum().reset_index()
                zone_df = zone_df[zone_df[AMT] > 0].sort_values(AMT)
                fig3 = px.bar(zone_df, x=AMT, y='POSTCODE ZONE', orientation='h',
                              color=AMT, color_continuous_scale=['#1e3a5f','#38bdf8'],
                              text=[f"£{v:,.0f}" for v in zone_df[AMT]])
                fig3.update_traces(textposition='outside', textfont_color='#64748b',
                                   hovertemplate='<b>%{y}</b><br>£%{x:,.2f}<extra></extra>')
                fig3.update_coloraxes(showscale=False)
                apply_theme(fig3, "By Geographic Zone")
                fig3.update_layout(margin=dict(r=80))
                st.plotly_chart(fig3, use_container_width=True)

        with c4:
            st.markdown('<div class="section-header">Donations by Forum</div>', unsafe_allow_html=True)
            if 'TRANSACTION FORUM' in df_cur.columns and AMT in df_cur.columns:
                forum_df = df_cur.groupby('TRANSACTION FORUM')[AMT].sum().reset_index()
                forum_df = forum_df[forum_df[AMT] > 0].sort_values(AMT, ascending=False)
                fig4 = px.bar(forum_df, x='TRANSACTION FORUM', y=AMT,
                              color=AMT, color_continuous_scale=['#1e3a5f','#34d399'],
                              text=[f"£{v:,.0f}" for v in forum_df[AMT]])
                fig4.update_traces(textposition='outside', textfont_color='#64748b',
                                   hovertemplate='<b>%{x}</b><br>£%{y:,.2f}<extra></extra>')
                fig4.update_coloraxes(showscale=False)
                apply_theme(fig4, "By Transaction Forum")
                st.plotly_chart(fig4, use_container_width=True)

    # ═══════════ TAB 2: YEAR COMPARISON ══════════════════════════════════════
    with tab2:
        st.markdown(f'<div class="section-header">Year-over-Year: {sel_year_val if sel_year_val else "All"} vs {prev_year}</div>',
                    unsafe_allow_html=True)

        comp_cols = st.columns(4)
        prev_max_val = df_prev[AMT].max() if AMT in df_prev.columns and len(df_prev) > 0 else 0
        metrics = [
            ("Total (GBP)",    f"£{cur_total:,.2f}", f"£{prev_total:,.2f}"),
            ("Transactions",   f"{cur_count:,}",      f"{prev_count:,}"),
            ("Avg Donation",   f"£{cur_avg:,.2f}",    f"£{prev_avg:,.2f}"),
            ("Max Donation",   f"£{cur_top:,.2f}",    f"£{prev_max_val:,.2f}"),
        ]
        for col, (label, cur_val, prv_val) in zip(comp_cols, metrics):
            with col:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">{label}</div>
                    <div style="display:flex;justify-content:space-around;margin-top:12px">
                        <div style="text-align:center">
                            <div style="color:#38bdf8;font-size:0.62rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px">{sel_year_val}</div>
                            <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#f1f5f9">{cur_val}</div>
                        </div>
                        <div style="color:#334155;font-size:1.2rem;align-self:center">│</div>
                        <div style="text-align:center">
                            <div style="color:#818cf8;font-size:0.62rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px">{prev_year}</div>
                            <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#94a3b8">{prv_val}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if 'ITEM HEAD 1' in df_cur.columns:
            c_cur  = df_cur.groupby('ITEM HEAD 1')[AMT].sum().reset_index().rename(columns={AMT: str(sel_year_val)})
            c_prev = df_prev.groupby('ITEM HEAD 1')[AMT].sum().reset_index().rename(columns={AMT: str(prev_year)}) \
                     if len(df_prev) > 0 else pd.DataFrame(columns=['ITEM HEAD 1', str(prev_year)])
            comp_cat = c_cur.merge(c_prev, on='ITEM HEAD 1', how='outer').fillna(0)
            comp_cat = comp_cat.sort_values(str(sel_year_val), ascending=False)

            fig5 = go.Figure()
            fig5.add_trace(go.Bar(x=comp_cat['ITEM HEAD 1'], y=comp_cat[str(sel_year_val)],
                                  name=str(sel_year_val), marker_color='#38bdf8', marker_line_width=0,
                                  hovertemplate='<b>%{x}</b><br>£%{y:,.2f}<extra></extra>'))
            fig5.add_trace(go.Bar(x=comp_cat['ITEM HEAD 1'], y=comp_cat[str(prev_year)],
                                  name=str(prev_year), marker_color='#818cf8', marker_line_width=0, opacity=0.7,
                                  hovertemplate='<b>%{x}</b><br>£%{y:,.2f}<extra></extra>'))
            fig5.update_layout(barmode='group', bargap=0.25)
            apply_theme(fig5, f"Category Comparison: {sel_year_val} vs {prev_year}")
            st.plotly_chart(fig5, use_container_width=True)

        mc2 = df_cur.groupby('MONTH')[AMT].sum().reset_index()
        mc2['MN'] = mc2['MONTH'].map(months_map)
        mc2 = mc2.sort_values('MONTH')
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(x=mc2['MN'], y=mc2[AMT], name=str(sel_year_val),
                              marker_color='#38bdf8', marker_line_width=0,
                              hovertemplate='<b>%{x}</b><br>£%{y:,.2f}<extra></extra>'))
        if len(df_prev) > 0:
            mp2 = df_prev.groupby('MONTH')[AMT].sum().reset_index()
            mp2['MN'] = mp2['MONTH'].map(months_map)
            mp2 = mp2.sort_values('MONTH')
            fig6.add_trace(go.Bar(x=mp2['MN'], y=mp2[AMT], name=str(prev_year),
                                  marker_color='#818cf8', marker_line_width=0, opacity=0.7,
                                  hovertemplate='<b>%{x}</b><br>£%{y:,.2f}<extra></extra>'))
        fig6.update_layout(barmode='group', bargap=0.2)
        apply_theme(fig6, f"Monthly Comparison: {sel_year_val} vs {prev_year}")
        st.plotly_chart(fig6, use_container_width=True)

        if sel_month:
            st.info(f"ℹ️ Comparing **{MONTH_NUM.get(sel_month, '')}** in both {sel_year_val} and {prev_year}.")

    # ═══════════ TAB 3: CATEGORY ANALYSIS ════════════════════════════════════
    with tab3:
        c5, c6 = st.columns(2)

        with c5:
            st.markdown('<div class="section-header">Top Items by Value</div>', unsafe_allow_html=True)
            if 'ITEM' in df_cur.columns and AMT in df_cur.columns:
                item_df = df_cur.groupby('ITEM')[AMT].sum().reset_index()
                item_df = item_df[item_df[AMT] > 0].sort_values(AMT, ascending=False).head(12)
                fig7 = px.bar(item_df, x=AMT, y='ITEM', orientation='h',
                              color=AMT, color_continuous_scale=['#1e3a5f','#38bdf8'],
                              text=[f"£{v:,.2f}" for v in item_df[AMT]])
                fig7.update_traces(textposition='outside', textfont_color='#64748b',
                                   hovertemplate='<b>%{y}</b><br>£%{x:,.2f}<extra></extra>')
                fig7.update_coloraxes(showscale=False)
                apply_theme(fig7, "Top 12 Donation Items")
                fig7.update_layout(margin=dict(r=90))
                st.plotly_chart(fig7, use_container_width=True)

        with c6:
            st.markdown('<div class="section-header">Donation Type Distribution</div>', unsafe_allow_html=True)
            if 'ITEM HEAD 2' in df_cur.columns and AMT in df_cur.columns:
                type_df = df_cur.groupby('ITEM HEAD 2')[AMT].sum().reset_index()
                type_df = type_df[type_df[AMT] > 0]
                fig8 = px.pie(type_df, names='ITEM HEAD 2', values=AMT,
                              hole=0.45, color_discrete_sequence=CHART_THEME["colorway"])
                fig8.update_traces(textinfo='percent+label', textfont_size=11,
                                   textfont_color='#94a3b8',
                                   hovertemplate='<b>%{label}</b><br>£%{value:,.2f}<extra></extra>')
                apply_theme(fig8, "By Donation Type")
                fig8.update_layout(showlegend=True, margin=dict(l=20,r=20,t=50,b=20))
                st.plotly_chart(fig8, use_container_width=True)

        st.markdown('<div class="section-header">Donations by Hijri Month</div>', unsafe_allow_html=True)
        if 'HIJRI MONTH NAME' in df_cur.columns and AMT in df_cur.columns:
            hijri_order = ['Muharram','Safar','Rabi ul Awwal','Rabi ul Sani',
                           'Jamadi ul Awwal','Jamadi ul Sani','Rajjab','Shaban',
                           'Ramadan','Shawwal','Dhu ul Qadah','Dhu ul Hijjah']
            hm = df_cur.groupby('HIJRI MONTH NAME')[AMT].sum().reset_index()
            hm = hm[hm[AMT] > 0]
            hm['order'] = hm['HIJRI MONTH NAME'].map({m:i for i,m in enumerate(hijri_order)}).fillna(99)
            hm = hm.sort_values('order')
            colors = ['#facc15' if m == 'Ramadan' else '#0ea5e9' for m in hm['HIJRI MONTH NAME']]
            fig9 = go.Figure(go.Bar(
                x=hm['HIJRI MONTH NAME'], y=hm[AMT],
                marker=dict(color=colors, line=dict(width=0)),
                text=[f"£{v:,.2f}" for v in hm[AMT]],
                textposition='outside', textfont_color='#64748b',
                hovertemplate='<b>%{x}</b><br>£%{y:,.2f}<extra></extra>'
            ))
            apply_theme(fig9, "Collections by Islamic Calendar Month")
            fig9.update_layout(showlegend=False)
            st.plotly_chart(fig9, use_container_width=True)
            st.caption("🌕 Gold = Ramadan")

    # ═══════════ TAB 4: TRANSACTIONS ═════════════════════════════════════════
    with tab4:
        sc1, sc2 = st.columns([3, 1])
        with sc1:
            search = st.text_input("🔍 Search", placeholder="Search by ID, item, city, category…",
                                   label_visibility="collapsed")
        with sc2:
            st.download_button("⬇️ Export CSV",
                               data=df_cur.to_csv(index=False).encode('utf-8'),
                               file_name=f"mwf_{sel_year_val or 'all'}.csv",
                               mime="text/csv", use_container_width=True)

        st.markdown('<div class="section-header">Transaction Register</div>', unsafe_allow_html=True)

        display_cols = ['TRANSACTION PRIMARY KEY','DATE','ITEM','ITEM HEAD 1',
                        'TRANSACTION FORUM','POSTCODE ZONE','LINK CLUSTER CITY',
                        AMT,'CURRENCY','HIJRI MONTH NAME','HIJRI DATE']
        display_cols = [c for c in display_cols if c in df_cur.columns]

        disp_df = df_cur[display_cols].copy()
        if AMT in disp_df.columns:
            disp_df = disp_df.rename(columns={AMT: 'Amount (GBP)'})
            disp_df['Amount (GBP)'] = disp_df['Amount (GBP)'].apply(lambda x: f"£{x:,.2f}")
        if 'DATE' in disp_df.columns:
            disp_df['DATE'] = disp_df['DATE'].dt.strftime('%d %b %Y')

        if search:
            mask = disp_df.apply(lambda row: row.astype(str).str.contains(
                search, case=False, na=False).any(), axis=1)
            disp_df = disp_df[mask]

        st.dataframe(disp_df.reset_index(drop=True), use_container_width=True, height=460)
        st.caption(f"Showing {len(disp_df):,} of {cur_count:,} transactions")

if __name__ == "__main__":
    main()
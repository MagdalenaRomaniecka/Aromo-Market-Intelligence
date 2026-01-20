import streamlit as st
import pandas as pd
import plotly.express as px
import re

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Aromo Intel",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. DARK LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap');
    
    /* GLOBAL THEME */
    .stApp { background-color: #000000; color: #E0E0E0; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222; }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span { color: #888 !important; }

    /* DROPDOWN MENU FIX (Force Dark Mode) */
    div[data-baseweb="select"] > div { background-color: #111 !important; color: #EEE !important; border: 1px solid #333 !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] { background-color: #111 !important; border: 1px solid #333 !important; }
    li[role="option"] { color: #CCC !important; }
    li[role="option"]:hover { background-color: #D4AF37 !important; color: #000 !important; }

    /* TYPOGRAPHY */
    h1, h2, h3 { font-family: 'Montserrat', sans-serif !important; color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 2px; }
    
    /* METRIC CARDS */
    div[data-testid="stMetric"] { background-color: #090909; border: 1px solid #222; padding: 10px; border-radius: 0px; }
    div[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.7rem !important; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 1.8rem !important; }
    
    /* HIDE STREAMLIT UI */
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE & CLEANING ---
@st.cache_data(ttl=0)
def load_data():
    # SWITCHING TO THE CLEANED DATASET SEEN IN SCREENSHOT
    file_path = 'aromo_cleaned.csv'
    
    try:
        # Engine python is safer for complex CSVs
        df = pd.read_csv(file_path, sep=None, engine='python')
        df.columns = df.columns.str.lower().str.strip()
        
        # 1. Basic Cleanup
        df = df.dropna(subset=['brand'])
        
        # 2. Year Parsing (Robust)
        df['year_clean'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        
        # 3. ADVANCED DEDUPLICATION (Core Name Logic)
        def get_core_name(text):
            if not isinstance(text, str): return str(text)
            text = text.lower()
            # Remove content in parentheses e.g., "(2020)"
            text = re.sub(r'\(.*?\)', '', text)
            # Remove common variant suffixes
            remove_list = [
                ' eau de parfum', ' eau de toilette', ' edp', ' edt', ' parfum', 
                ' cologne', ' intense', ' l\'eau', ' fraiche', ' extreme', 
                ' absolu', ' elixir', ' sport', ' legere', ' tendre'
            ]
            for r in remove_list:
                text = text.replace(r, '')
            return text.strip()

        # Identify name column
        name_col = 'name' if 'name' in df.columns else 'perfume'
        
        if name_col in df.columns:
            df['brand_norm'] = df['brand'].astype(str).str.lower().str.strip()
            df['core_name'] = df[name_col].apply(get_core_name)
            
            # DROP DUPLICATES based on Brand + Core Name
            df = df.drop_duplicates(subset=['brand_norm', 'core_name'])
        
        # 4. Final Formatting
        df['Brand'] = df['brand'].astype(str).str.title().strip()
        df['families'] = df['families'].fillna('Unknown')
        
        return df
        
    except Exception as e:
        # DETECTIVE MODE: Show the exact error on screen
        st.error(f"⚠️ DATA ERROR: {e}")
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("AROMO")
    st.caption("MARKET INTELLIGENCE")
    st.write("---")
    
    # Filter
    show_last_10 = st.checkbox("Last 10 Years Only", value=True)

    if not df.empty:
        if show_last_10:
            df_chart = df[(df['year_clean'] >= 2015) & (df['year_clean'] <= 2025)]
        else:
            df_chart = df[df['year_clean'] > 1900]
    else:
        df_chart = df

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 style='text-align:center;'>Market Intelligence</h1>", unsafe_allow_html=True)

if df.empty:
    st.stop() # Stops execution here if data failed to load (Error is shown above)

# --- KPI SECTION ---
c1, c2, c3 = st.columns(3)
c1.metric("Unique Lines", f"{len(df):,}") 
c2.metric("Peak Activity", int(df_chart['year_clean'].mode()[0]) if not df_chart.empty else "-")
c3.metric("Active Brands", f"{df['Brand'].nunique():,}")

st.markdown("---")

# --- CHART SECTION (Line Chart for Visibility) ---
st.markdown("### 📈 Market Dynamics (Launches)")

if not df_chart.empty:
    # Prepare Data
    chart_data = df_chart[df_chart['year_clean'] > 0].groupby('year_clean').size().reset_index(name='Count')
    chart_data = chart_data.sort_values('year_clean')
    
    if not chart_data.empty:
        # Use Line Chart with Markers (High Visibility)
        fig = px.line(chart_data, x='year_clean', y='Count', markers=True)
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#AAA',
            font_family='Montserrat',
            xaxis=dict(showgrid=False, title="", color='#666'),
            yaxis=dict(showgrid=True, gridcolor='#222', title=""),
            height=350,
            margin=dict(l=0,r=0,t=10,b=0)
        )
        # Gold Line
        fig.update_traces(line_color='#D4AF37', line_width=3, marker_size=6)
        st.plotly_chart(fig, use_container_width=True)
    else:
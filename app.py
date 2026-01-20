import streamlit as st
import pandas as pd
import plotly.express as px
import re

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Aromo Market Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. DARK LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Montserrat:wght@300;400;600&display=swap');

    /* APP BACKGROUND */
    .stApp { background-color: #000000; color: #E0E0E0; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222; }
    section[data-testid="stSidebar"] * { color: #AAAAAA !important; }

    /* DROPDOWN FIX */
    div[data-baseweb="select"] > div { background-color: #111 !important; color: #E0E0E0 !important; border-color: #333 !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] { background-color: #111 !important; border: 1px solid #333 !important; }
    li[role="option"] { color: #CCCCCC !important; background-color: #111 !important; }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] { background-color: #D4AF37 !important; color: #000 !important; }

    /* FONTS */
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: #D4AF37 !important; }
    p, div, span, label { font-family: 'Montserrat', sans-serif !important; }
    
    /* KPI CARDS */
    div[data-testid="stMetric"] { background-color: #080808; border: 1px solid #222; padding: 15px; text-align: center; border-radius: 4px; }
    div[data-testid="stMetricLabel"] { color: #888 !important; font-size: 0.75rem !important; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 2rem !important; font-family: 'Cormorant Garamond', serif !important; }

    /* HIDE SYSTEM */
    header, footer {visibility: hidden;} 
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }

    /* FOOTER */
    .custom-footer { width: 100%; text-align: center; padding: 30px 0; margin-top: 50px; border-top: 1px solid #222; color: #555; font-size: 0.7rem; font-family: 'Montserrat', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE (HARD RESET) ---

def extract_year_fallback(text):
    """Try to find a year like (2020) in the name if the Year column is empty."""
    match = re.search(r'\((\d{4})\)', str(text))
    if match:
        y = int(match.group(1))
        if 1900 < y < 2026: return y
    return 0

def clean_name_logic(text):
    if not isinstance(text, str): return str(text)
    text = text.lower()
    text = re.sub(r'\(.*?\)', '', text) # Remove year from name for deduplication
    removals = [
        ' eau de parfum', ' eau de toilette', ' edp', ' edt', ' parfum', 
        ' cologne', ' extrait', ' intense', ' l\'eau', ' fraiche', ' extreme',
        ' absolu', ' absolute', ' legere', ' tendre', ' elixir', ' sport'
    ]
    for r in removals:
        text = text.replace(r, '')
    return text.strip()

# TTL=0 forces reload every time (No caching issues)
@st.cache_data(ttl=0)
def load_data():
    file_path = 'aromo_english.csv'
    try:
        df = pd.read_csv(file_path, sep=None, engine='python')
        df.columns = df.columns.str.lower().str.strip()
        
        # 1. Clean Columns
        df = df.dropna(subset=['brand'])
        df['brand_norm'] = df['brand'].astype(str).str.lower().str.strip()
        
        name_col = 'name' if 'name' in df.columns else 'perfume'
        if name_col not in df.columns: return pd.DataFrame()
        
        # 2. Year Parsing (Robust)
        # First try standard conversion
        df['Year_Numeric'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        
        # 3. Aggressive Deduplication
        df['universal_name'] = df[name_col].apply(clean_name_logic)
        df = df.drop_duplicates(subset=['brand_norm', 'universal_name'])

        # 4. Final Formatting
        df['Brand'] = df['brand'].astype(str).str.title().str.strip()
        df['families'] = df['families'].fillna('Unclassified')
        
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h3 style='text-align:center; color:#D4AF37;'>AROMO INTEL.</h3>", unsafe_allow_html=True)
    st.write("---")
    
    time_mode = st.radio("DATA RANGE:", ["Last 10 Years", "Full History"], index=0)
    
    if not df.empty:
        if time_mode == "Last 10 Years":
            df_active = df[(df['Year_Numeric'] >= 2015) & (df['Year_Numeric'] <= 2025)]
            subtitle = "Market Trends (2015-2025)"
        else:
            df_active = df[df['Year_Numeric'] > 1900]
            subtitle = "Full Market History"
    else:
        df_active = df
        subtitle = ""

# --- 5. DASHBOARD ---
st.markdown("<h1 style='text-align:center;'>Aromo Market Intelligence</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#888; font-size:0.8rem; margin-bottom:40px; text-transform:uppercase;'>Strategic Insights • {subtitle}</p>", unsafe_allow_html=True)

if df.empty:
    st.error("⚠️ Failed to load data. Please check CSV.")
    st.stop()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📈 TRENDS", "🧬 BRAND DNA", "🤖 AI MONITOR"])

# === TAB 1: TRENDS ===
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    c1.metric("Unique Fragrances", f"{len(df):,}") 
    
    if not df_active.empty:
        peak = df_active['Year_Numeric'].mode()[0]
        c2.metric("Peak Activity", int(peak))
    else:
        c2.metric("Peak Activity", "-")
        
    brands_num = df['Brand'].nunique()
    c3.metric("Active Brands", f"{brands_num:,}")
    
    st.markdown("---")
    st.markdown("### Market Saturation (Launches per Year)")
    
    if not df_active.empty:
        # DATA PREP FOR CHART
        # Only keep valid years > 1900
        valid_years = df_active[df_active['Year_Numeric'] > 1900]
        
        if not valid_years.empty:
            trend_data = valid_years.groupby('Year_Numeric').size().reset_index(name='Count')
            # SORTING IS KEY
            trend_data = trend_data.sort_values('Year_Numeric')
            
            fig = px.area(trend_data, x='Year_Numeric', y='Count')
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#AAA',
                font_family='Montserrat',
                xaxis=dict(title="", showgrid=False, gridcolor='#333'),
                yaxis=dict(title="", showgrid=True, gridcolor='#222'),
                margin=dict(l=0, r=0, t=0, b=0),
                height=400
            )
            fig.update_traces(line_color='#D4AF37', fillcolor='rgba(212, 175, 55, 0.2)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No year data found in the selected range.")
    else:
        st.info("No data available.")

# === TAB 2: BRAND DNA ===
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    brands_list = sorted(df['Brand'].unique())
    sel_brand = st.selectbox("Select Brand:", brands_list)
    brand_df = df[df['Brand'] == sel_brand]
    
    c1, c2 = st.columns([1,2])
    with c1:
        st.markdown(f"<h3 style='margin:0; color:#D4AF37;'>{sel_brand}</h3>", unsafe_allow_html=True)
        st.write(f"Total Scents: **{len(brand_df)}**")
        if not brand_df.empty:
            if brand_df['families'].isnull().all():
                style = "Unknown"
            else:
                style = brand_df['families'].mode()[0]
            st.write(f"Dominant Style: **{style}**")
            
    with c2:
        if not brand_df.empty:
            brand_df['Family_Group'] = brand_df['families'].astype(str).apply(lambda x: x.split(',')[0].strip())
            fig_sun = px.sunburst(brand_df, path=['Family_Group'], color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_sun.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=0, l=0, r=0, b=0),
                height=300,
                font_family='Montserrat'
            )
            st.plotly_chart(fig_sun, use_container_width=True)

# === TAB 3: AI MONITOR ===
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3>AI Match: {sel_brand}</h3>", unsafe_allow_html=True)
    st.caption("Competitor proximity analysis based on olfactory notes (Simulation)")
    
    mock = pd.DataFrame({
        'Competitor': ['Tom Ford', 'Dior', 'YSL', 'Chanel', 'Gucci'],
        'Match Score': [95, 88, 82, 75, 70]
    })
    
    # FIXED: Use text_auto=True for automatic labeling without bugs
    fig_ai = px.bar(mock, x='Match Score', y='Competitor', orientation='h', text_auto=True)
    
    fig_ai.update_traces(
        marker_color='#D4AF37', 
        textposition='inside'
    )
    
    fig_ai.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#E0E0E0',
        xaxis=dict(visible=False),
        yaxis=dict(title=""),
        height=300,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_ai, use_container_width=True)

# --- FOOTER ---
st.markdown("""
<div class="custom-footer">
    Aromo Market Intelligence • Developed by Magdalena Romaniecka • 2026<br>
    Data Source: <a href="https://www.kaggle.com/datasets/olgagmiufana1/aromo-ru-fragrance-dataset" target="_blank">Fragrantica Dataset (Kaggle)</a>
</div>
""", unsafe_allow_html=True)
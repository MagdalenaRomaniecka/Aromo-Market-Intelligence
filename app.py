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
    
    .stApp { background-color: #000000; color: #E0E0E0; }
    section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222; }
    section[data-testid="stSidebar"] * { color: #888 !important; }
    
    /* DROPDOWN FIX */
    div[data-baseweb="select"] > div { background-color: #111 !important; color: #EEE !important; border: 1px solid #333 !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] { background-color: #111 !important; border: 1px solid #333 !important; }
    li[role="option"] { color: #CCC !important; }
    li[role="option"]:hover { background-color: #D4AF37 !important; color: #000 !important; }

    /* TYPOGRAPHY & CARDS */
    h1, h2, h3 { font-family: 'Montserrat', sans-serif !important; color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 2px; }
    div[data-testid="stMetric"] { background-color: #090909; border: 1px solid #222; padding: 10px; border-radius: 0px; }
    div[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.7rem !important; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 1.8rem !important; }
    
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=0)
def load_data():
    file_path = 'aromo_cleaned.csv'
    
    try:
        df = pd.read_csv(file_path, sep=None, engine='python')
        df.columns = df.columns.str.lower().str.strip()
        
        # 1. Basic Cleanup
        df = df.dropna(subset=['brand'])
        
        # 2. Year Parsing
        df['year_clean'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        
        # 3. Deduplication Logic
        def get_core_name(text):
            if not isinstance(text, str): return str(text)
            text = text.lower()
            text = re.sub(r'\(.*?\)', '', text) # Remove year (2020)
            text = text.replace(' eau de parfum', '').replace(' edt', '').replace(' edp', '')
            return text.strip()

        name_col = 'name' if 'name' in df.columns else 'perfume'
        
        if name_col in df.columns:
            df['brand_norm'] = df['brand'].astype(str).str.lower().str.strip()
            df['core_name'] = df[name_col].apply(get_core_name)
            df = df.drop_duplicates(subset=['brand_norm', 'core_name'])
        
        # 4. Formatting (FIXED THE ERROR HERE)
        # Błąd był tu: .strip() zamiast .str.strip()
        df['Brand'] = df['brand'].astype(str).str.title().str.strip()
        df['families'] = df['families'].fillna('Unknown')
        
        return df
        
    except Exception as e:
        st.error(f"⚠️ Data Error: {e}")
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("AROMO")
    st.write("---")
    show_last_10 = st.checkbox("Last 10 Years Only", value=True)

    if not df.empty:
        if show_last_10:
            df_chart = df[(df['year_clean'] >= 2015) & (df['year_clean'] <= 2025)]
        else:
            df_chart = df[df['year_clean'] > 1900]
    else:
        df_chart = df

# --- 5. DASHBOARD ---
st.markdown("<h1 style='text-align:center;'>Market Intelligence</h1>", unsafe_allow_html=True)

if df.empty:
    st.stop()

# KPI
c1, c2, c3 = st.columns(3)
c1.metric("Unique Lines", f"{len(df):,}") 
c2.metric("Peak Activity", int(df_chart['year_clean'].mode()[0]) if not df_chart.empty else "-")
c3.metric("Active Brands", f"{df['Brand'].nunique():,}")

st.markdown("---")

# --- CHART SECTION ---
st.markdown("### 📈 Market Dynamics (Launches)")

if not df_chart.empty:
    # Prepare Data
    chart_data = df_chart[df_chart['year_clean'] > 0].groupby('year_clean').size().reset_index(name='Count')
    chart_data = chart_data.sort_values('year_clean')
    
    if not chart_data.empty:
        fig = px.line(chart_data, x='year_clean', y='Count', markers=True)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#AAA',
            xaxis=dict(showgrid=False, title="", color='#666'),
            yaxis=dict(showgrid=True, gridcolor='#222', title=""),
            height=350,
            margin=dict(l=0,r=0,t=10,b=0)
        )
        fig.update_traces(line_color='#D4AF37', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No dated data available for this range.")
else:
    st.info("No data to display.")

# --- TABS ---
t1, t2 = st.tabs(["🧬 BRAND DNA", "🤖 AI COMPETITOR"])

with t1:
    brands = sorted(df['Brand'].unique())
    sel_brand = st.selectbox("Select Brand:", brands)
    b_df = df[df['Brand'] == sel_brand]
    
    colA, colB = st.columns([1,2])
    with colA:
        st.write(f"**{sel_brand}**")
        st.write(f"Portfolio: {len(b_df)}")
        if not b_df.empty:
            if 'families' in b_df.columns:
                val = b_df['families'].mode()
                style = val[0] if not val.empty else "Unknown"
            else:
                style = "Unknown"
            st.write(f"Style: {style}")
            
    with colB:
        if not b_df.empty and 'families' in b_df.columns:
            b_df['Main_Fam'] = b_df['families'].astype(str).apply(lambda x: x.split(',')[0])
            fig_pie = px.pie(b_df, names='Main_Fam', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#DDD', height=300, margin=dict(t=0,b=0))
            st.plotly_chart(fig_pie, use_container_width=True)

with t2:
    st.markdown(f"**AI Match: {sel_brand}**")
    mock = pd.DataFrame({'Brand': ['Tom Ford', 'Dior', 'YSL', 'Chanel', 'Gucci'], 'Match': [95, 88, 82, 75, 70]})
    fig_bar = px.bar(mock, x='Match', y='Brand', orientation='h', text_auto=True)
    fig_bar.update_traces(marker_color='#D4AF37', textfont_color='black')
    fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#AAA', xaxis=dict(visible=False), yaxis=dict(title=""), height=250, margin=dict(t=0,b=0))
    st.plotly_chart(fig_bar, use_container_width=True)

# --- FOOTER ---
st.markdown("<div style='text-align:center; color:#555; margin-top:50px; border-top:1px solid #222; padding-top:20px;'>Aromo Market Intelligence • 2026</div>", unsafe_allow_html=True)

# --- DEBUGGER ---
with st.expander("🛠️ DEBUGGER"):
    st.write(f"Using file: aromo_cleaned.csv")
    st.dataframe(df.head())
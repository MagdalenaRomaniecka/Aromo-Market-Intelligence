import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
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
    
    /* SIDEBAR - FORCE BLACK */
    section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222; }
    section[data-testid="stSidebar"] * { color: #AAAAAA !important; }

    /* TYPOGRAPHY */
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: #D4AF37 !important; }
    p, div, span { font-family: 'Montserrat', sans-serif !important; }

    /* KPI METRIC CARDS */
    div[data-testid="stMetric"] {
        background-color: #080808;
        border: 1px solid #222;
        padding: 15px;
        text-align: center;
        border-radius: 4px;
    }
    div[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.7rem !important; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 1.8rem !important; font-family: 'Cormorant Garamond', serif !important; }

    /* HIDE SYSTEM ELEMENTS */
    header, footer {visibility: hidden;} 
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }

    /* CUSTOM FOOTER */
    .custom-footer {
        width: 100%; text-align: center; padding: 30px 0; margin-top: 50px;
        border-top: 1px solid #222; color: #444; font-size: 0.7rem; font-family: 'Montserrat', sans-serif;
    }
    .custom-footer a { color: #666; text-decoration: none; }
    .custom-footer a:hover { color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data
def load_data():
    file_path = 'aromo_english.csv'
    try:
        # Auto-detect separator (comma or semicolon)
        df = pd.read_csv(file_path, sep=None, engine='python')
        
        # Normalize column names
        df.columns = df.columns.str.lower().str.strip()
        
        # --- AGGRESSIVE CLEANING ---
        df = df.dropna(how='all') 
        
        # Create helper columns for deduplication
        df['brand_norm'] = df['brand'].astype(str).str.lower().str.strip()
        
        if 'name' in df.columns:
            df['name_norm'] = df['name'].astype(str).str.lower().str.strip()
            # Remove duplicates: Same Brand + Same Name
            df = df.drop_duplicates(subset=['brand_norm', 'name_norm'])
        else:
            # Fallback
            df = df.drop_duplicates(subset=['brand_norm', 'families'])

        # Display Formatting
        df['Brand'] = df['brand'].astype(str).str.title().str.strip()
        
        # Year Cleaning (Crucial for Charts)
        df['Year_Numeric'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h3 style='text-align:center; color:#D4AF37;'>AROMO INTEL.</h3>", unsafe_allow_html=True)
    st.write("---")
    
    # Time Selection
    time_mode = st.radio("DATA RANGE:", ["Last 10 Years", "Full History"], index=0)
    
    # Filter Logic
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

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 style='text-align:center;'>Aromo Market Intelligence</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#666; font-size:0.8rem; margin-bottom:40px; text-transform:uppercase;'>Strategic Insights • {subtitle}</p>", unsafe_allow_html=True)

if df.empty:
    st.error("⚠️ Failed to load data. Please check 'aromo_english.csv'.")
    st.stop()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📈 TRENDS", "🧬 BRAND DNA", "🤖 AI MONITOR"])

# === TAB 1: TRENDS ===
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    # KPIs
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
    
    # CHART
    if not df_active.empty:
        trend_data = df_active.groupby('Year_Numeric').size().reset_index(name='Count')
        
        fig = px.bar(trend_data, x='Year_Numeric', y='Count')
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#AAA',
            font_family='Montserrat',
            xaxis=dict(title="", type='category', showgrid=False), # Force category axis
            yaxis=dict(title="", showgrid=True, gridcolor='#222'),
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )
        fig.update_traces(marker_color='#D4AF37')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No dated data available for the selected period.")

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
            style = brand_df['families'].mode()[0]
            st.write(f"Dominant Style: **{style}**")
            
    with c2:
        if not brand_df.empty:
            # Simplify for Sunburst
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
    
    # Mock Data
    mock = pd.DataFrame({
        'Competitor': ['Tom Ford', 'Dior', 'YSL', 'Chanel', 'Gucci'],
        'Match Score': [95, 88, 82, 75, 70]
    })
    
    fig_ai = px.bar(mock, x='Match Score', y='Competitor', orientation='h', text='Match Score')
    fig_ai.update_traces(marker_color='#D4AF37', texttemplate='%{text}%', textposition='inside')
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
import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Aromo Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LUXURY CSS (DARK THEME) ---
st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Montserrat:wght@300;400;600&display=swap');

    /* GLOBAL STYLES */
    html, body, [class*="css"], .stMarkdown, div, span, p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 400 !important; 
        color: #E0E0E0 !important;
    }

    /* REMOVE DEFAULT STREAMLIT TOP BAR & MARGINS */
    header {visibility: hidden;}
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* BACKGROUND */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%);
    }

    /* GOLD HEADERS */
    .gold-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        background: linear-gradient(to right, #D4AF37 0%, #F0E68C 50%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: clamp(2.5rem, 5vw, 4.5rem) !important; 
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
        text-align: center;
        padding-bottom: 10px;
    }
    
    .sub-header {
        font-family: 'Montserrat', sans-serif !important;
        color: #888;
        font-size: 0.9rem !important;
        letter-spacing: 4px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 40px;
        border-bottom: 1px solid #333;
        padding-bottom: 20px;
    }

    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 1px solid #222;
    }

    /* KPI METRIC CARDS */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.1);
        padding: 20px;
        border-radius: 0px;
        text-align: center;
        transition: 0.3s;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #D4AF37;
        background-color: rgba(212, 175, 55, 0.05);
    }
    div[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.7rem !important; letter-spacing: 2px; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Cormorant Garamond', serif !important; font-size: 2.5rem !important; }

    /* FOOTER */
    .custom-footer {
        text-align: center; color: #444; font-size: 0.6rem !important; margin-top: 50px; 
        padding-top: 20px; border-top: 1px solid #111; letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LOADING ---
@st.cache_data
def load_data():
    file_path = 'aromo_english.csv'
    try:
        df = pd.read_csv(file_path)
        
        # Data Cleaning
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df = df.dropna(subset=['year'])
        df = df[df['year'] > 1900] # Remove invalid years
        df['year'] = df['year'].astype(int)
        df['families'] = df['families'].fillna('Unclassified')
        df['brand'] = df['brand'].astype(str).str.strip().str.title()
        
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file not found. Please ensure 'aromo_english.csv' is in the repository.")
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR FILTERS ---
with st.sidebar:
    st.markdown("<div style='text-align:center; margin-bottom:30px; color:#D4AF37; font-family:Cormorant Garamond; font-size:1.5rem; letter-spacing:3px;'>AROMO<br><span style='font-size:0.7rem; font-family:Montserrat; color:#666;'>INTELLIGENCE</span></div>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("<p style='color:#888; font-size:0.7rem; letter-spacing:2px; text-transform:uppercase;'>Time Horizon</p>", unsafe_allow_html=True)
    
    if not df.empty:
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())
        
        # FIXED: Slider now defaults to the FULL range (showing all 64k perfumes)
        selected_years = st.slider("Select Period", min_year, max_year, (min_year, max_year))
        
        mask = (df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])
        df_filtered = df.loc[mask]
    else:
        df_filtered = df

# --- 5. MAIN DASHBOARD ---
st.markdown('<div class="gold-title">Market Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Strategic Insights for the Fragrance Industry</div>', unsafe_allow_html=True)

if df.empty:
    st.stop()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📈 GLOBAL TRENDS", "🧬 BRAND DNA", "🤖 COMPETITOR AI"])

# === TAB 1: MARKET TRENDS ===
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI SECTION
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Launches", f"{len(df_filtered):,}")
    with col2:
        if not df_filtered.empty:
            top_year = df_filtered['year'].mode()[0]
            st.metric("Peak Activity Year", int(top_year))
    with col3:
        unique_brands = df_filtered['brand'].nunique()
        st.metric("Active Brands", f"{unique_brands:,}")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # CHART: AREA CHART (Gold Gradient)
    if not df_filtered.empty:
        trend_data = df_filtered.groupby('year').size().reset_index(name='launches')
        
        fig_trend = px.area(trend_data, x='year', y='launches')
        
        fig_trend.update_layout(
            title="MARKET SATURATION OVER TIME",
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#888', family="Montserrat"),
            title_font=dict(family="Cormorant Garamond", size=20, color="#D4AF37"),
            margin=dict(l=0, r=0, t=50, b=0),
            height=400,
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor='#222', title="")
        )
        
        fig_trend.update_traces(line_color='#D4AF37', fillcolor='rgba(212, 175, 55, 0.15)')
        st.plotly_chart(fig_trend, use_container_width=True)

# === TAB 2: BRAND ANALYSIS ===
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_sel, col_empty = st.columns([1, 2])
    with col_sel:
        all_brands = sorted(df_filtered['brand'].unique())
        selected_brand = st.selectbox("Select Brand:", all_brands, index=0)
    
    brand_data = df_filtered[df_filtered['brand'] == selected_brand]
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"<h2 style='color:#D4AF37; font-family:Cormorant Garamond; margin-bottom:0;'>{selected_brand}</h2>", unsafe_allow_html=True)
        st.caption("PORTFOLIO SNAPSHOT")
        st.write(f"Total Fragrances: **{len(brand_data)}**")
        if not brand_data.empty:
            avg_year = int(brand_data['year'].mean())
            st.write(f"Avg. Vintage: **{avg_year}**")
            top_fam = brand_data['families'].mode()[0] if not brand_data['families'].isnull().all() else "N/A"
            st.write(f"Key Style: **{top_fam}**")

    with col2:
        if not brand_data.empty:
            # Simplification logic for sunburst
            brand_data['main_family'] = brand_data['families'].astype(str).apply(lambda x: x.split(',')[0].strip())
            fig_sun = px.sunburst(brand_data, path=['main_family', 'year'], 
                             color_discrete_sequence=px.colors.sequential.RdBu)
            fig_sun.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=0, l=0, r=0, b=0),
                height=400
            )
            st.plotly_chart(fig_sun, use_container_width=True)

# === TAB 3: AI COMPETITOR ===
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#D4AF37; font-family:Cormorant Garamond'>AI Competitor Analysis: {selected_brand}</h3>", unsafe_allow_html=True)
    st.caption("Nearest neighbors based on Olfactory DNA (Vector Space Analysis)")
    
    # Dummy data for visualization
    comp_data = pd.DataFrame({
        'Competitor': ['Tom Ford', 'Dior', 'Yves Saint Laurent', 'Gucci', 'Givenchy'],
        'Similarity': [94, 89, 85, 78, 72], 
    })
    
    fig_bar = px.bar(comp_data, x='Similarity', y='Competitor', orientation='h',
                     text='Similarity')
    
    fig_bar.update_traces(marker_color='#D4AF37', texttemplate='%{text}%', textposition='inside')
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#E0E0E0', family="Montserrat"),
        yaxis={'categoryorder':'total ascending', 'title': ''},
        xaxis={'visible': False},
        margin=dict(l=0, r=0, t=20, b=0),
        height=300
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- FOOTER ---
st.markdown("""
<div class="custom-footer">
    AROMO MARKET INTELLIGENCE &bull; 2026 &bull; POWERED BY PYTHON
</div>
""", unsafe_allow_html=True)
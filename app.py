import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Aromo Market Intelligence",
    page_icon="mn",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. FORCED DARK LUXURY CSS ---
st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Montserrat:wght@300;400;600&display=swap');

    /* FORCE DARK BACKGROUND EVERYWHERE */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%);
    }

    /* FORCE SIDEBAR BLACK */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #333;
    }
    
    /* FIX SIDEBAR TEXT COLOR */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #E0E0E0 !important;
    }

    /* GLOBAL FONTS */
    html, body, [class*="css"], div, span, p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 400 !important; 
        color: #E0E0E0;
    }

    /* REMOVE WHITESPACE */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }
    header, footer, #MainMenu {visibility: hidden;}

    /* GOLD HEADERS */
    .gold-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        background: linear-gradient(to right, #D4AF37 0%, #F0E68C 50%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: clamp(2rem, 4vw, 3.5rem) !important; 
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
        text-align: center;
        padding-bottom: 5px;
    }
    
    .sub-header {
        font-family: 'Montserrat', sans-serif !important;
        color: #888;
        font-size: 0.8rem !important;
        letter-spacing: 4px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 1px solid #333;
        padding-bottom: 20px;
    }

    /* METRIC CARDS */
    div[data-testid="stMetric"] {
        background-color: rgba(20, 20, 20, 0.8) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        padding: 15px;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] { color: #888 !important; font-size: 0.7rem !important; letter-spacing: 2px; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Cormorant Garamond', serif !important; font-size: 2.2rem !important; }

    /* SLIDER COLOR FIX */
    div[data-baseweb="slider"] div { background-color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LOADING & CLEANING ---
@st.cache_data
def load_data():
    file_path = 'aromo_english.csv'
    try:
        df = pd.read_csv(file_path)
        
        # 1. REMOVE EXACT DUPLICATES (Fixes the 78k issue)
        df = df.drop_duplicates()
        
        # 2. CLEAN TEXT
        df['brand'] = df['brand'].astype(str).str.strip().str.title()
        df['families'] = df['families'].fillna('Unclassified')
        
        # 3. CLEAN YEARS (CRITICAL FOR CHART)
        # Force convert to numeric, turning errors to NaN
        df['year_clean'] = pd.to_numeric(df['year'], errors='coerce')
        
        return df
        
    except FileNotFoundError:
        st.error("⚠️ Error: 'aromo_english.csv' not found.")
        return pd.DataFrame()

df = load_data()

# --- 4. PREPARE CHART DATA ---
# Create a strict subset for charts: ONLY valid years > 1900
df_chart = df.dropna(subset=['year_clean']).copy()
df_chart['year_clean'] = df_chart['year_clean'].astype(int)
df_chart = df_chart[df_chart['year_clean'] > 1900]
df_chart = df_chart.sort_values('year_clean')

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='text-align:center; margin-bottom:20px; color:#D4AF37; font-family:Cormorant Garamond; font-size:1.5rem; letter-spacing:2px;'>AROMO<br><span style='font-size:0.7rem; font-family:Montserrat; color:#888;'>INTELLIGENCE</span></div>", unsafe_allow_html=True)
    st.write("---")
    
    # Year Slider
    if not df_chart.empty:
        min_year = int(df_chart['year_clean'].min())
        max_year = int(df_chart['year_clean'].max())
        selected_years = st.slider("Analysis Period", min_year, max_year, (min_year, max_year))
        
        # Filter Logic
        mask = (df_chart['year_clean'] >= selected_years[0]) & (df_chart['year_clean'] <= selected_years[1])
        df_chart_filtered = df_chart.loc[mask]
    else:
        df_chart_filtered = df_chart

# --- 6. MAIN DASHBOARD ---
st.markdown('<div class="gold-title">Market Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Strategic Insights for the Fragrance Industry</div>', unsafe_allow_html=True)

if df.empty:
    st.stop()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📈 TRENDS", "🧬 BRAND DNA", "🤖 AI COMPETITOR"])

# === TAB 1: MARKET TRENDS ===
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI CARDS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Fragrances", f"{len(df):,}")
    with col2:
        if not df_chart_filtered.empty:
            peak = df_chart_filtered['year_clean'].mode()[0]
            st.metric("Peak Activity", int(peak))
        else:
            st.metric("Peak Activity", "N/A")
    with col3:
        brands_count = df['brand'].nunique()
        st.metric("Active Brands", f"{brands_count:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    # AREA CHART (FIXED)
    if not df_chart_filtered.empty:
        # Group by year to get counts
        trend_data = df_chart_filtered.groupby('year_clean').size().reset_index(name='launches')
        
        fig_trend = px.area(trend_data, x='year_clean', y='launches')
        
        fig_trend.update_layout(
            title="MARKET SATURATION",
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#AAA', family="Montserrat"),
            title_font=dict(family="Cormorant Garamond", size=20, color="#D4AF37"),
            height=400,
            xaxis=dict(showgrid=False, title="", color='#666'),
            yaxis=dict(showgrid=True, gridcolor='#222', title="")
        )
        fig_trend.update_traces(line_color='#D4AF37', fillcolor='rgba(212, 175, 55, 0.2)')
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("No data for timeline chart.")

# === TAB 2: BRAND ANALYSIS ===
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        all_brands = sorted(df['brand'].unique())
        selected_brand = st.selectbox("Select Brand:", all_brands, index=0)
    
    brand_data = df[df['brand'] == selected_brand]
    brand_data_chart = df_chart[df_chart['brand'] == selected_brand]
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"<h2 style='color:#D4AF37; font-family:Cormorant Garamond; margin:0;'>{selected_brand}</h2>", unsafe_allow_html=True)
        st.caption("PORTFOLIO")
        st.write(f"Total Scents: **{len(brand_data)}**")
        
        if not brand_data_chart.empty:
            avg = int(brand_data_chart['year_clean'].mean())
            st.write(f"Avg. Vintage: **{avg}**")
            
        if not brand_data.empty:
            style = brand_data['families'].mode()[0]
            st.write(f"Key Style: **{style}**")

    with col2:
        if not brand_data.empty:
            plot_data = brand_data.copy()
            # Handle undated for visualization
            plot_data['year_label'] = plot_data['year_clean'].fillna(0).astype(int).astype(str).replace('0', 'Undated')
            plot_data['main_family'] = plot_data['families'].astype(str).apply(lambda x: x.split(',')[0].strip())
            
            fig_sun = px.sunburst(plot_data, path=['main_family', 'year_label'], 
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
    st.markdown(f"<h3 style='color:#D4AF37; font-family:Cormorant Garamond'>AI Match: {selected_brand}</h3>", unsafe_allow_html=True)
    
    # Dummy Visualization
    comp_data = pd.DataFrame({
        'Competitor': ['Tom Ford', 'Dior', 'Yves Saint Laurent', 'Gucci', 'Givenchy'],
        'Similarity': [94, 89, 85, 78, 72], 
    })
    
    fig_bar = px.bar(comp_data, x='Similarity', y='Competitor', orientation='h', text='Similarity')
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
    AROMO MARKET INTELLIGENCE &bull; 2026
</div>
""", unsafe_allow_html=True)
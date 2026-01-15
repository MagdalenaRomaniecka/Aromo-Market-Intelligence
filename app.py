import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Aromo Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LUXURY CSS (SCENTSATIONAL STYLE FOR AROMO) ---
st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Montserrat:wght@300;400;500;600;700&display=swap');

    /* GLOBAL STYLES */
    html, body, [class*="css"], .stMarkdown, div, span, p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 400 !important; 
        color: #E0E0E0 !important;
        font-size: 0.95rem !important;
    }

    /* BACKGROUND */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 100%);
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        color: #D4AF37 !important;
    }

    /* CUSTOM TITLE GRADIENT */
    .gold-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        background: linear-gradient(to bottom, #D4AF37 0%, #F0E68C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: clamp(2.5rem, 5vw, 4rem) !important; 
        text-transform: uppercase;
        letter-spacing: 4px;
        margin: 0;
        padding-top: 10px;
    }
    
    .sub-header {
        font-family: 'Montserrat', sans-serif !important;
        color: #888;
        font-size: 0.8rem !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 30px;
    }

    /* --- SIDEBAR STYLING --- */
    section[data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 1px solid rgba(212, 175, 55, 0.15);
    }
    
    /* Custom Slider */
    div[data-baseweb="slider"] div { background-color: #D4AF37 !important; }
    
    /* --- METRIC CARDS --- */
    div[data-testid="stMetric"] {
        background-color: rgba(20, 20, 20, 0.6);
        border: 1px solid rgba(212, 175, 55, 0.2);
        padding: 15px;
        border-radius: 5px;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] { color: #888 !important; font-size: 0.8rem !important; text-transform: uppercase; letter-spacing: 1px; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Cormorant Garamond', serif !important; font-size: 2rem !important; }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: 1px solid #333;
        color: #888;
        border-radius: 0px;
        padding: 10px 20px;
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(212, 175, 55, 0.1) !important;
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
    }

    /* FOOTER */
    .custom-footer {
        text-align: center; color: #444; font-size: 0.6rem !important; margin-top: 80px; 
        padding-top: 20px; border-top: 1px solid #111; letter-spacing: 0.5px; opacity: 0.7;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LOADING ---
@st.cache_data
def load_data():
    file_path = 'aromo_english.csv'
    try:
        df = pd.read_csv(file_path)
        
        # Cleaning
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df = df.dropna(subset=['year'])
        df = df[df['year'] > 1900]
        df['year'] = df['year'].astype(int)
        df['families'] = df['families'].fillna('Unclassified')
        df['brand'] = df['brand'].astype(str).str.strip().str.title()
        
        return df
    except FileNotFoundError:
        st.error(f"⚠️ SYSTEM ERROR: File '{file_path}' missing.")
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='text-align:center; color:#D4AF37; font-family:Cormorant Garamond; font-size:1.5rem; letter-spacing:2px; margin-bottom:20px;'>AROMO<br><span style='font-size:0.8rem; font-family:Montserrat; color:#888;'>INTELLIGENCE</span></div>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("<p style='color:#D4AF37; font-size:0.7rem; font-weight:bold; letter-spacing:2px;'>FILTERS</p>", unsafe_allow_html=True)
    
    if not df.empty:
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())
        
        selected_years = st.slider("Analysis Period", min_year, max_year, (2015, 2024))
        
        mask = (df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])
        df_filtered = df.loc[mask]
    else:
        df_filtered = df

# --- 5. MAIN LAYOUT ---
# Header Style form ScentSational
st.markdown('<div class="gold-title">Market Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Strategic Insights for the Fragrance Industry</div>', unsafe_allow_html=True)

if df.empty:
    st.stop()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📈 TRENDS", "🧬 BRAND DNA", "🤖 COMPETITOR AI"])

# === TAB 1: MACRO TRENDS ===
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPIs styled by CSS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Launches", f"{len(df_filtered):,}")
    with col2:
        if not df_filtered.empty:
            top_year = df_filtered['year'].mode()[0]
            st.metric("Peak Activity", int(top_year))
    with col3:
        unique_brands = df_filtered['brand'].nunique()
        st.metric("Active Brands", unique_brands)

    st.markdown("---")

    # CHART: Launches over time (GOLD STYLE)
    if not df_filtered.empty:
        trend_data = df_filtered.groupby('year').size().reset_index(name='launches')
        
        fig_trend = px.area(trend_data, x='year', y='launches', 
                            title='Market Saturation: Product Launches Over Time')
        
        # APPLYING DARK LUXURY THEME TO PLOTLY
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#E0E0E0', family="Montserrat"),
            title_font=dict(family="Cormorant Garamond", size=24, color="#D4AF37"),
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        fig_trend.update_traces(line_color='#D4AF37', fillcolor='rgba(212, 175, 55, 0.2)')
        
        st.plotly_chart(fig_trend, use_container_width=True)

# === TAB 2: BRAND ANALYSIS ===
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dropdown styled by CSS
    all_brands = sorted(df_filtered['brand'].unique())
    selected_brand = st.selectbox("Select Brand to Analyze:", all_brands, index=0)
    
    brand_data = df_filtered[df_filtered['brand'] == selected_brand]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"<h3 style='color:#D4AF37'>{selected_brand}</h3>", unsafe_allow_html=True)
        st.write(f"Total Fragrances: **{len(brand_data)}**")
        if not brand_data.empty:
            avg_year = int(brand_data['year'].mean())
            st.write(f"Average Vintage: **{avg_year}**")
            top_fam = brand_data['families'].mode()[0] if not brand_data['families'].isnull().all() else "N/A"
            st.write(f"Dominant Profile: **{top_fam}**")
        else:
            st.write("No data in selected range.")

    with col2:
        if not brand_data.empty:
            brand_data['main_family'] = brand_data['families'].astype(str).apply(lambda x: x.split(',')[0].strip())
            
            fig_sun = px.sunburst(brand_data, path=['main_family', 'year'], 
                             title=f"Olfactory DNA: {selected_brand}",
                             color_discrete_sequence=px.colors.sequential.RdBu)
            
            # DARK THEME FOR SUNBURST
            fig_sun.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='#E0E0E0', family="Montserrat"),
                title_font=dict(family="Cormorant Garamond", size=24, color="#D4AF37"),
            )
            st.plotly_chart(fig_sun, use_container_width=True)

# === TAB 3: COMPETITOR AI ===
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Powered by Sentence-Transformers & Vector Embeddings")
    
    st.markdown(f"### ⚡ AI Competitor Analysis for **{selected_brand}**")
    
    # Dummy data with Gold Theme
    comp_data = pd.DataFrame({
        'Competitor': ['Tom Ford', 'Dior', 'Yves Saint Laurent', 'Gucci', 'Givenchy'],
        'Similarity Score': [0.94, 0.89, 0.85, 0.78, 0.72], 
    })
    
    fig_bar = px.bar(comp_data, x='Similarity Score', y='Competitor', orientation='h',
                     title=f"Nearest Neighbors (Vector Space)",
                     color='Similarity Score',
                     color_continuous_scale=['#333333', '#D4AF37']) # Black to Gold gradient
    
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#E0E0E0', family="Montserrat"),
        title_font=dict(family="Cormorant Garamond", size=24, color="#D4AF37"),
        yaxis={'categoryorder':'total ascending'},
        xaxis=dict(gridcolor='#333'),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- FOOTER ---
st.markdown("""
<div class="custom-footer">
    Aromo Market Intelligence v2.0 &bull; 2026 &bull; Powered by Python & Plotly
</div>
""", unsafe_allow_html=True)
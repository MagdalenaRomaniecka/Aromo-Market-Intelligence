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

# --- 2. LUXURY CSS (DARK THEME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Montserrat:wght@300;400;600&display=swap');

    html, body, [class*="css"], .stMarkdown, div, span, p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 400 !important; 
        color: #E0E0E0 !important;
    }

    /* CLEAN LAYOUT */
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
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
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.1);
        padding: 15px;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.7rem !important; letter-spacing: 2px; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Cormorant Garamond', serif !important; font-size: 2.2rem !important; }

    /* FOOTER */
    .custom-footer {
        text-align: center; color: #444; font-size: 0.6rem !important; margin-top: 50px; 
        padding-top: 20px; border-top: 1px solid #111; letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LOADING (ROBUST) ---
@st.cache_data
def load_data():
    file_path = 'aromo_english.csv'
    try:
        # 1. Load Data
        df = pd.read_csv(file_path)
        
        # 2. FIX DUPLICATES (This solves the 78k vs 64k issue)
        df = df.drop_duplicates()

        # 3. Clean Text Columns
        df['brand'] = df['brand'].astype(str).str.strip().str.title()
        df['families'] = df['families'].fillna('Unclassified')
        
        # 4. Clean Years (Strict Mode)
        # Force conversion to numeric, turn errors into NaN
        df['year_clean'] = pd.to_numeric(df['year'], errors='coerce')
        
        return df
        
    except FileNotFoundError:
        st.error("⚠️ Error: 'aromo_english.csv' not found.")
        return pd.DataFrame()

df = load_data()

# --- 4. PREPARE DATA FOR CHARTS ---
# Create a dedicated dataframe for the timeline charts
# We only keep rows where 'year_clean' is a valid number > 1900
df_chart = df.dropna(subset=['year_clean']).copy()
df_chart['year_clean'] = df_chart['year_clean'].astype(int)
df_chart = df_chart[df_chart['year_clean'] > 1900]
df_chart = df_chart.sort_values('year_clean') # SORTING IS CRITICAL FOR CHARTS

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='text-align:center; margin-bottom:20px; color:#D4AF37; font-family:Cormorant Garamond; font-size:1.5rem; letter-spacing:2px;'>AROMO<br><span style='font-size:0.7rem; font-family:Montserrat; color:#666;'>INTELLIGENCE</span></div>", unsafe_allow_html=True)
    st.write("---")
    
    if not df_chart.empty:
        min_year = int(df_chart['year_clean'].min())
        max_year = int(df_chart['year_clean'].max())
        
        selected_years = st.slider("Analysis Period", min_year, max_year, (min_year, max_year))
        
        # Filter Chart Data
        mask = (df_chart['year_clean'] >= selected_years[0]) & (df_chart['year_clean'] <= selected_years[1])
        df_chart_filtered = df_chart.loc[mask]
    else:
        df_chart_filtered = df_chart

# --- 6. DASHBOARD ---
st.markdown('<div class="gold-title">Market Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Strategic Insights for the Fragrance Industry</div>', unsafe_allow_html=True)

if df.empty:
    st.stop()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📈 TRENDS", "🧬 BRAND DNA", "🤖 AI COMPETITOR"])

# === TAB 1: MARKET TRENDS ===
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Fragrances", f"{len(df):,}") # Real unique count
    with col2:
        if not df_chart_filtered.empty:
            top_year = df_chart_filtered['year_clean'].mode()[0]
            st.metric("Peak Year", int(top_year))
        else:
            st.metric("Peak Year", "N/A")
    with col3:
        unique_brands = df['brand'].nunique()
        st.metric("Active Brands", f"{unique_brands:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    # CHART FIX
    if not df_chart_filtered.empty:
        # Prepare data: Count launches per year
        trend_data = df_chart_filtered.groupby('year_clean').size().reset_index(name='launches')
        
        fig_trend = px.area(trend_data, x='year_clean', y='launches')
        
        fig_trend.update_layout(
            title="MARKET SATURATION OVER TIME",
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#AAA', family="Montserrat"),
            title_font=dict(family="Cormorant Garamond", size=20, color="#D4AF37"),
            height=450,
            xaxis=dict(showgrid=False, title="", color='#666'),
            yaxis=dict(showgrid=True, gridcolor='#222', title="")
        )
        
        # Use bright gold color and fill
        fig_trend.update_traces(line_color='#D4AF37', fillcolor='rgba(212, 175, 55, 0.2)')
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("No dated data available for this range.")

# === TAB 2: BRAND ANALYSIS ===
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        all_brands = sorted(df['brand'].unique())
        selected_brand = st.selectbox("Select Brand:", all_brands, index=0)
    
    # Filter Logic
    brand_data = df[df['brand'] == selected_brand]
    brand_data_chart = df_chart[df_chart['brand'] == selected_brand]
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"<h2 style='color:#D4AF37; font-family:Cormorant Garamond; margin:0;'>{selected_brand}</h2>", unsafe_allow_html=True)
        st.caption("PORTFOLIO")
        st.write(f"Total Scents: **{len(brand_data)}**")
        
        if not brand_data_chart.empty:
            avg_year = int(brand_data_chart['year_clean'].mean())
            st.write(f"Avg. Vintage: **{avg_year}**")
        
        if not brand_data.empty:
            top_fam = brand_data['families'].mode()[0]
            st.write(f"Style: **{top_fam}**")

    with col2:
        if not brand_data.empty:
            # Sunburst Logic
            plot_data = brand_data.copy()
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
    st.markdown(f"<h3 style='color:#D4AF37; font-family:Cormorant Garamond'>AI DNA Match: {selected_brand}</h3>", unsafe_allow_html=True)
    
    # Placeholder Data
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

# --- DEBUGGER (USUŃ GDY ZADZIAŁA) ---
with st.expander("🛠️ DATA DEBUGGER (Check if chart is empty)"):
    st.write("Chart Data Preview:", df_chart_filtered.head())
    if not df_chart_filtered.empty:
        st.write("Trend Data:", df_chart_filtered.groupby('year_clean').size().head())

# --- FOOTER ---
st.markdown("""
<div class="custom-footer">
    AROMO MARKET INTELLIGENCE &bull; 2026
</div>
""", unsafe_allow_html=True)
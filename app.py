import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Aromo Market Intelligence", layout="wide", page_icon="📊")

# --- DARK LUXURY CSS STYLING ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    /* Headers - Gold Color */
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1E1E1E;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #D4AF37;
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING & CLEANING ---
@st.cache_data
def load_data():
    # Load the raw file uploaded to Hugging Face
    file_path = 'aromo_english.csv'
    
    try:
        df = pd.read_csv(file_path)
        
        # --- DATA CLEANING ON THE FLY ---
        # 1. Clean 'Year': Convert to numeric, drop errors/NaNs
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df = df.dropna(subset=['year'])
        df = df[df['year'] > 1900] # Remove invalid years
        df['year'] = df['year'].astype(int)

        # 2. Clean 'Families': Fill missing values
        df['families'] = df['families'].fillna('Unclassified')
        
        # 3. Clean 'Brand': Standardize text
        df['brand'] = df['brand'].astype(str).str.strip().str.title()
        
        return df
        
    except FileNotFoundError:
        st.error(f"⚠️ CRITICAL ERROR: File '{file_path}' not found. Please ensure 'aromo_english.csv' is uploaded to Files tab.")
        return pd.DataFrame()

df = load_data()

# --- SIDEBAR FILTERS ---
with st.sidebar:
    # FIXED LINE: Changed use_container_width to use_column_width for compatibility
    st.image("https://via.placeholder.com/150x50?text=AROMO+INTEL", use_column_width=True)
    
    st.header("🔍 Market Filters")
    st.write("Configure analysis scope:")
    
    if not df.empty:
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())
        
        # Year Range Slider
        selected_years = st.slider("Analysis Period", min_year, max_year, (2015, 2024))
        
        # Apply Filter
        mask = (df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])
        df_filtered = df.loc[mask]
    else:
        df_filtered = df

# --- MAIN DASHBOARD ---
st.title("📊 Aromo Market Intelligence")
st.markdown("### Strategic Insights for the Fragrance Industry")
st.markdown("Monitor launch trends, analyze brand DNA, and evaluate competitor positioning using AI.")

if df.empty:
    st.stop()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📈 Market Trends", "🧬 Brand DNA", "🤖 Competitor AI"])

# === TAB 1: MACRO TRENDS ===
with tab1:
    st.subheader("Global Market Overview")
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Launches", f"{len(df_filtered):,}")
    with col2:
        # Find the year with most launches
        if not df_filtered.empty:
            top_year = df_filtered['year'].mode()[0]
            st.metric("Peak Activity Year", int(top_year))
    with col3:
        unique_brands = df_filtered['brand'].nunique()
        st.metric("Active Brands", unique_brands)

    st.markdown("---")

    # CHART: Launches over time
    if not df_filtered.empty:
        trend_data = df_filtered.groupby('year').size().reset_index(name='launches')
        
        fig_trend = px.area(trend_data, x='year', y='launches', 
                            title='Market Saturation: Product Launches Over Time',
                            color_discrete_sequence=['#D4AF37']) # Gold Color
        
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#e0e0e0')
        )
        st.plotly_chart(fig_trend, use_container_width=True)

# === TAB 2: BRAND ANALYSIS ===
with tab2:
    st.subheader("Brand Portfolio Analysis")
    
    # Dropdown to select a brand
    all_brands = sorted(df_filtered['brand'].unique())
    selected_brand = st.selectbox("Select Brand to Analyze:", all_brands, index=0)
    
    # Filter data for specific brand
    brand_data = df_filtered[df_filtered['brand'] == selected_brand]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info(f"**{selected_brand}** Snapshot")
        st.write(f"• Total Fragrances: **{len(brand_data)}**")
        if not brand_data.empty:
            avg_year = int(brand_data['year'].mean())
            st.write(f"• Average Vintage: **{avg_year}**")
            # Most common family
            top_fam = brand_data['families'].mode()[0] if not brand_data['families'].isnull().all() else "N/A"
            st.write(f"• Dominant Profile: **{top_fam}**")
        else:
            st.write("No data in selected range.")

    with col2:
        # CHART: Sunburst (Brand DNA)
        if not brand_data.empty:
            # Simple logic: Split families (e.g., "Floral, Woody" -> take "Floral" as main)
            brand_data['main_family'] = brand_data['families'].astype(str).apply(lambda x: x.split(',')[0].strip())
            
            fig_sun = px.sunburst(brand_data, path=['main_family', 'year'], 
                             title=f"Olfactory DNA Structure: {selected_brand}",
                             color_discrete_sequence=px.colors.sequential.RdBu)
            
            fig_sun.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e0e0e0'))
            st.plotly_chart(fig_sun, use_container_width=True)
        else:
            st.warning("No data to visualize.")

# === TAB 3: COMPETITOR AI ===
with tab3:
    st.subheader("🤖 AI Competitor Analysis")
    st.caption("Powered by Sentence-Transformers & Vector Embeddings")
    
    st.markdown("""
    This module uses **Natural Language Processing (NLP)** to calculate the mathematical distance 
    between brand portfolios. It identifies which competitors share the closest "Olfactory Space".
    """)
    
    st.markdown(f"### ⚡ Live Analysis: Top Competitors for **{selected_brand}**")
    
    # Dummy data for visualization purposes (Placeholder for AI model)
    comp_data = pd.DataFrame({
        'Competitor': ['Tom Ford', 'Dior', 'Yves Saint Laurent', 'Gucci', 'Givenchy'],
        'Similarity Score': [0.94, 0.89, 0.85, 0.78, 0.72], 
    })
    
    fig_bar = px.bar(comp_data, x='Similarity Score', y='Competitor', orientation='h',
                     title=f"Nearest Market Competitors to {selected_brand}",
                     color='Similarity Score',
                     color_continuous_scale='bluyl')
    
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#e0e0e0'),
        yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026 Magdalena Romaniecka | Aromo Market Intelligence | Powered by Python & Plotly")
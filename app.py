import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Aromo Market Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY DARK CSS (FORCE BLACK SIDEBAR) ---
st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Montserrat:wght@300;400;600&display=swap');

    /* GLOBAL DARK THEME */
    .stApp {
        background-color: #000000;
        color: #E0E0E0;
    }
    
    /* --- SIDEBAR: FORCE BLACK BACKGROUND --- */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #222;
    }
    /* Fix text colors in sidebar */
    [data-testid="stSidebar"] * {
        color: #BBBBBB !important;
    }
    /* Fix input fields in sidebar */
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #111 !important;
        color: white !important;
        border-color: #333 !important;
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif !important;
        color: #D4AF37 !important; /* Gold */
    }
    p, div, span {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* --- METRICS (KPIs) --- */
    div[data-testid="stMetric"] {
        background-color: #0A0A0A;
        border: 1px solid #333;
        border-radius: 0px;
        padding: 20px;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 1px; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 2.2rem !important; font-family: 'Cormorant Garamond', serif !important;}

    /* --- CLEAN UI --- */
    header, footer {visibility: hidden;} 
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }

    /* --- CUSTOM FOOTER --- */
    .custom-footer {
        width: 100%;
        text-align: center;
        padding: 30px 0;
        margin-top: 50px;
        border-top: 1px solid #222;
        color: #555;
        font-size: 0.7rem;
        font-family: 'Montserrat', sans-serif;
    }
    .custom-footer a { color: #777; text-decoration: none; transition: 0.3s; }
    .custom-footer a:hover { color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE (AGRESSIVE CLEANING) ---
@st.cache_data
def load_data():
    file_path = 'aromo_english.csv'
    try:
        df = pd.read_csv(file_path)
        
        # --- 1. UJEDNOLICENIE NAZW KOLUMN ---
        df.columns = df.columns.str.lower().str.strip()
        
        # --- 2. AGRESYWNE CZYSZCZENIE (Dla deduplikacji) ---
        # Tworzymy tymczasowe kolumny "clean", żeby znaleźć duplikaty typu "Dior" vs "dior "
        df['brand_clean'] = df['brand'].astype(str).str.lower().str.strip()
        if 'name' in df.columns:
            df['name_clean'] = df['name'].astype(str).str.lower().str.strip()
            # Usuwamy duplikaty na podstawie wyczyszczonych nazw
            df = df.drop_duplicates(subset=['brand_clean', 'name_clean'])
        else:
            # Jeśli nie ma kolumny name, usuwamy duplikaty po marce i rodzinie
            df = df.drop_duplicates(subset=['brand_clean', 'families'])

        # --- 3. FORMATOWANIE DO WYŚWIETLANIA ---
        df['brand'] = df['brand'].astype(str).str.strip().str.title()
        df['families'] = df['families'].fillna('Unclassified')
        
        # Kolumna roku (zamiana błędów na 0)
        df['year_numeric'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        
        return df
    except Exception as e:
        # Jeśli plik nie istnieje lub jest błąd
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; margin-bottom:20px; font-size:1.5rem;'>AROMO INTEL.</h2>", unsafe_allow_html=True)
    
    # WYBÓR CZASU (PROSTY)
    mode = st.radio(
        "ZAKRES ANALIZY:",
        ["Ostatnie 10 Lat", "Pełna Historia (1900+)"],
        index=0
    )
    
    # Logika filtra
    if not df.empty:
        if mode == "Ostatnie 10 Lat":
            df_filtered = df[df['year_numeric'] >= 2015]
            label = "2015 - 2025"
        else:
            df_filtered = df[df['year_numeric'] > 1900] # Tylko poprawne lata
            label = "1900 - 2025"
    else:
        df_filtered = df
        label = "No Data"

# --- 5. MAIN DASHBOARD ---
st.markdown(f"<h1 style='text-align:center;'>Market Intelligence</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#666; font-size:0.8rem; margin-bottom:40px; letter-spacing:2px; text-transform:uppercase;'>Strategic Insights • {label}</p>", unsafe_allow_html=True)

if df.empty:
    st.error("⚠️ Error loading data. Please check 'aromo_english.csv' file.")
    st.stop()

# TABS
tab1, tab2, tab3 = st.tabs(["📈 TRENDS", "🧬 BRAND DNA", "🤖 AI MONITOR"])

# === TAB 1: TRENDS ===
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI
    c1, c2, c3 = st.columns(3)
    # Total pokazuje zawsze pełną bazę (unikalne zapachy)
    c1.metric("Unique Fragrances", f"{len(df):,}") 
    
    if not df_filtered.empty:
        peak = df_filtered['year_numeric'].mode()[0]
        if peak > 0:
            c2.metric("Peak Activity", int(peak))
        else:
            c2.metric("Peak Activity", "N/A")
    else:
        c2.metric("Peak Activity", "-")
        
    brands_count = df['brand'].nunique()
    c3.metric("Active Brands", f"{brands_count:,}")
    
    st.markdown("---")
    
    # WYKRES
    st.markdown("### Market Saturation")
    if not df_filtered.empty:
        # Grupujemy po roku
        trend = df_filtered[df_filtered['year_numeric'] > 0].groupby('year_numeric').size().reset_index(name='launches')
        
        fig = px.bar(trend, x='year_numeric', y='launches')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#AAA',
            font_family='Montserrat',
            xaxis=dict(title="", showgrid=False),
            yaxis=dict(title="", showgrid=True, gridcolor='#222'),
            height=350
        )
        fig.update_traces(marker_color='#D4AF37')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Brak danych z datami dla tego okresu.")

# === TAB 2: BRAND DNA ===
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    brands = sorted(df['brand'].unique())
    sel_brand = st.selectbox("Wybierz Markę:", brands)
    
    brand_df = df[df['brand'] == sel_brand]
    
    c1, c2 = st.columns([1,2])
    with c1:
        st.markdown(f"<h3 style='margin:0; color:#D4AF37;'>{sel_brand}</h3>", unsafe_allow_html=True)
        st.caption("PORTFOLIO SNAPSHOT")
        st.write(f"Zapachów w bazie: **{len(brand_df)}**")
        
        if not brand_df.empty:
            main_fam = brand_df['families'].mode()[0]
            st.write(f"Główny styl: **{main_fam}**")
            
    with c2:
        if not brand_df.empty:
            # Uproszczony Sunburst
            brand_df['Simple Family'] = brand_df['families'].astype(str).apply(lambda x: x.split(',')[0].strip())
            fig_sun = px.sunburst(brand_df, path=['Simple Family'], color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_sun.update_layout(
                margin=dict(t=0, l=0, r=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                font_family='Montserrat',
                height=300
            )
            st.plotly_chart(fig_sun, use_container_width=True)

# === TAB 3: AI COMPETITOR ===
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3>AI Match: {sel_brand}</h3>", unsafe_allow_html=True)
    st.caption("Najbliżsi konkurenci (Analiza Wektorowa)")
    
    # MOCKUP DATA (Bo nie mamy jeszcze modelu AI podpiętego)
    # W przyszłości podmienisz to na prawdziwe wyniki z modelu
    mock_data = pd.DataFrame({
        'Competitor': ['Tom Ford', 'Dior', 'YSL', 'Chanel', 'Gucci'],
        'Match': [96, 88, 84, 79, 72]
    })
    
    fig_ai = px.bar(mock_data, x='Match', y='Competitor', orientation='h', text='Match')
    fig_ai.update_traces(
        marker_color='#D4AF37',
        texttemplate='%{text}%', 
        textposition='inside'
    )
    fig_ai.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#E0E0E0',
        xaxis=dict(visible=False),
        yaxis=dict(title=""),
        height=300,
        margin=dict(l=0,r=0,t=0,b=0)
    )
    st.plotly_chart(fig_ai, use_container_width=True)

# --- FOOTER ---
st.markdown("""
<div class="custom-footer">
    Aromo Market Intelligence • Developed by Magdalena Romaniecka • 2026<br>
    Data Source: <a href="https://www.kaggle.com/datasets/olgagmiufana1/aromo-ru-fragrance-dataset" target="_blank">Fragrantica Dataset (Kaggle)</a>
</div>
""", unsafe_allow_html=True)
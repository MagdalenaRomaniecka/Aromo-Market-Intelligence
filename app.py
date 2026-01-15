import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Aromo Market Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed" # Na telefonie domyślnie schowany
)

# --- 2. LUXURY CSS (MOBILE OPTIMIZED & DARK) ---
st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Montserrat:wght@300;400;600&display=swap');

    /* --- GLOBAL DARK THEME --- */
    .stApp {
        background-color: #000000;
        color: #E0E0E0;
    }
    
    /* --- SIDEBAR: FORCE BLACK --- */
    section[data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #222;
    }
    /* Naprawa kolorów tekstów w sidebarze */
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label {
        color: #AAAAAA !important;
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
        background-color: #111111;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] { color: #888 !important; font-size: 0.8rem !important; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 2rem !important; }

    /* --- CLEAN UP UI --- */
    header, footer {visibility: hidden;} /* Ukrywamy domyślną stopkę Streamlit */
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }

    /* --- CUSTOM FOOTER --- */
    .custom-footer {
        width: 100%;
        text-align: center;
        padding: 30px 0;
        margin-top: 50px;
        border-top: 1px solid #222;
        color: #666;
        font-size: 0.75rem;
        font-family: 'Montserrat', sans-serif;
    }
    .custom-footer a {
        color: #888;
        text-decoration: none;
        border-bottom: 1px dotted #888;
        transition: 0.3s;
    }
    .custom-footer a:hover {
        color: #D4AF37;
        border-bottom: 1px solid #D4AF37;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data
def load_data():
    file_path = 'aromo_english.csv'
    try:
        df = pd.read_csv(file_path)
        
        # 1. AGRESYWNA DEDUPLIKACJA (Naprawia licznik 78k -> ~60k)
        # Usuwamy wpisy, które mają tę samą Markę i Nazwę (ignorujemy pojemności/warianty)
        df = df.drop_duplicates(subset=['brand', 'name'])
        
        # 2. CZYSZCZENIE
        df['brand'] = df['brand'].astype(str).str.strip().str.title()
        df['families'] = df['families'].fillna('Unclassified')
        
        # 3. KOLUMNA ROKU (Dla wykresów)
        df['year_numeric'] = pd.to_numeric(df['year'], errors='coerce')
        
        return df
    except FileNotFoundError:
        st.error("⚠️ Brak pliku danych (aromo_english.csv).")
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR (MOBILE FRIENDLY) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; margin-bottom:20px;'>AROMO INTEL.</h2>", unsafe_allow_html=True)
    
    # ZAMIAST SUWAKA -> PROSTY WYBÓR (Lepsze na telefon)
    time_option = st.radio(
        "ZAKRES CZASOWY:",
        ["Ostatnie 10 Lat (Trendy)", "Pełna Historia (1900-2025)"],
        index=0
    )
    
    # Logika filtra
    df_chart = df.dropna(subset=['year_numeric']) # Tylko te z datą do wykresów
    df_chart['year_numeric'] = df_chart['year_numeric'].astype(int)
    df_chart = df_chart[df_chart['year_numeric'] > 1900]
    
    if "Ostatnie" in time_option:
        start_year = 2015
        df_filtered = df_chart[df_chart['year_numeric'] >= 2015]
        filter_label = "2015 - 2025"
    else:
        start_year = 1900
        df_filtered = df_chart
        filter_label = "1900 - 2025"

# --- 5. MAIN UI ---
st.markdown(f"<h1 style='text-align:center;'>Market Intelligence</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#666; font-size:0.8rem; margin-bottom:30px;'>STRATEGIC INSIGHTS • {filter_label}</p>", unsafe_allow_html=True)

if df.empty:
    st.stop()

# --- TABS ---
# Używamy prostych nazw, żeby mieściły się na ekranie telefonu
tab1, tab2, tab3 = st.tabs(["📈 TRENDS", "🧬 DNA", "🤖 AI"])

# === ZAKŁADKA 1: TRENDY ===
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI (Pokazują PEŁNĄ bazę, nie tylko filtrowaną, żeby widzieć skalę)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Fragrances", f"{len(df):,}") # Po deduplikacji
    
    if not df_filtered.empty:
        peak_year = int(df_filtered['year_numeric'].mode()[0])
        c2.metric("Peak Activity", peak_year)
    else:
        c2.metric("Peak Activity", "-")
        
    unique_brands = df['brand'].nunique()
    c3.metric("Active Brands", f"{unique_brands:,}")
    
    st.markdown("---")
    
    # WYKRES NASYCENIA (Naprawiony)
    if not df_filtered.empty:
        trend_counts = df_filtered.groupby('year_numeric').size().reset_index(name='launches')
        
        fig = px.bar(trend_counts, x='year_numeric', y='launches', title="Product Launches per Year")
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#AAA',
            font_family='Montserrat',
            title_font_family='Cormorant Garamond',
            title_font_color='#D4AF37',
            xaxis=dict(title="", showgrid=False),
            yaxis=dict(title="", showgrid=True, gridcolor='#222')
        )
        fig.update_traces(marker_color='#D4AF37')
        st.plotly_chart(fig, use_container_width=True)

# === ZAKŁADKA 2: BRAND DNA ===
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Wybór marki
    brands_list = sorted(df['brand'].unique())
    selected_brand = st.selectbox("Wybierz Markę:", brands_list)
    
    brand_data = df[df['brand'] == selected_brand]
    
    # Dane o marce
    c1, c2 = st.columns([1,2])
    with c1:
        st.markdown(f"<h3 style='margin:0;'>{selected_brand}</h3>", unsafe_allow_html=True)
        st.caption("PORTFOLIO OVERVIEW")
        st.write(f"Liczba zapachów: **{len(brand_data)}**")
        
        if not brand_data.empty:
             top_family = brand_data['families'].mode()[0]
             st.write(f"Główny profil: **{top_family}**")
    
    with c2:
        if not brand_data.empty:
            # Uproszczenie do Sunburst (tylko 1. rodzina)
            brand_data['Simple Family'] = brand_data['families'].astype(str).apply(lambda x: x.split(',')[0].strip())
            
            # Sunburst
            fig_sun = px.sunburst(brand_data, path=['Simple Family'], 
                                  color_discrete_sequence=px.colors.qualitative.Pastel)
            
            fig_sun.update_layout(
                margin=dict(t=0, l=0, r=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                font_family='Montserrat'
            )
            st.plotly_chart(fig_sun, use_container_width=True)
        else:
            st.info("Brak danych dla wybranej marki.")

# === ZAKŁADKA 3: AI COMPETITOR ===
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3>AI Match: {selected_brand}</h3>", unsafe_allow_html=True)
    st.caption("Analiza bliskości olfaktorycznej (Mockup Data)")
    
    # Dane przykładowe (Naprawione wyświetlanie)
    ai_data = pd.DataFrame({
        'Marka': ['Tom Ford', 'Dior', 'YSL', 'Gucci', 'Chanel'],
        'Zgodnosc': [95, 88, 82, 75, 60]
    })
    
    fig_ai = px.bar(ai_data, x='Zgodnosc', y='Marka', orientation='h', text='Zgodnosc')
    
    # Naprawa etykiet tekstowych (zamiast %text%)
    fig_ai.update_traces(
        marker_color='#D4AF37',
        texttemplate='%{text}%', # To naprawia wyświetlanie procentów
        textposition='inside'
    )
    
    fig_ai.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#E0E0E0',
        xaxis=dict(visible=False),
        yaxis=dict(title=""),
        margin=dict(l=0, r=0, t=0, b=0),
        height=300
    )
    st.plotly_chart(fig_ai, use_container_width=True)

# --- 6. STOPKA (FOOTER) ---
st.markdown("""
<div class="custom-footer">
    Aromo Market Intelligence • Developed by Magdalena Romaniecka • 2026<br>
    Data Source: <a href="https://www.kaggle.com/datasets/olgagmiufana1/aromo-ru-fragrance-dataset" target="_blank">Fragrantica Dataset (Kaggle)</a>
</div>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="Aromo Market Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. STYLIZACJA CSS (DARK LUXURY) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Montserrat:wght@300;400;600&display=swap');

    /* TŁO APLIKACJI */
    .stApp { background-color: #000000; color: #E0E0E0; }
    
    /* PASEK BOCZNY - WYMUSZONY CZARNY */
    section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222; }
    section[data-testid="stSidebar"] * { color: #AAAAAA !important; }

    /* TYPOGRAFIA */
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: #D4AF37 !important; }
    p, div, span { font-family: 'Montserrat', sans-serif !important; }

    /* KARTY METRYK (KPI) */
    div[data-testid="stMetric"] {
        background-color: #080808;
        border: 1px solid #222;
        padding: 15px;
        text-align: center;
        border-radius: 4px;
    }
    div[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.7rem !important; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 1.8rem !important; font-family: 'Cormorant Garamond', serif !important; }

    /* UKRYCIE ELEMENTÓW SYSTEMOWYCH */
    header, footer {visibility: hidden;} 
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }

    /* STOPKA */
    .custom-footer {
        width: 100%; text-align: center; padding: 30px 0; margin-top: 50px;
        border-top: 1px solid #222; color: #444; font-size: 0.7rem; font-family: 'Montserrat', sans-serif;
    }
    .custom-footer a { color: #666; text-decoration: none; }
    .custom-footer a:hover { color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SILNIK DANYCH ---
@st.cache_data
def load_data():
    file_path = 'aromo_english.csv'
    try:
        # Automatyczne wykrywanie separatora (przecinek lub średnik)
        df = pd.read_csv(file_path, sep=None, engine='python')
        
        # Normalizacja nazw kolumn
        df.columns = df.columns.str.lower().str.strip()
        
        # --- AGRESYWNE CZYSZCZENIE DUPLIKATÓW ---
        df = df.dropna(how='all') # Usuń puste wiersze
        
        # Tworzymy kolumny pomocnicze do wykrywania duplikatów
        df['brand_norm'] = df['brand'].astype(str).str.lower().str.strip()
        
        if 'name' in df.columns:
            df['name_norm'] = df['name'].astype(str).str.lower().str.strip()
            # Usuwamy duplikaty: Ta sama marka + Ta sama nazwa
            df = df.drop_duplicates(subset=['brand_norm', 'name_norm'])
        else:
            # Opcja zapasowa
            df = df.drop_duplicates(subset=['brand_norm', 'families'])

        # Formatowanie do wyświetlania
        df['Brand'] = df['brand'].astype(str).str.title().str.strip()
        
        # Naprawa daty (Kluczowe dla wykresu)
        df['Year_Numeric'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- 4. PASEK BOCZNY ---
with st.sidebar:
    st.markdown("<h3 style='text-align:center; color:#D4AF37;'>AROMO INTEL.</h3>", unsafe_allow_html=True)
    st.write("---")
    
    # Wybór zakresu czasu
    time_mode = st.radio("ZAKRES DANYCH:", ["Ostatnie 10 Lat", "Pełna Historia"], index=0)
    
    # Logika filtrowania
    if not df.empty:
        if time_mode == "Ostatnie 10 Lat":
            df_active = df[(df['Year_Numeric'] >= 2015) & (df['Year_Numeric'] <= 2025)]
            subtitle = "Trendy Rynkowe (2015-2025)"
        else:
            df_active = df[df['Year_Numeric'] > 1900]
            subtitle = "Pełna Historia Rynku"
    else:
        df_active = df
        subtitle = ""

# --- 5. GŁÓWNY PANEL ---
st.markdown("<h1 style='text-align:center;'>Aromo Market Intelligence</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#666; font-size:0.8rem; margin-bottom:40px; text-transform:uppercase;'>Strategiczna Analiza Danych • {subtitle}</p>", unsafe_allow_html=True)

if df.empty:
    st.error("⚠️ Nie udało się załadować danych. Sprawdź plik CSV.")
    st.stop()

# --- ZAKŁADKI ---
tab1, tab2, tab3 = st.tabs(["📈 TRENDY", "🧬 DNA MARKI", "🤖 MONITOR AI"])

# === ZAKŁADKA 1: TRENDY ===
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    # KPI
    c1.metric("Unikalne Zapachy", f"{len(df):,}")
    
    if not df_active.empty:
        peak = df_active['Year_Numeric'].mode()[0]
        c2.metric("Szczyt Popularności", int(peak))
    else:
        c2.metric("Szczyt Popularności", "-")
        
    brands_num = df['Brand'].nunique()
    c3.metric("Aktywne Marki", f"{brands_num:,}")
    
    st.markdown("---")
    st.markdown("### Nasycenie Rynku (Liczba Premier)")
    
    # WYKRES
    if not df_active.empty:
        trend_data = df_active.groupby('Year_Numeric').size().reset_index(name='Liczba')
        
        fig = px.bar(trend_data, x='Year_Numeric', y='Liczba')
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#AAA',
            font_family='Montserrat',
            xaxis=dict(title="", type='category', showgrid=False), # Wymuszenie osi czasu
            yaxis=dict(title="", showgrid=True, gridcolor='#222'),
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )
        fig.update_traces(marker_color='#D4AF37')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Brak danych z rocznikiem dla wybranego okresu.")

# === ZAKŁADKA 2: DNA MARKI ===
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    brands_list = sorted(df['Brand'].unique())
    sel_brand = st.selectbox("Wybierz Markę:", brands_list)
    
    brand_df = df[df['Brand'] == sel_brand]
    
    c1, c2 = st.columns([1,2])
    with c1:
        st.markdown(f"<h3 style='margin:0; color:#D4AF37;'>{sel_brand}</h3>", unsafe_allow_html=True)
        st.write(f"Liczba zapachów: **{len(brand_df)}**")
        
        if not brand_df.empty:
            style = brand_df['families'].mode()[0]
            st.write(f"Główny styl: **{style}**")
            
    with c2:
        if not brand_df.empty:
            # Uproszczenie do wykresu kołowego
            brand_df['Grupa_Zapachowa'] = brand_df['families'].astype(str).apply(lambda x: x.split(',')[0].strip())
            
            fig_sun = px.sunburst(brand_df, path=['Grupa_Zapachowa'], color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_sun.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=0, l=0, r=0, b=0),
                height=300,
                font_family='Montserrat'
            )
            st.plotly_chart(fig_sun, use_container_width=True)

# === ZAKŁADKA 3: MONITOR AI ===
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3>Dopasowanie AI: {sel_brand}</h3>", unsafe_allow_html=True)
    st.caption("Symulacja analizy konkurencji na podstawie nut zapachowych")
    
    # Dane symulacyjne (Placeholder)
    mock = pd.DataFrame({
        'Konkurent': ['Tom Ford', 'Dior', 'YSL', 'Chanel', 'Gucci'],
        'Zgodność': [95, 88, 82, 75, 70]
    })
    
    fig_ai = px.bar(mock, x='Zgodność', y='Konkurent', orientation='h', text='Zgodność')
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

# --- STOPKA ---
st.markdown("""
<div class="custom-footer">
    Aromo Market Intelligence • Developed by Magdalena Romaniecka • 2026<br>
    Źródło danych: <a href="https://www.kaggle.com/datasets/olgagmiufana1/aromo-ru-fragrance-dataset" target="_blank">Fragrantica Dataset (Kaggle)</a>
</div>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px
import re

# --- 1. KONFIGURACJA ---
st.set_page_config(page_title="Aromo Intel", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS (ZACHOWUJEMY TO CO DZIAŁA: CZERŃ I DROPDOWN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap');
    
    .stApp { background-color: #000000; color: #E0E0E0; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222; }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span { color: #888 !important; }

    /* DROPDOWN FIX (To zadziałało - zostawiamy) */
    div[data-baseweb="select"] > div { background-color: #111 !important; color: #EEE !important; border: 1px solid #333 !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"] { background-color: #111 !important; border: 1px solid #333 !important; }
    li[role="option"] { color: #CCC !important; }
    li[role="option"]:hover { background-color: #D4AF37 !important; color: #000 !important; }

    /* TYPOGRAFIA */
    h1, h2, h3 { font-family: 'Montserrat', sans-serif !important; color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 2px; }
    
    /* KPI CARDS */
    div[data-testid="stMetric"] { background-color: #090909; border: 1px solid #222; padding: 10px; border-radius: 0px; }
    div[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.7rem !important; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 1.8rem !important; }
    
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SILNIK DANYCH (RADYKALNA REDUKCJA) ---
@st.cache_data(ttl=0)
def load_data():
    file_path = 'aromo_english.csv'
    try:
        df = pd.read_csv(file_path, sep=None, engine='python')
        df.columns = df.columns.str.lower().str.strip()
        
        # 1. WYCINAJKI
        df = df.dropna(subset=['brand'])
        
        # 2. ROK (Konwersja na siłę)
        df['year_clean'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        
        # 3. RADYKALNE DEDUPLIKOWANIE (Metoda "Pierwszego Słowa")
        # Jeśli perfumy to "Chanel No 5 Eau de Parfum", bierzemy tylko "Chanel" + "No"
        # To drastycznie zmniejszy liczbę unikalnych wpisów.
        name_col = 'name' if 'name' in df.columns else 'perfume'
        
        # Funkcja pomocnicza: bierze tylko 2 pierwsze słowa z nazwy
        def get_series(text):
            words = str(text).split()
            return " ".join(words[:2]).lower() if len(words) >= 1 else str(text).lower()

        df['series_key'] = df[name_col].apply(get_series)
        df['brand_key'] = df['brand'].str.lower().str.strip()
        
        # Zostawiamy tylko jedną unikalną "Serię" dla danej marki
        df = df.drop_duplicates(subset=['brand_key', 'series_key'])
        
        # 4. Formatowanie
        df['Brand'] = df['brand'].astype(str).str.title().strip()
        df['families'] = df['families'].fillna('Unknown')
        
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("AROMO")
    st.caption("MARKET INTELLIGENCE")
    st.write("---")
    # Prosty przycisk zamiast suwaków
    show_last_10 = st.checkbox("Pokaż tylko ostatnie 10 lat", value=True)

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
    st.error("Błąd pliku CSV. Sprawdź formatowanie.")
    st.stop()

# --- KPI ---
c1, c2, c3 = st.columns(3)
c1.metric("Unikalne Linie Zapachowe", f"{len(df):,}") # Tu musi być mniej!
c2.metric("Najlepszy Rok", int(df_chart['year_clean'].mode()[0]) if not df_chart.empty else "-")
c3.metric("Aktywne Marki", f"{df['Brand'].nunique():,}")

st.markdown("---")

# --- ALTERNATYWNY WYKRES (LINIOWY) ---
st.markdown("### 📈 Dynamika Rynku (Premiery)")

if not df_chart.empty:
    # Agregacja
    chart_data = df_chart[df_chart['year_clean'] > 0].groupby('year_clean').size().reset_index(name='Liczba')
    chart_data = chart_data.sort_values('year_clean')
    
    if not chart_data.empty:
        # Zmiana na LINE CHART - jest bardziej "odporny" na błędy wyświetlania niż Area
        fig = px.line(chart_data, x='year_clean', y='Liczba', markers=True)
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#AAA',
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor='#222', title=""),
            height=350,
            margin=dict(l=0,r=0,t=10,b=0)
        )
        # Złota linia
        fig.update_traces(line_color='#D4AF37', line_width=3, marker_size=8)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Brak danych z datami w wybranym okresie.")
else:
    st.info("Brak danych do wyświetlenia wykresu.")

# --- TABS ---
t1, t2 = st.tabs(["🧬 BRAND DNA", "🤖 AI COMPETITOR"])

with t1:
    brands = sorted(df['Brand'].unique())
    sel_brand = st.selectbox("Wybierz Markę:", brands)
    b_df = df[df['Brand'] == sel_brand]
    
    colA, colB = st.columns([1,2])
    with colA:
        st.write(f"**{sel_brand}**")
        st.write(f"Liczba linii: {len(b_df)}")
        if not b_df.empty:
            st.write(f"Styl: {b_df['families'].mode()[0]}")
            
    with colB:
        if not b_df.empty:
            # Uproszczony wykres kołowy zamiast Sunburst
            b_df['Main_Fam'] = b_df['families'].astype(str).apply(lambda x: x.split(',')[0])
            fig_pie = px.pie(b_df, names='Main_Fam', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=0,b=0))
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

with t2:
    st.markdown(f"**Konkurencja dla: {sel_brand}**")
    # Mockup
    mock = pd.DataFrame({'Marka': ['Tom Ford', 'Dior', 'YSL'], 'Podobienstwo': [95, 85, 75]})
    
    # Naprawa etykiet (text_auto)
    fig_bar = px.bar(mock, x='Podobienstwo', y='Marka', orientation='h', text_auto=True)
    fig_bar.update_traces(marker_color='#D4AF37', textfont_color='black')
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font_color='#AAA', xaxis=dict(visible=False), yaxis=dict(title=""),
        height=250, margin=dict(t=0,b=0)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- DEBUGGER (POKAŻE PRAWDĘ) ---
with st.expander("🛠️ DEBUGGER - SPRAWDŹ DANE"):
    st.write("Pierwsze 5 wierszy z bazy (sprawdź kolumnę year_clean):")
    st.dataframe(df.head())
    st.write(f"Liczba wierszy z rokiem > 0: {len(df[df['year_clean'] > 0])}")
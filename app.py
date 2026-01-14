import streamlit as st
import pandas as pd
import plotly.express as px

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Aromo Market Intelligence", layout="wide")

# --- CUSTOM CSS (STYL SCENTSATIONAL ATELIER) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400&display=swap');

    /* Tło i główna czcionka */
    .stApp {
        background-color: #FDFCFB;
        color: #2D2D2D;
        font-family: 'Montserrat', sans-serif;
    }

    /* Nagłówki */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #1A365D !important;
    }

    /* Karty danych */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #F1EFE9;
    }

    /* Sidebar - elegancki wygląd */
    section[data-testid="stSidebar"] {
        background-color: #F8F5F2;
        border-right: 1px solid #EAE2D7;
    }

    /* Przycisk */
    .stButton>button {
        background-color: #C5A059;
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.5rem 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOCKUP DANYCH (Tutaj połączysz swoją bazę 64k) ---
# Ustawienie domyślne na pełny zakres, aby pokazać 64,000 rekordów
TOTAL_RECORDS = 64364 

# --- SIDEBAR (FILTRY) ---
st.sidebar.image("https://via.placeholder.com/150x50?text=ATELIER+LOGO", use_container_width=True) # Podepnij swoje logo
st.sidebar.title("Market Filters")

# KLUCZOWA POPRAWKA: Zakres dat ustawiony domyślnie na całość
year_range = st.sidebar.slider(
    "Analysis Period", 
    min_value=1900, 
    max_value=2026, 
    value=(1900, 2026) 
)

# --- HEADER ---
st.title("Aromo Market Intelligence")
st.markdown("### Strategic Insights for the Fragrance Industry")

# --- SEKCOJA 1: GLOBAL OVERVIEW ---
col1, col2, col3 = st.columns(3)
with col1:
    # Wyświetlamy pełną liczbę zamiast ułamka
    st.metric("Total Launches", f"{TOTAL_RECORDS:,}")
with col2:
    st.metric("Peak Activity Year", "2017")
with col3:
    st.metric("Active Brands", "1,723")

# --- SEKCOJA 2: WYKRES NASYCENIA (NAPRAWA OSI Y) ---
st.subheader("Market Saturation: Product Launches Over Time")

# Przykładowe dane trendu
chart_data = pd.DataFrame({
    'year': range(1900, 2027),
    'launches': [i**1.5 / 10 for i in range(127)] # Trend rosnący
})

fig_trend = px.area(chart_data, x='year', y='launches',
                    color_discrete_sequence=['#C5A059'])

fig_trend.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=20, b=0),
    yaxis=dict(range=[0, chart_data['launches'].max() * 1.1], title="Liczba Premier", gridcolor='#F1F1F1'),
    xaxis=dict(title="Rok", gridcolor='#F1F1F1')
)
st.plotly_chart(fig_trend, use_container_width=True)

# --- SEKCOJA 3: ANALIZA KONKURENCJI (NAPRAWA TOOLTIPÓW) ---
st.subheader("AI Competitor Analysis: Olfactory Proximity")

comp_data = pd.DataFrame({
    'Competitor': ['Givenchy', 'Gucci', 'Yves Saint Laurent', 'Dior', 'Tom Ford'],
    'Similarity': [4.0, 3.8, 2.1, 1.0, 0.5]
})

fig_comp = px.bar(comp_data, x='Similarity', y='Competitor', 
                   orientation='h',
                   color_discrete_sequence=['#1A365D'])

# POPRAWKA: Czyste etykiety bez błędów kodu
fig_comp.update_traces(
    hovertemplate="<b>%{y}</b><br>Zgodność DNA: %{x} / 4.0<extra></extra>"
)

fig_comp.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title="Similarity Score (AI Match)", gridcolor='#F1F1F1'),
    yaxis=dict(title="", autorange="reversed")
)
st.plotly_chart(fig_comp, use_container_width=True)

# --- FOOTER ---
st.divider()
st.caption("© 2026 Scentsational Atelier | Powered by AI Market Intelligence")
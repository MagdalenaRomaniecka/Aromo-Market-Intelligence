import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Aromo Intel",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. DARK LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap');
    
    .stApp { background-color: #000000; color: #E0E0E0; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222; }
    section[data-testid="stSidebar"] * { color: #888 !important; }
    
    /* DROPDOWN FIX */
    div[data-baseweb="select"] > div { background-color: #111 !important; color: #EEE !important; border: 1px solid #333 !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] { background-color: #111 !important; border: 1px solid #333 !important; }
    li[role="option"] { color: #CCC !important; }
    li[role="option"]:hover { background-color: #D4AF37 !important; color: #000 !important; }

    /* TYPOGRAPHY */
    h1, h2, h3 { font-family: 'Montserrat', sans-serif !important; color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 2px; }
    
    /* METRICS */
    div[data-testid="stMetric"] { background-color: #090909; border: 1px solid #222; padding: 10px; }
    div[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.7rem !important; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 1.8rem !important; }
    
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=0)
def load_data():
    file_path = 'aromo_english.csv'
    try:
        df = pd.read_csv(file_path, sep=None, engine='python')
        df.columns = df.columns.str.lower().str.strip()
        
        # Cleanup
        df = df.dropna(subset=['brand'])
        
        # Fix Brand Names (Remove #, *)
        df['Brand'] = df['brand'].astype(str).str.strip().str.lstrip("#*-").str.title()
        
        # Year Parsing
        df['year_clean'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        
        # Deduplication
        name_col = 'name' if 'name' in df.columns else 'perfume'
        if name_col in df.columns:
            df['name_norm'] = df[name_col].astype(str).str.lower().str.strip()
            df['brand_norm'] = df['Brand'].str.lower()
            df = df.drop_duplicates(subset=['brand_norm', 'name_norm'])
        
        # Families
        df['families'] = df['families'].fillna('Unknown')
        
        return df
    except Exception as e:
        st.error(f"⚠️ Data Error: {e}")
        return pd.DataFrame()

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("AROMO")
    st.write("---")
    show_last_10 = st.checkbox("Last 10 Years Only", value=True)

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
    st.stop()

# KPI
c1, c2, c3 = st.columns(3)
c1.metric("Unique Fragrances", f"{len(df):,}") 
c2.metric("Peak Year", int(df_chart['year_clean'].mode()[0]) if not df_chart.empty else "-")
c3.metric("Active Brands", f"{df['Brand'].nunique():,}")

st.markdown("---")

# --- TABS (ON TOP) ---
tab_trends, tab_dna, tab_ai = st.tabs(["📈 TRENDS", "🧬 BRAND DNA", "🤖 AI COMPETITOR"])

# === TAB 1: TRENDS (AREA CHART - ALWAYS VISIBLE) ===
with tab_trends:
    st.markdown("### Market Saturation")
    
    if not df_chart.empty:
        # Group by year
        chart_data = df_chart[df_chart['year_clean'] > 0].groupby('year_clean').size().reset_index(name='Count')
        chart_data = chart_data.sort_values('year_clean')
        
        if not chart_data.empty:
            # AREA CHART (Filled Mountain) - Najlepiej widoczny
            fig = px.area(chart_data, x='year_clean', y='Count')
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#E0E0E0',
                # Axis Settings
                xaxis=dict(showgrid=False, title="", color='#AAA'),
                yaxis=dict(showgrid=True, gridcolor='#222', title="", zeroline=False),
                height=350,
                margin=dict(l=0,r=0,t=10,b=0),
                hovermode="x unified"
            )
            # Gold Fill
            fig.update_traces(line_color='#D4AF37', fillcolor='rgba(212, 175, 55, 0.3)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data for chart.")

# === TAB 2: BRAND DNA (LABELS INSIDE) ===
with tab_dna:
    st.markdown("<br>", unsafe_allow_html=True)
    brands = sorted(df['Brand'].unique())
    
    # Default: Tom Ford
    default_ix = brands.index("Tom Ford") if "Tom Ford" in brands else 0
    sel_brand = st.selectbox("Select Brand:", brands, index=default_ix)
    b_df = df[df['Brand'] == sel_brand]
    
    colA, colB = st.columns([1,2])
    with colA:
        st.markdown(f"<h2 style='color:#D4AF37; margin:0'>{sel_brand}</h2>", unsafe_allow_html=True)
        st.write(f"**Total Scents:** {len(b_df)}")
        if not b_df.empty:
            style = b_df['families'].mode()[0] if not b_df['families'].mode().empty else "Unknown"
            st.write(f"**Key Style:** {style}")
            
    with colB:
        if not b_df.empty and 'families' in b_df.columns:
            b_df['Main_Fam'] = b_df['families'].astype(str).apply(lambda x: x.split(',')[0])
            
            fig_pie = px.pie(b_df, names='Main_Fam', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                font_color='#DDD', 
                height=300, 
                margin=dict(t=0,b=0),
                showlegend=False # UKRYWAMY LEGENDĘ (zajmuje miejsce)
            )
            # POKAZUJEMY NAZWY NA WYKRESIE
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

# === TAB 3: AI COMPETITOR (CLEAN AXIS) ===
with tab_ai:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### AI Match: {sel_brand}")
    
    # Dane
    mock = pd.DataFrame({
        'Competitor': ['Tom Ford', 'Dior', 'YSL', 'Chanel', 'Gucci'], 
        'Score': [95, 88, 82, 75, 70]
    })
    
    # Wykres
    fig_bar = px.bar(mock, x='Score', y='Competitor', orientation='h', text='Score')
    
    fig_bar.update_traces(
        marker_color='#D4AF37', 
        texttemplate='%{text}%', # Pokazuje "95%"
        textposition='inside',
        textfont_color='black'
    )
    
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font_color='#AAA', 
        # CAŁKOWICIE UKRYWAMY DOLNĄ OŚ (1, 2, 3...)
        xaxis=dict(visible=False), 
        yaxis=dict(title=""), 
        height=250, 
        margin=dict(t=0,b=0)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- FOOTER ---
st.markdown("<div style='text-align:center; color:#444; margin-top:50px; border-top:1px solid #222; padding-top:20px; font-size:0.8rem;'>Aromo Market Intelligence • 2026</div>", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter
import re
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Aromo Intel | Atelier",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LUXURY DARK CSS (FIXED DROPDOWN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    /* GLOBAL DARK THEME */
    .stApp { background-color: #050505; color: #E0E0E0; font-family: 'Montserrat', sans-serif; }
    
    /* HEADERS - CENTERED & ELEGANT */
    h1, h2, h3, h4, h5, h6 { 
        font-family: 'Cormorant Garamond', serif !important; 
        text-align: center !important; 
        color: #FFF !important;
        text-transform: uppercase;
        font-weight: 400 !important;
    }
    h1 { font-size: 3.5rem !important; margin: 20px 0 10px 0; letter-spacing: 2px; }
    h3 { font-size: 1.5rem !important; color: #D4AF37 !important; margin-top: 50px; margin-bottom: 30px; border-bottom: 1px solid #333; padding-bottom: 10px; letter-spacing: 3px; }
    
    /* INTRO TEXT (ADDED) */
    .intro-text {
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.9rem;
        color: #AAA;
        max_width: 800px;
        margin: 0 auto 40px auto;
        line-height: 1.6;
        border-bottom: 1px solid #222;
        padding-bottom: 20px;
    }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #222;
    }
    
    /* --- FIX: DROPDOWN MENU BACKGROUND (BLACK) --- */
    div[data-baseweb="select"] > div {
        background-color: #111 !important;
        color: #FFF !important;
        border-color: #333 !important;
    }
    div[data-baseweb="menu"], div[role="listbox"], div[data-baseweb="popover"] {
        background-color: #050505 !important;
        border: 1px solid #333 !important;
    }
    li[role="option"] {
        background-color: #050505 !important;
        color: #E0E0E0 !important;
    }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #1a1a1a !important;
        color: #D4AF37 !important;
        font-weight: bold !important;
    }
    
    /* METRICS */
    .gold-metric { 
        border: 1px solid rgba(212, 175, 55, 0.2); 
        background-color: rgba(255, 255, 255, 0.02); 
        padding: 20px; 
        text-align: center; 
    }
    .metric-value { font-family: 'Cormorant Garamond', serif; font-size: 2.5rem; color: #F0E68C; }
    .metric-label { font-family: 'Montserrat'; font-size: 0.7rem; letter-spacing: 2px; color: #888; text-transform: uppercase; }
    
    /* CARDS & SIGNATURES */
    .perfume-card { 
        border: 1px solid rgba(212, 175, 55, 0.3); 
        background: #111; 
        padding: 25px; 
        margin-bottom: 20px; 
        text-align: center; 
        position: relative;
    }
    .card-signature {
        width: 40px; height: 40px;
        border: 1px solid #D4AF37;
        border-radius: 50%;
        color: #D4AF37;
        font-family: 'Cormorant Garamond';
        font-size: 1.2rem;
        line-height: 38px;
        margin: 0 auto 10px auto;
        display: block;
    }
    .card-title { font-family: 'Cormorant Garamond'; font-size: 1.4rem; color: #FFF; margin-bottom: 5px; }
    .card-meta { font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; }
    
    .gold-btn { 
        text-decoration: none; color: #000 !important; background: #D4AF37; 
        padding: 8px 25px; font-size: 0.7rem; font-weight: 700; 
        display: inline-block; border-radius: 2px; text-transform: uppercase; letter-spacing: 1px;
    }
    
    /* BRAND HEADER BOX */
    .brand-signature-box { 
        border: 1px solid rgba(212, 175, 55, 0.4); 
        background: radial-gradient(circle, rgba(30,30,30,1) 0%, rgba(10,10,10,1) 100%);
        padding: 40px; margin-bottom: 40px; text-align: center; 
    }
    .brand-main-emblem { 
        width: 80px; height: 80px;
        border: 2px solid #D4AF37;
        border-radius: 50%;
        color: #D4AF37;
        font-family: 'Cormorant Garamond';
        font-size: 2.5rem;
        line-height: 76px;
        margin: 0 auto 15px auto;
        display: block;
    }
    
    /* FOOTER & CHART TEXT */
    .chart-insight { font-family: 'Montserrat', sans-serif; font-size: 0.8rem; color: #888; text-align: center; margin-top: 10px; font-style: italic; }
    .custom-footer { text-align: center; margin-top: 100px; padding-top: 40px; border-top: 1px solid #333; color: #666; font-size: 0.75rem; letter-spacing: 1px; line-height: 1.8; }
    .footer-link { color: #D4AF37; text-decoration: none; border-bottom: 1px dotted #D4AF37; }
    
    /* TAB CENTERING HACK */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; }
    
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=0)
def load_data():
    file_path = 'aromo_english.csv'
    if not os.path.exists(file_path): return pd.DataFrame(), "FILE_NOT_FOUND"

    try:
        # Explicit comma separator
        df = pd.read_csv(file_path, sep=',', on_bad_lines='skip', engine='python')
        df.columns = df.columns.str.lower().str.strip()
        df = df.dropna(subset=['brand'])
        
        # Clean Data
        df['Brand'] = df['brand'].astype(str).str.strip().str.lstrip("#*-").str.title()
        df['display_name'] = df['name'].astype(str).str.strip() if 'name' in df.columns else "Unknown"
        df['Type_Raw'] = df['type'].astype(str).str.strip() if 'type' in df.columns else "Fragrance"
        
        # Year
        if 'year' in df.columns:
            df['year_clean'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        else: df['year_clean'] = 0
            
        # Segment
        df['Segment_Raw'] = df['segment'].astype(str) if 'segment' in df.columns else "Unknown"

        # Families
        if 'families' in df.columns:
            df['families'] = df['families'].astype(str).replace('nan', 'Unknown')
            df['Main_Fam'] = df['families'].apply(lambda x: x.split(',')[0].strip().title().replace("['", "").replace("']", "") if isinstance(x, str) else "Unknown")
        else: df['Main_Fam'] = "Unknown"
            
        # Notes
        if 'top_notes' in df.columns:
            df['notes_display'] = df['top_notes'].astype(str).replace('nan', '').apply(lambda x: x[:60] + "..." if len(x) > 60 else x)
            df['notes_list'] = df['top_notes'].astype(str).replace('nan', '').apply(lambda x: [i.strip() for i in x.split(',') if i.strip()])
        else:
            df['notes_display'] = ""; df['notes_list'] = [[] for _ in range(len(df))]
            
        df['url'] = df['url'] if 'url' in df.columns else "#"
        return df, "OK"
    except Exception as e: return pd.DataFrame(), str(e)

def get_initials(text):
    if not isinstance(text, str): return "SC"
    words = text.replace("'", "").split()
    return (words[0][0] + words[1][0]).upper() if len(words) >= 2 else words[0][:2].upper()

# --- 4. EXECUTE LOAD ---
df, status = load_data()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; color:#D4AF37; font-family:"Cormorant Garamond"; font-size:1.5rem; margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:10px;'>
    ATELIER SETTINGS
    </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        st.success(f"DATABASE ONLINE\n{len(df):,} Records")
        st.markdown("---")
        filter_mode = st.radio("SCOPE", ["All Products", "Fine Fragrance Only"])
        
        # --- FIX: FILTERING LOGIC (METRICS will now change) ---
        if filter_mode == "Fine Fragrance Only":
            mask = df['Type_Raw'].str.contains('Parfum|Toilette|Cologne|EdP|EdT', case=False, na=False)
            df_filtered = df[mask].copy()
        else: 
            df_filtered = df.copy()
            
        df_brand_view = df_filtered.copy() # Use this for Brand Tab
    else:
        st.error(f"Status: {status}")
        df_filtered = pd.DataFrame()
        df_brand_view = pd.DataFrame()

# --- 6. HEADER ---
st.markdown("<h1>AROMO INTELLIGENCE</h1>", unsafe_allow_html=True)

# --- ADDED: INTRO DESCRIPTION ---
st.markdown("""
<div class="intro-text">
    Welcome to the <b>Aromo Intelligence Atelier</b>. This interactive dashboard provides a deep-dive analysis 
    of the global fragrance market. Explore trends, analyze brand portfolios, and discover the olfactory DNA 
    of thousands of perfumes. Data powered by the Aromo.ru dataset.
</div>
""", unsafe_allow_html=True)

if df.empty: st.stop()

# METRICS (Using df_filtered to react to sidebar)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="gold-metric"><div class="metric-label">Global Portfolio</div><div class="metric-value">{len(df_filtered):,}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="gold-metric"><div class="metric-label">Unique Brands</div><div class="metric-value">{df_filtered["Brand"].nunique():,}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="gold-metric"><div class="metric-label">Olfactory Families</div><div class="metric-value">{df_filtered["Main_Fam"].nunique():,}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 7. TABS ---
tab_brand, tab_global = st.tabs(["BRAND ANALYSIS", "GLOBAL MARKET"])

# =========================================================
# TAB 1: BRAND ANALYSIS
# =========================================================
with tab_brand:
    st.markdown("<h3>BRAND ANALYSIS</h3>", unsafe_allow_html=True) # Explicit centered header
    
    if df_brand_view.empty:
        st.warning("No data available.")
    else:
        brands = sorted(df_brand_view['Brand'].unique())
        idx = brands.index("Tom Ford") if "Tom Ford" in brands else 0
        
        c_fill1, c_sel, c_fill2 = st.columns([1, 2, 1])
        with c_sel:
            st.markdown("<div style='text-align:center; color:#D4AF37; font-size:0.8rem; letter-spacing:2px; margin-bottom:5px;'>SELECT MAISON</div>", unsafe_allow_html=True)
            sel_brand = st.selectbox("Brand", brands, index=idx, label_visibility="collapsed")

        b_df = df_brand_view[df_brand_view['Brand'] == sel_brand]
        
        # HEADER BOX
        brand_init = get_initials(sel_brand)
        seg_str = "ESTABLISHED HOUSE"
        if 'Segment_Raw' in b_df.columns:
            val = b_df['Segment_Raw'].iloc[0]
            if pd.notna(val) and str(val) != 'nan': seg_str = str(val).upper()

        st.markdown(f"""
        <div class="brand-signature-box">
            <div class="brand-main-emblem">{brand_init}</div>
            <div style="font-family:'Cormorant Garamond'; font-size:3rem; color:#FFF; margin-bottom:10px;">{sel_brand}</div>
            <div style="font-family:'Montserrat'; font-size:0.8rem; color:#D4AF37; letter-spacing:3px;">{len(b_df)} CREATIONS • {seg_str}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # LATEST RELEASES (WITH SIGNATURE)
        st.markdown("<h3>LATEST RELEASES</h3>", unsafe_allow_html=True)
        if not b_df.empty:
            top_scents = b_df.sort_values('year_clean', ascending=False).head(4)
            cols = st.columns(2)
            for i, (idx, row) in enumerate(top_scents.iterrows()):
                year_str = str(row['year_clean']) if row['year_clean'] > 0 else "N/A"
                initials = get_initials(row['display_name'])
                with cols[i % 2]: 
                    st.markdown(f"""
                    <div class="perfume-card">
                        <div class="card-signature">{initials}</div>
                        <div class="card-title">{row['display_name']}</div>
                        <div class="card-meta">{row['Type_Raw']} • {year_str}</div>
                        <div class="card-notes">{row['notes_display']}</div>
                        <a href="{row['url']}" target="_blank" class="gold-btn">VIEW PROFILE</a>
                    </div>
                    """, unsafe_allow_html=True)

        # --- TIMELINE ---
        st.markdown("<h3>ACTIVITY TIMELINE (MODERN ERA)</h3>", unsafe_allow_html=True)
        if not b_df.empty:
            timeline_series = b_df[b_df['year_clean'] >= 2000]['year_clean'].value_counts().sort_index()
            
            if not timeline_series.empty:
                x_vals = timeline_series.index.astype(str).tolist()
                y_vals = timeline_series.values.tolist()
                max_y = max(y_vals)

                fig_time = go.Figure(go.Bar(
                    x=x_vals, y=y_vals,
                    text=y_vals,
                    textposition='outside', # Value on top
                    texttemplate='%{y}',    # Force Y value
                    cliponaxis=False,
                    marker_color='#D4AF37',
                    textfont=dict(color='white', size=14, weight='bold')
                ))
                fig_time.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=450,
                    xaxis=dict(showgrid=False, title="", type='category'),
                    yaxis=dict(showgrid=True, gridcolor='#333', title="", range=[0, max_y * 1.4]),
                    margin=dict(t=50, b=40)
                )
                st.plotly_chart(fig_time, use_container_width=True)
            else: st.info("No releases found after year 2000.")

        st.markdown("<br>", unsafe_allow_html=True)

        # DNA & INGREDIENTS
        c_dna, c_ing = st.columns(2)
        with c_dna:
            st.markdown("<h3>OLFACTORY DNA</h3>", unsafe_allow_html=True)
            fam_series = b_df['Main_Fam'].value_counts().head(8).sort_values(ascending=True)
            
            if not fam_series.empty:
                x_vals = fam_series.values.tolist()
                y_vals = fam_series.index.tolist()
                max_x = max(x_vals)
                
                fig_dna = go.Figure(go.Bar(
                    x=x_vals, y=y_vals, orientation='h',
                    text=x_vals,
                    textposition='outside',
                    texttemplate='%{x}',
                    cliponaxis=False,
                    marker_color='#D4AF37', textfont=dict(color='white', size=14, weight='bold')
                ))
                fig_dna.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=500,
                    xaxis=dict(showgrid=False, visible=False, range=[0, max_x * 1.5]), # 50% Space
                    yaxis=dict(tickfont=dict(color='#E0E0E0', size=12)),
                    margin=dict(r=180) # HUGE RIGHT MARGIN
                )
                st.plotly_chart(fig_dna, use_container_width=True)

        with c_ing:
            st.markdown("<h3>SIGNATURE INGREDIENTS</h3>", unsafe_allow_html=True)
            all_n = [x for sub in b_df['notes_list'] for x in sub]
            if all_n:
                top_n = pd.Series(Counter(all_n)).sort_values(ascending=False).head(8).sort_values(ascending=True)
                x_vals = top_n.values.tolist()
                y_vals = top_n.index.tolist()
                max_x = max(x_vals)
                
                fig_ing = go.Figure(go.Bar(
                    x=x_vals, y=y_vals, orientation='h',
                    text=x_vals,
                    textposition='outside',
                    texttemplate='%{x}',
                    cliponaxis=False, 
                    marker_color='#B8860B', textfont=dict(color='white', size=14, weight='bold')
                ))
                fig_ing.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=500,
                    xaxis=dict(showgrid=False, visible=False, range=[0, max_x * 1.5]),
                    yaxis=dict(tickfont=dict(color='#E0E0E0', size=12)),
                    margin=dict(r=180) # HUGE RIGHT MARGIN
                )
                st.plotly_chart(fig_ing, use_container_width=True)

# =========================================================
# TAB 2: GLOBAL MARKET
# =========================================================
with tab_global:
    st.markdown("<h3>GLOBAL MARKET TRENDS</h3>", unsafe_allow_html=True)
    # --- FIX: GREY TEXT (REPLACED ST.INFO) ---
    st.markdown("<div class='chart-insight'>Analysis based on full dataset (78,000+ records).</div>", unsafe_allow_html=True)

    # 1. TOP BRANDS
    st.markdown("<h3>TOP 15 BRANDS (VOLUME)</h3>", unsafe_allow_html=True)
    brand_series = df_filtered['Brand'].value_counts().head(15).sort_values(ascending=True)
    
    # RAW LIST EXTRACTION TO PREVENT PANDAS INDEX ERRORS
    y_labels = brand_series.index.tolist()
    x_values = brand_series.values.tolist()
    max_val = max(x_values)
    
    fig1 = go.Figure(go.Bar(
        x=x_values, y=y_labels, orientation='h',
        text=x_values, 
        textposition='outside',
        texttemplate='%{x}', # Force X value
        cliponaxis=False,
        marker_color='#D4AF37', textfont=dict(color='white', size=14, weight='bold')
    ))
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=600, 
        xaxis=dict(showgrid=False, visible=False, range=[0, max_val * 1.4]), 
        yaxis=dict(tickfont=dict(color='#E0E0E0', size=12)), margin=dict(r=180)
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("<div class='chart-insight'>Brands with the largest number of releases.</div>", unsafe_allow_html=True)

    # 2. FAMILIES
    st.markdown("<h3>TOP OLFACTORY FAMILIES</h3>", unsafe_allow_html=True)
    fam_series = df_filtered['Main_Fam'].value_counts().head(15)
    if 'Unknown' in fam_series: fam_series = fam_series.drop('Unknown')
    fam_series = fam_series.sort_values(ascending=True)
    
    y_labels = fam_series.index.tolist()
    x_values = fam_series.values.tolist()
    max_val = max(x_values)
    
    fig2 = go.Figure(go.Bar(
        x=x_values, y=y_labels, orientation='h',
        text=x_values, 
        textposition='outside',
        texttemplate='%{x}',
        cliponaxis=False,
        marker_color='#B8860B', textfont=dict(color='white', size=14, weight='bold')
    ))
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=600,
        xaxis=dict(showgrid=False, visible=False, range=[0, max_val * 1.4]),
        yaxis=dict(tickfont=dict(color='#E0E0E0', size=12)), margin=dict(r=180)
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("<div class='chart-insight'>Most popular fragrance families.</div>", unsafe_allow_html=True)

    # 3. YEARS
    st.markdown("<h3>LAUNCH HISTORY (TOP 15 YEARS)</h3>", unsafe_allow_html=True)
    year_series = df_filtered[(df_filtered['year_clean'] > 1990) & (df_filtered['year_clean'] <= 2026)]['year_clean'].value_counts().head(15).sort_index(ascending=True)
    
    x_cats = year_series.index.astype(str).tolist()
    y_vals = year_series.values.tolist()
    max_val = max(y_vals)
    
    fig3 = go.Figure(go.Bar(
        x=x_cats, y=y_vals,
        text=y_vals, 
        textposition='outside',
        texttemplate='%{y}',
        cliponaxis=False,
        marker_color='#A0522D', textfont=dict(color='white', size=14, weight='bold')
    ))
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=500,
        xaxis=dict(showgrid=False, title="", type='category'),
        yaxis=dict(showgrid=False, visible=False, range=[0, max_val * 1.4]),
        margin=dict(t=50)
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("<div class='chart-insight'>Most active years for new perfume launches.</div>", unsafe_allow_html=True)

    # 4. WORDS
    st.markdown("<h3>MOST POPULAR NAME WORDS</h3>", unsafe_allow_html=True)
    text_data = " ".join(df_filtered['display_name'].dropna().astype(str))
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text_data.lower())
    stop_words = set(['eau', 'de', 'parfum', 'toilette', 'cologne', 'the', 'le', 'la', 'les', 'for', 'men', 'women', 'pour', 'homme', 'femme', 'intense', 'elixir', 'and', 'of', 'in', 'to', 'a', 'by', 'no', 'vol', 'ml', 'edp', 'edt', 'spray', 'water', 'collection', 'edition', 'unknown'])
    filtered = [w.capitalize() for w in words if w not in stop_words]
    
    word_series = pd.Series(Counter(filtered)).sort_values(ascending=False).head(15).sort_values(ascending=True)
    y_labels = word_series.index.tolist()
    x_values = word_series.values.tolist()
    max_val = max(x_values)
    
    fig_w = go.Figure(go.Bar(
        x=x_values, y=y_labels, orientation='h',
        text=x_values, 
        textposition='outside',
        texttemplate='%{x}',
        cliponaxis=False,
        marker_color='#B8860B', textfont=dict(color='white', size=14, weight='bold')
    ))
    fig_w.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=600,
        xaxis=dict(showgrid=False, visible=False, range=[0, max_val * 1.4]),
        yaxis=dict(tickfont=dict(color='#E0E0E0', size=12)), margin=dict(r=180)
    )
    st.plotly_chart(fig_w, use_container_width=True)
    st.markdown("<div class='chart-insight'>Common keywords found in perfume names.</div>", unsafe_allow_html=True)

# --- 9. FOOTER ---
st.markdown("""
<div class="custom-footer">
    Aromo Market Intelligence • Developed by Magdalena Romaniecka • 2026<br>
    Data Source: <a href="https://www.kaggle.com/datasets/olgagmiufana1/aromo-ru-fragrance-dataset" target="_blank" class="footer-link">Aromo.ru Dataset (Kaggle)</a> 
    • Code available on <a href="https://github.com/MagdalenaRomaniecka/Aromo-Market-Intelligence" target="_blank" class="footer-link">GitHub</a>
</div>
""", unsafe_allow_html=True)
---
title: Aromo Market Intelligence
emoji: 📊
colorFrom: yellow
colorTo: gray
sdk: streamlit
sdk_version: 1.31.0
app_file: app.py
pinned: false
license: mit
---

# Aromo Market Intelligence 📊

Professional dashboard for fragrance market analysis.
# 💎 Aromo Market Intelligence

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Live%20App-blue)](https://huggingface.co/spaces/Baphomert/Aromo-Market-Intelligence)
[![Python](https://img.shields.io/badge/Python-3.9%2B-yellow)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)](https://streamlit.io/)

**A comprehensive Business Intelligence dashboard for the fragrance industry, exploring global trends, brand DNA, and the structure of the olfactory market.**

👉 **[View Live App](https://huggingface.co/spaces/Baphomert/Aromo-Market-Intelligence)**

---

## 🎯 Project Objective
The goal was to build a specialized analytical tool ("Atelier") for the perfumery sector that enables:
1.  **Macro Analysis:** Understanding global market shifts, dominant olfactory families, and release dynamics over decades.
2.  **Micro Analysis:** Profiling specific fashion houses (e.g., Tom Ford, Chanel) to decode their unique "scent signature."
3.  **Data Verification:** Transforming a raw, noisy dataset into interactive, actionable insights.

---

## ⚙️ Process & Methodology (The Data Science Journey)

The path from raw data to the final v145 deployment involved several critical stages:

### 1. Data Wrangling & Cleaning
The project utilizes the Aromo.ru dataset (78,000+ records).
* **Challenge:** The raw data contained significant noise—inconsistent date formats, duplicate scent notes, and missing segmentations.
* **Solution:** Custom Pandas scripts were implemented to normalize brand names, convert data types, and extract specific fragrance notes from unstructured text strings.

### 2. UI/UX Design ("Dark Luxury")
Standard analytical dashboards often lack aesthetic appeal. This project adopted a **"Dark Luxury"** philosophy:
* **Custom CSS:** Injected code to force a dark, high-contrast theme suitable for a premium industry.
* **Typography:** Integration of *Cormorant Garamond* (headers) and *Montserrat* (body) to reflect the elegance of high-end perfume labeling.
* **UX Fixes:** Overriding default Streamlit elements (like dropdown backgrounds) to ensure visual consistency.

### 3. Visualization Logic
* **Tools:** Plotly Graph Objects for high-fidelity interactive charts.
* **Technical Challenge:** Ensuring accurate scaling for global market data. Early iterations struggled with plotting large datasets, occasionally misinterpreting index positions as data values.
* **Final Solution (v145):** The codebase now uses explicit value extraction (`Series.values` and `Series.index`) to guarantee mathematical accuracy, correctly displaying high-volume data (e.g., mass-market brands with 900+ releases) without truncation or indexing errors.

---
## 📊 Data Analysis & Market Insights

By visualizing over 78,000 records, several distinct patterns in the global fragrance market emerged. Below is a breakdown of the key findings derived from the dashboard charts:

### 1. The Volume vs. Prestige Paradox (Top Brands Chart)
The "Top 15 Brands" chart reveals a counter-intuitive insight: **High recognition does not equal high volume.**
* **Finding:** The list is dominated by catalog and direct-sales brands (e.g., *Avon, Oriflame, Faberlic*), which operate on a "Fast Perfumery" model, releasing dozens of scents annually.
* **Contrast:** Luxury fashion houses (like *Chanel* or *Dior*) appear much lower on the volume scale, confirming their strategy of scarcity and exclusivity over mass saturation.

### 2. The "Fast Fashion" of Fragrance (Timeline Chart)
The "Launch History" chart depicts a massive, exponential spike in releases starting around 2000-2010.
* **Insight:** This correlates with two major industry phenomena:
    1.  **The Flanker Strategy:** Brands releasing multiple variations of a bestseller (e.g., *Black Opium*, *Black Opium Neon*, *Black Opium Extreme*) to capture shelf space.
    2.  **Niche Boom:** The explosion of independent artisan perfumery, flooding the market with experimental scents.

### 3. Olfactory Conservatism vs. Trends (Families Chart)
Despite the rise of niche perfumery, the global market remains conservative.
* **Dominance:** The **"Floral"** family is the undisputed hegemon, accounting for the vast majority of releases. It is the "safe bet" for mass-market profitability.
* **Trend:** However, the high rank of **"Amber" (Oriental)** and **"Woody"** families suggests a shifting consumer preference towards unisex, warmer, and more complex profiles in the modern era.

### 4. Semantic Branding (Word Cloud Analysis)
Analyzing the most frequent words in perfume names reveals marketing psychology.
* **Findings:** Keywords like **"Love," "Night," "Blue," "Rose,"** and **"Gold"** dominate.
* **Conclusion:** Brands prioritize emotional triggers (Romance, Mystery) and associations with luxury materials (Gold) over descriptive ingredient names, except for "Rose" and "Oud," which have strong standalone marketing power.

### 5. Case Study: Tom Ford (Micro-Analysis)
Using the "Brand Analysis" tab to isolate *Tom Ford* reveals a different DNA than the global average.
* **Differentiation:** Unlike the global "Floral" dominance, Tom Ford's portfolio leans heavily into **"Woody"** and **"Spicy"** segments.
* **Strategy:** This confirms the brand's positioning as a disruptor in the "High-End / Private Blend" sector, targeting a customer looking for bold, non-traditional compositions.


---

## 🛠️ Tech Stack

* **Language:** Python 3.9
* **Frontend:** Streamlit (Customized)
* **Data Manipulation:** Pandas, NumPy, Collections
* **Visualization:** Plotly Graph Objects
* **Deployment:** Hugging Face Spaces (Dockerized environment)

---

## 🚀 How to Run Locally

1.  Clone the repository:
    ```bash
    git clone [https://github.com/MagdalenaRomaniecka/Aromo-Market-Intelligence.git](https://github.com/MagdalenaRomaniecka/Aromo-Market-Intelligence.git)
    ```
2.  Install dependencies:
    ```bash
    pip install streamlit pandas plotly
    ```
3.  Run the application:
    ```bash
    streamlit run app.py
    ```

---

*Developed by Magdalena Romaniecka © 2026*

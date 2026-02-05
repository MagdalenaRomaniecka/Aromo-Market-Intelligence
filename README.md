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

## 📊 Key Market Insights

Based on the analysis of the full dataset (78k+ records):

1.  **Mass-Market Volume:** In terms of sheer volume, the market is dominated by catalog and mass-market brands (Avon, Oriflame, Faberlic). These entities release hundreds of fragrances annually, vastly outpacng luxury fashion houses.
2.  **The Reign of Floral:** The "Floral" family is the absolute global leader, serving as the foundation for the majority of compositions across both feminine and unisex segments.
3.  **The 21st Century Boom:** The "Activity Timeline" reveals an exponential increase in perfume launches post-2000. This correlates with the rise of niche perfumery and the "fast fashion" phenomenon entering the fragrance world.
4.  **Brand DNA:** The analysis successfully isolates brand signatures. For example, Middle Eastern brands show a heavy reliance on Oud and Amber, whereas classic European houses (like Chanel) maintain a strong identity built around Jasmine, Rose, and Aldehydes.

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

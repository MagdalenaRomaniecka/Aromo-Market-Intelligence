import pandas as pd
import numpy as np

def clean_data(input_file, output_file):
    """
    Reads raw perfume data, cleans years and olfactory families, 
    and exports a production-ready CSV.
    """
    print("🔄 Loading raw data...")
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.")
        return

    # 1. Clean 'Year' column
    # Convert to numeric, turn 0 into NaN, remove rows without a year
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['year'] = df['year'].replace(0, np.nan)
    df_clean = df.dropna(subset=['year'])
    df_clean['year'] = df_clean['year'].astype(int)

    # 2. Clean 'Families' column
    # Fill missing values with 'Unclassified'
    df_clean['families'] = df_clean['families'].fillna('Unclassified')
    
    # 3. Standardize 'Brand' names
    # Title case and remove trailing spaces
    df_clean['brand'] = df_clean['brand'].astype(str).str.strip().str.title()

    print(f"✅ Data cleaned successfully! Saved {len(df_clean)} rows to '{output_file}'.")
    df_clean.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Ensure your source file is named 'aromo_english.csv'
    clean_data('aromo_english.csv', 'aromo_cleaned.csv')
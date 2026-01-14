import pandas as pd
from sentence_transformers import SentenceTransformer
import pickle
import os

# --- CONFIGURATION ---
INPUT_FILE = 'aromo_english.csv'
OUTPUT_MODEL = 'aromo_embeddings.pkl'

def generate_embeddings():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] Input file {INPUT_FILE} not found. Run pipeline first.")
        return

    print("[INFO] Loading dataset...")
    df = pd.read_csv(INPUT_FILE)
    df = df.fillna('')

    # Create a "Soup" of text for the AI to understand the context
    # Combining Brand, Name, Family, Type and Notes into one string
    print("[INFO] Preprocessing text data...")
    df['semantic_text'] = (
        df['brand'] + " " + 
        df['name'] + " " + 
        df['families'] + " " + 
        df['type'] + " " + 
        df['top_notes']
    )
    
    corpus = df['semantic_text'].tolist()
    
    print("[INFO] Loading Sentence-Transformer model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print(f"[INFO] Generating embeddings for {len(corpus)} items. This may take a while...")
    embeddings = model.encode(corpus, show_progress_bar=True)
    
    print(f"[INFO] Saving embeddings to {OUTPUT_MODEL}...")
    with open(OUTPUT_MODEL, 'wb') as f:
        pickle.dump(embeddings, f)
        
    print("[SUCCESS] AI Engine is ready.")

if __name__ == "__main__":
    generate_embeddings()
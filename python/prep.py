import pandas as pd
import ast
import re
from collections import defaultdict
import pickle
import os

# --- Configuration ---
RAW_DATA_FILE = 'RAW_recipes.csv'
INDEX_FILE = 'inverted_index.pkl'
DATA_FILE = 'recipes_indexed.csv'

# --- Persistence Functions ---
def save_index(index_dict, filename):
    """Saves the Python dictionary index to a file using pickle."""
    with open(filename, 'wb') as f:
        pickle.dump(index_dict, f)
    print(f"✅ Inverted Index saved to {filename}")

# Note: The load_index function will only be used in the 'prep.py' script.

# Data Cleaning and Indexing 
def normalize_ingredient(ingredient_list):
    """Cleans and tokenizes raw ingredients list."""
    cleaned_ingredients = set()
    for item in ingredient_list:
        item = item.lower()
        # Simplified cleaning: removing numbers, units, and punctuation
        item = re.sub(r'[^a-z\s]', '', item).strip()
        if item.endswith('s'):
            item = item[:-1]
        
        if len(item) > 2:
            cleaned_ingredients.add(item)
    return cleaned_ingredients

def build_inverted_index(df):
    """Builds the inverted index and prepares the DataFrame."""
    
    # 1. Clean Ingredients
    df['ingredients'] = df['ingredients'].apply(ast.literal_eval)
    df['clean_ingredients'] = df['ingredients'].apply(normalize_ingredient)

    # 2. Build Index
    inverted_index = defaultdict(list)
    
    for _, row in df.iterrows():
        recipe_id = row['id']
        for ingredient in row['clean_ingredients']:
            inverted_index[ingredient].append(recipe_id)
            
    # 3. Prepare DataFrame for quick lookup (Set ID as index and extract calories)
    df = df.set_index('id')
    
    # Extract Calories (first item in the nutrition list) for Constraint Search
    # Note: nutrition column must be converted to list first if it's still a string
    if isinstance(df['nutrition'].iloc[0], str):
        df['nutrition'] = df['nutrition'].apply(ast.literal_eval)
        
    df['calories'] = df['nutrition'].str[0] # The first item is calories

    print(f"Index built successfully. Total unique indexed ingredients: {len(inverted_index)}")
    return dict(inverted_index), df # Convert defaultdict back to standard dict

# --- Main Setup Function ---
def run_indexing_pipeline():
    print(f"--- 1. Loading Raw Data from {RAW_DATA_FILE} ---")
    
    # Load the raw data
    recipes_df = pd.read_csv(RAW_DATA_FILE)
    
    # Run the core indexing process
    inverted_index, processed_df = build_inverted_index(recipes_df)
    
    # 2. SAVE THE FILES (The missing step!)
    print("--- 2. Saving Processed Files ---")
    
    # A. Save the Inverted Index (Dictionary)
    save_index(inverted_index, INDEX_FILE)
    
    # B. Save the Cleaned DataFrame (Set ID as Index)
    processed_df.to_csv(DATA_FILE)
    print(f"Indexed DataFrame saved to {DATA_FILE}")

    print("SETUP COMPLETE. You can now run the search application.")

if __name__ == "__main__":
    run_indexing_pipeline()
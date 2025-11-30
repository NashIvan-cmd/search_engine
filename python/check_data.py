import pandas as pd
import ast

file_path = 'RAW_recipes.csv'
recipes_df = pd.read_csv(file_path)

recipes_df['ingredients'] = recipes_df['ingredients'].apply(ast.literal_eval)
recipes_df['nutrition'] = recipes_df['nutrition'].apply(ast.literal_eval)

print("First 5 recipes loaded: ")
print(recipes_df[['id', 'name', 'ingredients', 'nutrition']].head())
import pandas as pd
import glob

# Step 1: Find all CSV files starting with 'scopus_'
files = glob.glob('scopus_*.csv')

# Step 2: Concatenate the files
combined_df = pd.concat((pd.read_csv(file) for file in files), ignore_index=True)

# Step 3: Write the combined DataFrame to a new CSV file
combined_df.to_csv('combined_scopus.csv', index=False)

print("Concatenation complete. Output saved to 'combined_scopus.csv'")

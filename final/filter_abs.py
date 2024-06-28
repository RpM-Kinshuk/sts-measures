import pandas as pd

# Read the CSV file
df = pd.read_csv('scopus_abs.csv')

# Filter out the records that have "Error fetching content" in the abstract column
filtered_df = df[df['abstract'] != 'Error fetching content']

# Write the filtered records to a new CSV file
filtered_df.to_csv('scopus_abs_filtered.csv', index=False)

print("Filtered records have been saved to 'scopus_abs_filtered.csv'.")

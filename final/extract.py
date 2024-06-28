import httpx
import time
import pandas as pd
import json

# Load the data from the CSV file
df = pd.read_csv('scopus_results.csv')

# df = df.head(1)

# Function to get the abstract using the DOI of the paper
def get_text_content(doi, api_key, max_retries=3, backoff_factor=0.3):
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }
    timeout = httpx.Timeout(30.0, connect=60.0)
    client = httpx.Client(timeout=timeout, headers=headers)
    url = f"https://api.elsevier.com/content/article/doi/{doi}"
    
    for attempt in range(max_retries):
        try:
            response = client.get(url)
            if response.status_code == 200:
                data = response.json()
                abstract = data.get('full-text-retrieval-response', {}).get('coredata', {}).get('dc:description', 'No abstract available')
                return abstract
            else:
                print(f"Error {response.status_code} for DOI: {doi}")
                return 'Error fetching content'
        except httpx.ReadTimeout:
            print(f"Read timeout for DOI: {doi}, attempt {attempt + 1}")
            if attempt < max_retries - 1:
                time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
            else:
                return 'Error fetching content due to timeout'
# Your API key here
API_KEY = '89072218d14bbda5d9acdad8d14bcfbd'

# Extract abstracts
df['abstract'] = df['prism:doi'].apply(lambda x: get_text_content(x, API_KEY) if pd.notna(x) else 'No DOI available')

# Save the dataframe with abstracts
df.to_csv('scopus_results_with_abstracts.csv', index=False)

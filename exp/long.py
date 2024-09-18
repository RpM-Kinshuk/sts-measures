import requests
import pandas as pd
import time
from datetime import datetime

# Your API key here
API_KEY = '89072218d14bbda5d9acdad8d14bcfbd'
HEADERS = {
    'X-ELS-APIKey': API_KEY,
    'Accept': 'application/json'
}

BASE_URL = 'https://api.elsevier.com/content/search/scopus'

# Query parameters
keywords = ['environmental sustainability', 'sustainable development', 'sustainable development goals']
query = ' OR '.join([f'TITLE-ABS-KEY({kw})' for kw in keywords])

# Function to get results for a specific year
def get_results(query, year):
    results = []
    params = {
        'query': query,
        'count': 25,  # Number of results per request, maximum is 25
        'start': 0,
        'pubyear': year
    }
    print(f"Querying publication year: {year}")

    while True:
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        print(f"Request URL: {response.url}")
        print(f"Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.json())  # Print the error message from the API
            break

        data = response.json()
        entries = data.get('search-results', {}).get('entry', [])
        results.extend(entries)

        # Check if there are more results to fetch
        total_results = int(data.get('search-results', {}).get('opensearch:totalResults', 0))
        start_index = int(data.get('search-results', {}).get('opensearch:startIndex', 0))
        items_per_page = int(data.get('search-results', {}).get('opensearch:itemsPerPage', 0))

        if start_index + items_per_page >= total_results:
            break

        # Update the start index for the next request
        params['start'] = start_index + items_per_page
        time.sleep(1)  # To avoid hitting the rate limit

    return results

# Collect results for each year
all_results = []
start_year = 2010
end_year = 2023

for year in range(start_year, end_year + 1):
    print(f"Fetching results for the year {year}")
    results = get_results(query, year)
    all_results.extend(results)
    print(f"Collected {len(results)} records for the year {year}")

# Convert the results to a DataFrame
df = pd.DataFrame(all_results)

# Save the DataFrame to a CSV file
df.to_csv('scopus_results.csv', index=False)
print(f"Saved {len(df)} records to scopus_results.csv")

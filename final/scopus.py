import requests
import pandas as pd
import time

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
years = range(2010, 2012)
results_per_year = 150  # Number of results to fetch per year

def get_results_for_year(year):
    results = []
    params = {
        'query': f'({query}) AND PUBYEAR = {year}',
        'count': 25,  # Number of results per request, maximum is 25
        'start': 0,
        'sort': 'rowTotal'  # Sort results by relevance
    }
    while True:
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        entries = data.get('search-results', {}).get('entry', [])
        results.extend(entries)

        # Check if there are more results to fetch
        total_results = int(data.get('search-results', {}).get('opensearch:totalResults', 0))
        start_index = int(data.get('search-results', {}).get('opensearch:startIndex', 0))
        items_per_page = int(data.get('search-results', {}).get('opensearch:itemsPerPage', 0))

        if start_index + items_per_page >= total_results or len(results) >= results_per_year:
            break

        # Update the start index for the next request
        params['start'] = start_index + items_per_page
        time.sleep(1)  # To avoid hitting the rate limit

    return results[:results_per_year]

# Fetch results for each year
all_results = []
for year in years:
    year_results = get_results_for_year(year)
    all_results.extend(year_results)
    print(f"Fetched {len(year_results)} records for year {year}")

# Convert the results to a DataFrame
df = pd.DataFrame(all_results)

# Save the DataFrame to a CSV file
df.to_csv('scopus_results_by_year.csv', index=False)
print(f"Saved {len(df)} records to scopus_results_by_year.csv")

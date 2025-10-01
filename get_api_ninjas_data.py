import json
import os
import sys
import requests

API_KEY = os.environ.get("API_NINJAS_KEY")
API_URL = 'https://api.api-ninjas.com/v1/country'

def get_country_data(min_pop_thousands=50000, limit=30):
    """
    Fetches country data from API Ninjas Country API.
    """
    if not API_KEY:
        print("Error: API_NINJAS_KEY environment variable not set.")
        sys.exit(1)

    try:
        headers = {'X-Api-Key': API_KEY}
        params = {'min_population': min_pop_thousands, 'limit': limit}
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        if e.response:
            print(f"Response content: {e.response.content}")
        return None

def main():
    country_list = get_country_data(min_pop_thousands=50000)

    if not country_list:
        print("Could not retrieve country data. Exiting.")
        return

    sorted_countries = sorted(country_list, key=lambda x: x.get('population', 0), reverse=True)

    countries_data = []
    for idx, country in enumerate(sorted_countries[:20]):
        population = country.get('population', 0) * 1000
        gdp_nominal_millions = country.get('gdp', 0)
        gdp_ppp_per_capita = country.get('gdp_per_capita', 0)

        # Calculate Total GDP (PPP)
        total_gdp_ppp = (gdp_ppp_per_capita * population) if gdp_ppp_per_capita and population else 0

        gdp_nominal_str = f"${gdp_nominal_millions / 1000000:.2f} Trillion" if gdp_nominal_millions else 'N/A'
        gdp_ppp_str = f"${total_gdp_ppp / 1_000_000_000_000:.2f} Trillion" if total_gdp_ppp else 'N/A'

        countries_data.append({
            'rank': idx + 1,
            'name': country.get('name'),
            'flag': country.get('iso2', '').lower(),
            'population': f"{population:,}",
            'share': 'N/A',
            'gdp_nominal': gdp_nominal_str,
            'gdp_ppp': gdp_ppp_str,
            'link': f'{country.get("name", "").lower().replace(" ", "-")}-population'
        })

    with open('countries_data.json', 'w') as f:
        json.dump(countries_data, f, indent=4)

    print("Successfully created countries_data.json with total GDP (PPP).")

if __name__ == '__main__':
    main()
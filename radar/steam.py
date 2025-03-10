# radar/steam.py
import requests
import json
from .utils import DEFAULT_HEADERS

def fetch_steam_data(steam_id: str) -> dict:
    '''
    Retrieves game data from the Steam API.
    Returns a dictionary containing at least the game name and the initial price in euros.
    '''
    steam_api_url = f'https://store.steampowered.com/api/appdetails?appids={steam_id}'
    response = requests.get(url=steam_api_url, headers=DEFAULT_HEADERS)
    data = json.loads(response.content)[steam_id]['data']
    # Convert the initial price from cents to euros, if available
    if 'price_overview' in data and data['price_overview']:
        data['price_eur'] = data['price_overview']['initial'] / 100
    else:
        data['price_eur'] = None
    return data

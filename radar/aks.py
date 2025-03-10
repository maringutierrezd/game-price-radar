# radar/aks.py
import requests
import json
from bs4 import BeautifulSoup as bs
from .utils import DEFAULT_HEADERS
from .cache_utils import get_cached_aks_id, update_cache

def extract_aks_game_id(steam_name: str) -> str:
    '''
    Scrapes the AllKeyShop page for a given Steam game name to extract the AKS game ID.
    '''
    aks_web_url = f'https://www.allkeyshop.com/blog/buy-{steam_name}-cd-key-compare-prices/'
    response = requests.get(url=aks_web_url, headers=DEFAULT_HEADERS)
    soup = bs(response.content, 'html5lib')
    # According to current structure of an AKS game page, the needed script tag is the fourth (index 3)
    script_tags = soup.findAll('script', type='application/ld+json')
    if len(script_tags) < 4:
        raise ValueError('Unexpected page structure: cannot find the required script tag.')
    json_data = json.loads(script_tags[3].string)
    aks_id = json_data['@id']
    return aks_id

def get_aks_id(steam_name: str) -> str:
    '''
    Retrieves the AKS game ID using the cache if possible; if not, extracts it from the page.
    '''
    aks_id = get_cached_aks_id(steam_name)
    if aks_id:
        return aks_id
    # If not cached, extract and update cache
    aks_id = extract_aks_game_id(steam_name)
    update_cache(steam_name, aks_id)
    return aks_id

def fetch_aks_offers(aks_id: str) -> list:
    '''
    Retrieves offers from AllKeyShop for the given game ID.
    '''
    aks_api_url = (
        f'https://www.allkeyshop.com/blog/wp-admin/admin-ajax.php?'
        f'action=get_offers&product={aks_id}&currency=eur&edition=0&locale=en&use_beta_offers_display=1'
    )
    response = requests.get(url=aks_api_url, headers=DEFAULT_HEADERS)
    data = json.loads(response.content)
    offers = data.get('offers', [])
    return offers

def get_cheapest_steam_price(offers: list) -> float:
    '''
    Determines the cheapest Steam offer from the list of offers.
    Returns the lowest price in euros.
    '''
    # Filter for offers where the platform is Steam
    steam_offers = [offer for offer in offers if offer.get('platform') == 'steam']
    if not steam_offers:
        return None

    # For the given offer, consider both 'priceCard' and 'pricePaypal' prices, as sometimes they differ
    offer = steam_offers[0]
    price_card = offer['price']['eur'].get('priceCard', float('inf'))
    price_paypal = offer['price']['eur'].get('pricePaypal', float('inf'))
    return min(price_card, price_paypal)

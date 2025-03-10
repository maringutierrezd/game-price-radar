# radar/cache_utils.py
import os
import json
import time

CACHE_FILE = 'cache/aks_game_id_cache.json'
CACHE_EXPIRY = 365 * 24 * 60 * 60  # 1 year in seconds

def load_cache() -> dict:
    '''
    Loads the cache from a JSON file if it exists.
    Creates the directory chain if it doesn't exist.
    '''
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache: dict) -> None:
    '''
    Saves the cache dictionary to a JSON file.
    '''
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=4)

def get_cached_aks_id(steam_name: str) -> str:
    '''
    Returns the cached AKS ID for a given Steam game name if available and fresh,
    otherwise returns None.
    '''
    cache = load_cache()
    entry = cache.get(steam_name)
    if entry:
        # Check if cache is still fresh
        if time.time() - entry['timestamp'] < CACHE_EXPIRY:
            return entry['aks_id']
    return None

def update_cache(steam_name: str, aks_id: str) -> None:
    '''
    Updates the cache with a new AKS ID for the given Steam game name.
    '''
    cache = load_cache()
    cache[steam_name] = {
        'aks_id': aks_id,
        'timestamp': time.time()
    }
    save_cache(cache)

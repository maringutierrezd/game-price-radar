# radar.py
from radar import steam, aks

def main():
    # Define the target price threshold (claim) and the Steam app ID
    game_claim = 40.0
    steam_id = '1174180'
    print(f'Steam ID: {steam_id}')

    # Retrieve game data from Steam
    steam_data = steam.fetch_steam_data(steam_id)
    steam_name = steam_data['name']
    steam_price = steam_data['price_eur']
    print(f'Game: {steam_name}')
    print(f'Base/initial price: {steam_price}€')

    # Get the AllKeyShop game ID
    aks_id = aks.extract_aks_game_id(steam_name)
    print(f'AKS Game ID: {aks_id}')

    # Retrieve offers from AllKeyShop and determine the cheapest Steam price
    offers = aks.fetch_aks_offers(aks_id)
    cheapest_price = aks.get_cheapest_steam_price(offers)
    print(f'Cheapest Steam price on AKS: {cheapest_price}€')

    # Compare the cheapest price with the claim
    if cheapest_price is not None and cheapest_price <= game_claim:
        print('Claim met!')
    else:
        print('Claim NOT met')

if __name__ == '__main__':
    main()

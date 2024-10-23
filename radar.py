import requests, json
from bs4 import BeautifulSoup as bs

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3"
}

def main():
    game_claim = 40.0
    steam_id = "1174180"
    print(f"Steam ID: {steam_id}")
    steam_api_url = f"https://store.steampowered.com/api/appdetails?appids={steam_id}"
    steam_api_request = requests.get(url=steam_api_url, headers=DEFAULT_HEADERS)
    # print(steam_api_request)
    steam_api_request_data = json.loads(steam_api_request.content)[steam_id]["data"]
    # print(steam_api_request_json_data[steam_id]["data"]["name"])
    steam_name = steam_api_request_data["name"]
    steam_initial_price = steam_api_request_data["price_overview"]["initial"] / 100
    print(f"Game: {steam_name}")
    print(f"Base/initial price: {steam_initial_price}€")

    aks_web_url = f"https://www.allkeyshop.com/blog/buy-{steam_name}-cd-key-compare-prices/"
    aks_web_request = requests.get(url=aks_web_url, headers=DEFAULT_HEADERS)

    aks_web_soup = bs(aks_web_request.content, "html5lib")
    
    aks_web_script_tag_ID = aks_web_soup.findAll("script", type="application/ld+json")[3]
    # table[3] contains the ID that AKS assigns to the game
    json_data = json.loads(aks_web_script_tag_ID.string)
    aks_id = json_data["@id"]
    print(f"AKS Game ID: {aks_id}")

    aks_api_url = f"https://www.allkeyshop.com/blog/wp-admin/admin-ajax.php?action=get_offers&product={aks_id}&currency=eur&edition=0&locale=en&use_beta_offers_display=1"
    aks_api_request = requests.get(url=aks_api_url, headers=DEFAULT_HEADERS)
    aks_api_request_data = json.loads(aks_api_request.content)
    # print(len(aks_api_request_data))
    # print(aks_api_request_data["offers"])
    aks_offers = aks_api_request_data["offers"]
    aks_cheapest_steam_price_offer = next((offer for offer in aks_offers if offer["platform"] == "steam"), None)
    aks_cheapest_steam_price = min(aks_cheapest_steam_price_offer["price"]["eur"]["priceCard"], aks_cheapest_steam_price_offer["price"]["eur"]["pricePaypal"])
    print(f"Cheapest Steam price on AKS: {aks_cheapest_steam_price}€")
    
    print("Claim met!") if aks_cheapest_steam_price <= game_claim else print("Claim NOT met")



    

if __name__ == "__main__":
    main()

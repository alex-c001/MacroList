import requests
import json
from concurrent.futures import ThreadPoolExecutor

base_ean = "3017620422003"

base_url_nutriscore = "https://world.openfoodfacts.net/api/v2/product/"
base_url_prices_code = "https://prices.openfoodfacts.org/api/v1/products/code/"
base_url_prices = "https://prices.openfoodfacts.org/api/v1/prices/"


def fetch(ean=base_ean):
    with ThreadPoolExecutor(max_workers=2) as executor:
        nutrients_future = executor.submit(requests.get, base_url_nutriscore + ean)
        price_id_future = executor.submit(requests.get, base_url_prices_code + ean)

        nutrients_response = nutrients_future.result()
        price_id = price_id_future.result().json()["id"]

    price_response = requests.get(base_url_prices + str(price_id))

    return nutrients_response, price_response


def respose_processing(nutrients_response, price_response):
    nutrients_data = nutrients_response.json()
    price_data = price_response.json()

    title = nutrients_data.get("product", {}).get("product_name", "N/A")
    price = price_data.get("price", "N/A")
    nutrients = nutrients_data.get("product", {}).get("nutriments", {})
    return title, price, nutrients




if __name__ == "__main__":
    nutrients_resp, price_resp = fetch()
    title, price, nutrients = respose_processing(nutrients_resp, price_resp)
    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Nutrients: {nutrients}")
    #pretty_json = json.dumps(nutrients_resp.json(), indent=4)
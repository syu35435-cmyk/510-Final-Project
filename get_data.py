import os
import csv
import json
import time
import random
import requests

RAW_DATA_DIR = "data/raw/"
OUTPUT_FILE = RAW_DATA_DIR + "products_with_prices.csv"

TARGET_PER_CATEGORY = 100
CATEGORIES = [ "bread", "breakfast-cereals", "sweet-snacks"]
PAGE_SIZE = 100

FIELDNAMES = [
    "category",
    "barcode",
    "product_name",
    "brands",
    "product_quantity",      
    "quantity",              
    "nutriments",
    "nutriscore_grade",
    "nutriscore_numeric",
    "latest_price"
]

def request_product(category, page) -> list[dict]:
    """
        Reqest a page of products from the OpenFoodFacts API
        for the given food category and return a list of 
        dictionary containing products from the API response.
    """
    params = {
        "action": "process",
        "tagtype_0": "categories",
        "tag_contains_0": "contains",
        "tag_0": category,
        "json": 1,
        "page": page,
        "page_size": PAGE_SIZE
    }

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            return r.json().get("products", [])
    except:
        print("Request failed")
        print("Retrying")
        time.sleep(2)

    return []


def request_latest_price(barcode) -> list[float]:
    """
    Query OpenPrices API and return latest price if available.
    """
    url = "https://prices.openfoodfacts.org/api/v1/prices"
    params = {"product_code": barcode}

    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code != 200:
            return None

        data = r.json()
        items = data.get("items", [])

        if len(items) == 0:
            return None

        last_item = items[-1]
        return last_item.get("price")

    except:
        time.sleep(2)

def main() -> None:
    """
    Collects food product data from the OpenFoodFacts API and saves it to a CSV file.
    Data collection stops once the target number of products per category is reached.
    """
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

    seen = set()


    for category in CATEGORIES:
        print("\nCategory:", category)
        count = 0

        for page in range(1, 10):
            if count >= TARGET_PER_CATEGORY:
                break

            products = request_product(category, page)
            if not products:
                break

            for product in products:
                if count >= TARGET_PER_CATEGORY:
                    break

                barcode = product.get("code")
                if not barcode:
                    continue

                barcode = str(barcode)

                price = request_latest_price(barcode)
                if price is None:
                    continue

                row = {
                    "category": category,
                    "barcode": barcode,
                    "product_name": product.get("product_name"),
                    "brands": product.get("brands"),
                    "product_quantity": product.get("product_quantity"),
                    "quantity": product.get("quantity"),
                    "nutriments": json.dumps(product.get("nutriments", {})),
                    "nutriscore_grade": product.get("nutrition_grade_fr"),
                    "nutriscore_numeric": product.get("nutrition_score_fr"),
                    "latest_price": price
                }

                with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                    writer.writerow(row)

                count += 1
                print(f"{count}: {row['product_name']}")

                time.sleep(0.5)


if __name__ == "__main__":
    main()

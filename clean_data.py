import os
import json
import pandas as pd
import re

RAW_DATA_DIR = "data/raw/"
PROCESSED_DIR = "data/processed/"

INPUT_FILE = RAW_DATA_DIR + "products_with_prices.csv"
OUT_CSV = PROCESSED_DIR + "clean_products.csv"
OUT_JSON = PROCESSED_DIR + "clean_products.json"

def load_nutriments(value) -> dict:
    """
    Loads the nutriments value into a dictionary.
    """
    try:
        return json.loads(value)
    except Exception:
        return {}


def get_nutrient(nutriments, nutrient) -> str:
    """
    Get the nutrient from the nutriments dictionary.
    """
    if isinstance(nutriments, dict):
        return nutriments.get(nutrient)
    return None


def main() -> None:
    """
    Clean raw data collected from the API
    Remove duplicates, Drop unneeded rows, 
    Extract needed nutrition data from "nutriments"
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    print("Loading raw CSV...")
    df = pd.read_csv(INPUT_FILE)
    print("Initial rows:", len(df))

    # Strip Strings
    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["brands"] = df["brands"].astype(str).str.strip()
    df["category"] = df["category"].astype(str)
    df["latest_price"] = pd.to_numeric(df["latest_price"], errors="coerce")

    # Remove Duplicates
    df = df.dropna(subset=["barcode", "product_name", "latest_price"])
    df = df.drop_duplicates(subset="barcode")

    # Extract nutrition data from nutriments
    df["nutriments"] = df["nutriments"].apply(load_nutriments)

    df["energy_kcal_100g"] = df["nutriments"].apply(
        lambda n: get_nutrient(n, "energy-kcal_100g")
    )
    df["sugars_100g"] = df["nutriments"].apply(
        lambda n: get_nutrient(n, "sugars_100g")
    )
    df["fat_100g"] = df["nutriments"].apply(
        lambda n: get_nutrient(n, "fat_100g")
    )
    df["salt_100g"] = df["nutriments"].apply(
        lambda n: get_nutrient(n, "salt_100g")
    )

    df["energy_kcal_100g"] = pd.to_numeric(df["energy_kcal_100g"], errors="coerce")
    df["sugars_100g"] = pd.to_numeric(df["sugars_100g"], errors="coerce")
    df["fat_100g"] = pd.to_numeric(df["fat_100g"], errors="coerce")
    df["salt_100g"] = pd.to_numeric(df["salt_100g"], errors="coerce")

    # Clean nutriscore grade data
    df["nutriscore_grade"] = df["nutriscore_grade"].astype(str).str.lower()
    df["nutriscore_grade"] = df["nutriscore_grade"].replace({"nan": None})

    df["nutriscore_numeric"] = pd.to_numeric(
        df["nutriscore_numeric"], errors="coerce"
    )

    # Compute price per 100g (simple loop)
    price_per_100g = []

    for _, row in df.iterrows():
        qty = row["product_quantity"]
        price = row["latest_price"]

        if qty > 0:
            price_per_100g.append(price / (qty / 100))
        else:
            price_per_100g.append(None)

    df["price_per_100g"] = price_per_100g

    # Remove empty prices
    df = df[df["latest_price"] > 0]

    df = df[
        [
            "barcode",
            "product_name",
            "brands",
            "category",
            "latest_price",
            "price_per_100g",
            "energy_kcal_100g",
            "sugars_100g",
            "fat_100g",
            "salt_100g",
            "nutriscore_numeric",
            "nutriscore_grade",
        ]
    ]

    # Save CSV
    df.to_csv(OUT_CSV, index=False)

    print("\nCleaning Complete")
    print("CSV saved to:", OUT_CSV)


if __name__ == "__main__":
    main()
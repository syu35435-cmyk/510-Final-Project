import pandas as pd

DIR = "data/processed/"
INPUT_FILE = "data/processed/clean_products.csv"


def main() -> None:
    """
    RUn data analysis on the cleaned data
    The analysis includes health classification using Nutri-Score,
    average pruce by category, healthy vs regular price comparisons, 
    and nutrition value per dollar calculations.
    """
    df = pd.read_csv(INPUT_FILE)

    # Classify healthiness
    df["nutriscore_grade"] = df["nutriscore_grade"].str.lower()

    grades = ["a", "b"]
    df["is_healthy"] = df["nutriscore_grade"].isin(grades)

    # Remove outliers
    filtered = df["price_per_100g"].quantile(0.99)
    df_filtered = df[df["price_per_100g"] <= filtered].copy()

    print("Total products:", len(df_filtered))

    print("\nProducts per category:")
    print(df_filtered["category"].value_counts())

    print("\nHealth status counts by category:")
    print(df_filtered.groupby(["category", "is_healthy"]).size())

    print("NUTRITION PER DOLLAR")

    df_filtered["calories_per_dollar"] = (df_filtered["energy_kcal_100g"] / df_filtered["price_per_100g"])
    df_filtered["sugar_per_dollar"] = (df_filtered["sugars_100g"] / df_filtered["price_per_100g"])
    df_filtered["fat_per_dollar"] = (df_filtered["fat_100g"] / df_filtered["price_per_100g"])
    df_filtered["salt_per_dollar"] = (df_filtered["salt_100g"] / df_filtered["price_per_100g"])

    cols = [ "calories_per_dollar", "sugar_per_dollar", "fat_per_dollar", "salt_per_dollar"]

    for category in df_filtered["category"].unique():
        print("\nCategory:", category)
        print(
            df_filtered[df_filtered["category"] == category][cols].mean()
        )


if __name__ == "__main__":
    main()

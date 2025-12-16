import pandas as pd
import matplotlib.pyplot as plt

PROCESSED_DATA_DIR = "data/processed/"

def main() -> None:
    """
    Generate visualizations for food price and nutrition data.
    """

    df = pd.read_csv(PROCESSED_DATA_DIR + "clean_products.csv")

    df["nutriscore_grade"] = df["nutriscore_grade"].str.lower()

    grades = ["a", "b"]
    df["is_healthy"] = df["nutriscore_grade"].isin(grades)

    # Remove outliers
    filtered = df["price_per_100g"].quantile(0.99)
    df = df[df["price_per_100g"] <= filtered].copy()

    # Average price per 100g by NutriScore grade
    for category in df["category"].unique():
        avg_grade_price = df[df["category"] == category].groupby("nutriscore_grade")["price_per_100g"].mean()

        grades = avg_grade_price.index
        prices = avg_grade_price.values

        plt.bar(grades, prices)
        plt.title("Average Price per 100g(" + category + ")")
        plt.xlabel("NutriScore")
        plt.ylabel("Average price per 100g")
        plt.show()

    # Calories per dollar
    df["calories_per_dollar"] = df["energy_kcal_100g"] / df["price_per_100g"]

    calorie_data = df.groupby(["category", "is_healthy"])["calories_per_dollar"].mean()
    calorie_data = calorie_data.unstack()

    calorie_data.plot(kind="bar")
    plt.title("Average Calories per Dollar")
    plt.xlabel("Category")
    plt.ylabel("Calories per dollar")
    plt.legend(["NutriScore C–E", "NutriScore A/B"])
    plt.show()

    # Sugar per dollar
    df["sugar_per_dollar"] = df["sugars_100g"] / df["price_per_100g"]

    sugar_data = df.groupby(["category", "is_healthy"])["sugar_per_dollar"].mean()
    sugar_data = sugar_data.unstack()

    sugar_data.plot(kind="bar")
    plt.title("Average Sugar Per Dollar")
    plt.xlabel("Category")
    plt.ylabel("Sugar per dollar")
    plt.legend(["NutriScore C–E", "NutriScore A/B"])
    plt.show()

    # Fat per dollar
    df["fat_per_dollar"] = df["fat_100g"] / df["price_per_100g"]

    fat_data = df.groupby(["category", "is_healthy"])["fat_per_dollar"].mean()
    fat_data = fat_data.unstack()

    fat_data.plot(kind="bar")
    plt.title("Average Fat per Dollar")
    plt.xlabel("Category")
    plt.ylabel("Fat per dollar")
    plt.legend(["NutriScore C–E", "NutriScore A/B"])
    plt.show()

    # Salt per dollar
    df["salt_per_dollar"] = df["salt_100g"] / df["price_per_100g"]

    salt_data = df.groupby(["category", "is_healthy"])["salt_per_dollar"].mean()
    salt_data = salt_data.unstack()

    salt_data.plot(kind="bar")
    plt.title("Average Salt Per Dollar")
    plt.xlabel("Category")
    plt.ylabel("Salt per dollar")
    plt.legend(["NutriScore C–E", "NutriScore A/B"])
    plt.show()

    print("Visualization complete")



if __name__ == "__main__":
    main()

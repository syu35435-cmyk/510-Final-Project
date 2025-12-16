import pandas as pd
import matplotlib.pyplot as plt

PROCESSED_DIR = "data/processed/"
INFILE = PROCESSED_DIR + "clean_products.csv"


def main():
    print("Loading cleaned dataset...")
    df = pd.read_csv(INFILE)

    # Health classification
    df["nutriscore_grade"] = df["nutriscore_grade"].astype(str).str.lower()
    df["is_healthy"] = df["nutriscore_grade"].isin(["a", "b"])

    cutoff = df["price_per_100g"].quantile(0.99)
    df = df[df["price_per_100g"] <= cutoff].copy()

    # Figure 1: Average price per 100g by category
    avg_price = df.groupby("category")["price_per_100g"].mean()
    avg_price.plot(kind="bar")
    plt.ylabel("Average Price per 100g")
    plt.title("Average Price per 100g by Category")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(PROCESSED_DIR + "avg_price_by_category.png")
    plt.close()

    # Figure 2: Price per 100g by health group
    price_health = df.groupby(
        ["category", "is_healthy"]
    )["price_per_100g"].mean().unstack()

    price_health.plot(kind="bar")
    plt.ylabel("Average Price per 100g")
    plt.title("Average Price per 100g by Nutri-Score Group")
    plt.xticks(rotation=0)
    plt.legend(["Nutri-Score C–E", "Nutri-Score A/B"])
    plt.tight_layout()
    plt.savefig(PROCESSED_DIR + "price_by_nutriscore_group.png")
    plt.close()

    # Figure 3: Average price by Nutri-Score grade
    for category in df["category"].unique():
        sub = df[df["category"] == category]
        sub = sub.dropna(subset=["nutriscore_grade"])

        avg_grade_price = sub.groupby(
            "nutriscore_grade"
        )["price_per_100g"].mean()

        avg_grade_price.plot(kind="bar")
        plt.ylabel("Average Price per 100g")
        plt.title(
            "Average Price per 100g by Nutri-Score Grade (" + category + ")"
        )
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(
            PROCESSED_DIR + "avg_price_by_nutriscore_" + category + ".png"
        )
        plt.close()

    df["calories_per_dollar"] = df["energy_kcal_100g"] / df["price_per_100g"]
    df["sugar_per_dollar"] = df["sugars_100g"] / df["price_per_100g"]
    df["fat_per_dollar"] = df["fat_100g"] / df["price_per_100g"]
    df["salt_per_dollar"] = df["salt_100g"] / df["price_per_100g"]

    # Figure 4: Calories per dollar
    cal_data = df.groupby(
        ["category", "is_healthy"]
    )["calories_per_dollar"].mean().unstack()

    cal_data.plot(kind="bar")
    plt.ylabel("Average Calories per Dollar")
    plt.title("Average Calories per Dollar by Nutri-Score Group")
    plt.xticks(rotation=0)
    plt.legend(["Nutri-Score C–E", "Nutri-Score A/B"])
    plt.tight_layout()
    plt.savefig(PROCESSED_DIR + "calories_per_dollar.png")
    plt.close()

    # Figure 5: Sugar per dollar
    sugar_data = df.groupby(
        ["category", "is_healthy"]
    )["sugar_per_dollar"].mean().unstack()

    sugar_data.plot(kind="bar")
    plt.ylabel("Average Sugar per Dollar")
    plt.title("Average Sugar per Dollar by Nutri-Score Group")
    plt.xticks(rotation=0)
    plt.legend(["Nutri-Score C–E", "Nutri-Score A/B"])
    plt.tight_layout()
    plt.savefig(PROCESSED_DIR + "sugar_per_dollar.png")
    plt.close()

    # Figure 6: Fat per dollar
    fat_data = df.groupby(
        ["category", "is_healthy"]
    )["fat_per_dollar"].mean().unstack()

    fat_data.plot(kind="bar")
    plt.ylabel("Average Fat per Dollar")
    plt.title("Average Fat per Dollar by Nutri-Score Group")
    plt.xticks(rotation=0)
    plt.legend(["Nutri-Score C–E", "Nutri-Score A/B"])
    plt.tight_layout()
    plt.savefig(PROCESSED_DIR + "fat_per_dollar.png")
    plt.close()

    # Figure 7: Salt per dollar
    salt_data = df.groupby(
        ["category", "is_healthy"]
    )["salt_per_dollar"].mean().unstack()

    salt_data.plot(kind="bar")
    plt.ylabel("Average Salt per Dollar")
    plt.title("Average Salt per Dollar by Nutri-Score Group")
    plt.xticks(rotation=0)
    plt.legend(["Nutri-Score C–E", "Nutri-Score A/B"])
    plt.tight_layout()
    plt.savefig(PROCESSED_DIR + "salt_per_dollar.png")
    plt.close()

    print("\n===================================")
    print("Visualization Complte")
    print("Figures saved to data/processed/")
    print("===================================")


if __name__ == "__main__":
    main()

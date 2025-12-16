    for category in df_filtered["category"].unique():
        print("\nCategory:", category)
        print(
            df_filtered[df_filtered["category"] == category][cols].mean()
        )
import pandas as pd

# Try loading your CSV
try:
    df = pd.read_csv("Flipkart_Mobiles.csv")
    print("\n✅ CSV Loaded Successfully!\n")
    print(df.head(3))  # Show first 3 rows
    print("\n📋 Column Names:")
    print(df.columns)
except Exception as e:
    print("❌ Error loading CSV:", e)
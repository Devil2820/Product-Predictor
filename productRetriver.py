import pandas as pd
import re

# Load the dataset
df = pd.read_csv("Flipkart_Mobiles.csv")

# Preprocess: lowercase everything for easier matching
df["Brand"] = df["Brand"].str.lower()
df["Model"] = df["Model"].str.lower()
df["Color"] = df["Color"].str.lower()
df["Memory"] = df["Memory"].str.lower()
df["Storage"] = df["Storage"].str.lower()

# --- Helper Functions ---

def extract_price(text):
    match = re.search(r"(?:under|below|less than)\s*₹?\s*(\d+)", text.lower())
    return int(match.group(1)) if match else None

def extract_keywords(text):
    # Remove numbers (like 20000) and common words
    text = text.lower()
    text = re.sub(r"\b\d+\b", "", text)  # remove standalone numbers
    stopwords = ["phone", "under", "mobiles", "mobile", "smartphone", "smart", "best", "buy", "cheap"]
    keywords = [word for word in text.split() if word not in stopwords]
    return keywords
# --- Matching Function ---

def find_matches(user_input):
    max_price = extract_price(user_input)
    keywords = extract_keywords(user_input)

    filtered_df = df.copy()

    # Apply price filter
    if max_price:
        filtered_df = filtered_df[filtered_df["Selling Price"] <= max_price]

    # Combine row fields into a searchable string
    matches = []
    for _, row in filtered_df.iterrows():
        combined = f"{row['Brand']} {row['Model']} {row['Color']} {row['Memory']} {row['Storage']}"
        if all(k in combined for k in keywords):
            matches.append(row)

    return pd.DataFrame(matches)

# --- Main ---

user_input = input("📲 Enter your phone requirement: ")

result = find_matches(user_input)

if result.empty:
    print("\n❌ No matching phones found.")
else:
    print("\n✅ Matching Phones:\n")
    for _, row in result.iterrows():
        print(f"📱 {row['Brand'].title()} {row['Model'].upper()} ({row['Color'].title()})")
        print(f"💾 Memory: {row['Memory']}, Storage: {row['Storage']}")
        print(f"💰 Selling Price: ₹{row['Selling Price']} (Original: ₹{row['Original Price']})")
        print(f"⭐ Rating: {row['Rating']}\n")

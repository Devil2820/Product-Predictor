from flask import Flask, render_template, request, jsonify
import pandas as pd
import re

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("Flipkart_Mobiles.csv")

# Preprocess: lowercase everything for easier matching
df["Brand"] = df["Brand"].str.lower()
df["Model"] = df["Model"].str.lower()
df["Color"] = df["Color"].str.lower()
df["Memory"] = df["Memory"].str.lower()
df["Storage"] = df["Storage"].str.lower()

# Helper Functions
def extract_price(text):
    match = re.search(r"(?:under|below|less than)\s*₹?\s*(\d+)", text.lower())
    return int(match.group(1)) if match else None

def extract_keywords(text):
    text = text.lower()
    text = re.sub(r"\b\d+\b", "", text)
    stopwords = ["phone", "under", "mobiles", "mobile", "smartphone", "smart", "best", "buy", "cheap"]
    keywords = [word for word in text.split() if word not in stopwords and word.strip()]
    return keywords

def find_matches(user_input):
    max_price = extract_price(user_input)
    keywords = extract_keywords(user_input)

    filtered_df = df.copy()

    if max_price:
        filtered_df = filtered_df[filtered_df["Selling Price"] <= max_price]

    matches = []
    for _, row in filtered_df.iterrows():
        combined = f"{row['Brand']} {row['Model']} {row['Color']} {row['Memory']} {row['Storage']}"
        if all(k in combined for k in keywords):
            matches.append(row.to_dict())
    
    return matches

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form.get('phone_requirement', '')
    if not user_input:
        return jsonify({'error': 'Please enter your requirements'}), 400
    
    results = find_matches(user_input)
    return render_template('results.html', results=results, query=user_input)

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.get_json()
    user_input = data.get('phone_requirement', '')
    results = find_matches(user_input)
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)

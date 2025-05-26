import pandas as pd
import requests
from tqdm import tqdm
import sqlite3


def ollama_query(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt
        }
    )
    full_output = ""
    for line in response.iter_lines():
        if line:
            data = line.decode('utf-8')
            full_output += data
    return full_output


# Connect to SQLite Database
conn = sqlite3.connect('../swiss_travel.db')  # Adjust path if necessary

# Load and join data with SQL
query = """
SELECT 
*
FROM hotels h
"""

df = pd.read_sql_query(query, conn)

def generate_hotel_description(row):
    return (f"{row['hotel']} in {row['place_cleaned']} has a rating of {row['rating_cleaned']} stars "
            f"based on {row['review_counter_cleaned']} reviews and costs {row['price_cleaned']} CHF per night.")

df['description'] = df.apply(generate_hotel_description, axis=1)

tqdm.pandas()
df['ollama_summary'] = df['description'].progress_apply(ollama_query)

df.to_csv("hotel_summaries_ollama.csv", index=False)
print("✅ Summaries saved to 'hotel_summaries_ollama.csv'")
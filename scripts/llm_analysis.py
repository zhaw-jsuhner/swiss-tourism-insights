import sqlite3
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from tqdm import tqdm

# Connect to SQLite Database
conn = sqlite3.connect('../swiss_travel.db')  # Adjust the path as needed

# Use top 50 rows
query = """
SELECT 
*
FROM hotels h
LIMIT 50
"""  # Adjust the limit for testing or remove for all rows
df = pd.read_sql_query(query, conn)

# Load BART model
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Create summarization pipeline
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device=-1)  # device=-1 for CPU, 0 for GPU

print("Model and tokenizer loaded. Ready to generate summaries.")

# Enable progress bar for DataFrame operations
tqdm.pandas()

print("Starting summarization...")

# Function to generate a hotel description based on attributes
def generate_description(row):
    if pd.isna(row['hotel']) or pd.isna(row['place']):
        return "No description available."
    prompt = f"""
Create 2-3 sentences that describe the following hotel. The reviews are on Booking.com:
- Hotel name: {row['hotel']}
- Location: {row['place']}
- Price per night: {row['price_cleaned']} CHF
- Rating: {row['rating_cleaned']} stars
- Number of reviews: {row['review_counter_cleaned']}
"""
    result = summarizer(prompt, max_length=60, min_length=20, do_sample=False)
    return result[0]['summary_text']

# Apply the description generation function to each row in the DataFrame
df['description'] = df.progress_apply(generate_description, axis=1)

# Show the results
print(df[['hotel', 'description']].head())

# Save the DataFrame with descriptions
df.to_csv('../data/hotels_summaries.csv', index=False)
print(f"Alle Hotels gespeichert in data/hotels_summaries.csv")
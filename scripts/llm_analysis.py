import sqlite3
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from tqdm import tqdm
import os

# Connect to SQLite Database
conn = sqlite3.connect('../swiss_travel.db')  # Adjust path if necessary

# Load and join data with SQL
query = """
SELECT 
*
FROM hotels h
LIMIT 1
"""
df = pd.read_sql_query(query, conn)

# Load Falcon 7B Instruct model
model_name = "tiiuae/falcon-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")

# Create text-generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto", torch_dtype="auto")

print("Model and tokenizer loaded. Ready to generate summaries.")

# Enable progress bar for DataFrame operations
tqdm.pandas()

print("Starting summarization...")

# Function to generate a hotel description based on attributes
def generate_description(row):
    if pd.isna(row['hotel']) or pd.isna(row['place']):
        return "No description available."
    prompt = f"""
### Instruction:
Create a short, engaging description for the following hotel in 2-3 sentences.

### Hotel Information:
- Hotel name: {row['hotel']}
- Location: {row['place']}
- Price per night: {row['price_cleaned']} CHF
- Rating: {row['rating_cleaned']} stars
- Number of reviews: {row['review_counter_cleaned']}

### Description:
"""
    result = generator(prompt, max_length=150, temperature=0.7, top_p=0.9, do_sample=True, num_return_sequences=1)
    return result[0]['generated_text'].split('### Description:')[-1].strip()

# Apply the description generation function to each row in the DataFrame
df['description'] = df.progress_apply(generate_description, axis=1)

# Show the results
print(df[['hotel', 'description']].head())

# Save the DataFrame with descriptions
# Datenordner sicherstellen
os.makedirs('data', exist_ok=True)

df.to_csv('../data/hotels_summaries.csv', index=False)
print(f"Alle Hotels gespeichert in data/hotels_summaries.csv")

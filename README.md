# Swiss Hotel Data Analysis Dashboard

This project scrapes hotel data from Booking.com, performs statistical and NLP-based analysis, and presents the results in an interactive dashboard.

## 📦 Setup and Workflow

Before starting, install all required Python libraries by running:
```bash
cd /workspaces/swiss-tourism-insights/
pip install -r requirements.txt
```

## 🌐 Step 1: Scrape Hotel Data
Execute the script `scrape_hotels.py` to scrape hotel data from Booking.com.
```bash
cd /workspaces/swiss-tourism-insights/scripts
python scrape_hotels.py
```
This script uses Playwright to fetch dynamic content and stores the data in a structured format for further processing.

## 🗃️ Step 2: Create and Populate the Database
Open and execute the Jupyter Notebook `DB_create.ipynb`.
This notebook:

- Creates an SQLite database (swiss_travel.db).
- Imports the scraped hotel data into the database.
- Prepares the dataset for analysis.
- Enrich the data by merging it with publicly available geographic data from [opendata.swiss](https://opendata.swiss/en/dataset/amtliches-ortschaftenverzeichnis-mit-postleitzahl-und-perimeter)
  This dataset provides official Swiss localities, postal codes, and geographic boundaries.

## 📊 Step 3: Statistical Analysis and Visualization
Run the following Jupyter Notebooks in sequence:

1. `Statistical_analysis.ipynb`  
   Perform statistical exploration and analysis, including price distributions, review counts, and rating insights.

2. `Map.ipynb`  
   Generate interactive maps and heatmaps showing hotel locations and price distributions across Switzerland.

## 🤖 Step 4: LLM-Based Text Analysis
Execute the script `llm_analysis.py` to generate descriptions of each hotel using a Language Model.

- LLM Model Used: **facebook/bart-large-cnn** <br>
  The jupyter notebook `LLM_analysis.ipynb` does further analysis on the generated data.

## 🌐 Step 5: Run the Web Application
Finally, launch the web dashboard to explore the results interactively.
```bash
cd /workspaces/swiss-tourism-insights/app
python app.py
```
Open your browser and navigate to http://localhost:5000 to view the Swiss Hotel Analysis Dashboard.

## 📄 License
This project is for educational and research purposes only. Data scraping from websites must comply with their terms of service.
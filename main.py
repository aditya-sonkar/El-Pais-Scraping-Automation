import sys
import json
import os
import time
import pandas as pd
from translator import translate_articles
from nlp_keyword_analyzer import analyze_titles
from report import generate_report

start_time = time.time()

# Use --parallel flag from terminal to run in parallel mode
PARALLEL_MODE = "--parallel" in sys.argv

# choose scraper
if PARALLEL_MODE:
    from parallel_scraping_controller import run_parallel_scraper
    articles = run_parallel_scraper()
else:
    from scraper import scrape_articles
    articles = scrape_articles()

# translate
translated_data = translate_articles(articles)

# NLP
english_titles_list = [row[1] for row in translated_data]
word_freq = analyze_titles(english_titles_list)

execution_time = round(time.time() - start_time)

# Report
articles_for_report = [
    {"spanish_title": row[0], "english_title": row[1], "content": row[2]}
    for row in translated_data
]

metadata = {
    "website": "El País — Opinion Section",
    "framework": "Selenium + BrowserStack",
    "articles_extracted": len(articles_for_report),
    "translation": "Google Translate API (RapidAPI)",
    "execution_time": f"{execution_time} seconds"
}

generate_report(articles_for_report, word_freq, metadata)

# JSON export
os.makedirs("output", exist_ok=True)
with open("output/data.json", "w", encoding="utf-8") as f:
    json.dump(articles_for_report, f, ensure_ascii=False, indent=2)
print("-> Data saved: output/data.json")

# Excel export
pd.DataFrame(articles_for_report).to_excel("output/articles.xlsx", index=False)
print("-> Data saved: output/articles.xlsx")

print("PROCESS COMPLETED")

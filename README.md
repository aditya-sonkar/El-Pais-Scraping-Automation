# El País Scraping Automation

## Overview
This project is a cloud-enabled Selenium automation framework that validates the El País (Spanish news) Opinion section across multiple browsers and real mobile devices using BrowserStack.

Along with validation, the system extracts article data, translates it to English, performs text analysis, and generates a structured dataset.
The goal is to simulate how QA Automation Engineers verify web applications in real production-like environments.

## Key Objectives
- Verify that the Opinion section loads correctly across platforms
- Demonstrate Selenium Remote WebDriver usage
- Execute parallel cloud tests
- Process real web content
- Generate automated reports

## Features
- Automated website navigation using Selenium 4
- Extraction of the first 5 Opinion articles
- Title and description scraping
- Cover image download
- Spanish → English translation
- Keyword frequency analysis using NLP
- Excel dataset generation
- Parallel execution
- Cross-browser testing on real devices via BrowserStack

## Tech Stack

| Technology | Purpose |
| ---------- | ------- |
| **Python** | Core programming language |
| **Selenium 4** | Browser automation |
| **BrowserStack** | Cloud cross-browser testing |
| **BeautifulSoup** | HTML parsing |
| **Requests** | Image download |
| **RapidAPI (Google Translate)** | Translation API |
| **NLTK** | Text processing |
| **Pandas** | Dataset creation |

## Architecture

**Local Execution**
`Local Machine → Selenium WebDriver → Chrome → Data Extraction → Translation → Analysis → Excel Report`

**Cloud Execution**
`Local Machine → Selenium RemoteWebDriver → BrowserStack Cloud Grid → Windows / macOS / Android / iOS Devices (Parallel)`

### Cross-Browser Environments Tested
- Windows 11 – Chrome
- Windows 10 – Firefox
- macOS – Safari
- Samsung Galaxy (Android)
- iPhone (iOS)

All sessions are recorded and viewable in the BrowserStack Automate dashboard.

## Workflow
1. Open El País Opinion page
2. Collect the first five article links
3. Visit each article
4. Extract title and description
5. Download cover image
6. Translate Spanish content to English
7. Perform keyword analysis
8. Generate dataset
9. Validate across 5 cloud environments in parallel

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/aditya-sonkar/El-Pais-Scraping-Automation.git
cd El-Pais-Scraping-Automation
```

**2. Install dependencies**
```bash
pip install selenium beautifulsoup4 requests python-dotenv nltk pandas openpyxl jinja2
```

**3. API Configuration**
Create a `.env` file in the root directory and inject your private API variables:
```env
RAPIDAPI_KEY=your_key_here
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
```

**4. Download NLP data**
```bash
python -m nltk.downloader punkt
python -m nltk.downloader stopwords
```

## Run the Project

**Local Execution**
```bash
python main.py
```

**BrowserStack Parallel Execution**
```bash
python bs_parallel.py
```

## Output
The project generates:
- Downloaded article images (in the `/images` directory)
- Translated article dataset (`articles.xlsx` & `data.json`)
- NLP keyword analysis
- HTML Web Report (`report.html`)
- BrowserStack session recordings
- Screenshots

## Learning Outcomes & Project Highlights
Through the development of this framework, the following technical competencies were successfully demonstrated:
- **Advanced DOM Navigation:** Bypassing cookie walls and extracting structured data using Selenium WebDriver and BeautifulSoup.
- **Microservices Integration:** Utilizing external APIs (RapidAPI Google Translate) to process and localize scraped text streams.
- **Natural Language Processing:** Implementing NLTK to tokenize, filter, and mathematically analyze the frequency of semantic keywords.
- **Concurrent Engineering:** Drastically reducing execution time by distributing cloud tests across 5 parallel Python threads.
- **Cloud Infrastructure QA:** Validating the web application's stability across distinct OS/Browser combinations dynamically via BrowserStack Remote WebDrivers.

## 👨‍💻 Author
**Aditya Sonkar**  
Final Year Computer Engineering Student | QA Automation & Backend Development

## Disclaimer
This project is created for educational and demonstration purposes only.
No data is stored or redistributed commercially.

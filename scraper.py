import time
import os
import requests
from bs4 import BeautifulSoup
from browser import create_driver

def scrape_articles():

    print("-> Opening browser...")

    driver = create_driver()
    driver.get("https://elpais.com/opinion/")

    # Wait for the page body to be present instead of hard sleeping
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Accept cookies (important or content hidden)
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        )
        cookie_btn.click()
        print("-> Cookies accepted")
    except:
        print("-> No cookie popup or took too long")

    # Page source is now ready for parsing after cookie click or timeout
    pass

    soup = BeautifulSoup(driver.page_source, "html.parser")

    from datetime import date
    today = date.today().strftime("%Y-%m-%d")

    # Get first 5 article links from today
    links = []
    articles = soup.select("article h2 a")

    for a in articles:
        link = a.get("href", "")
        if link.startswith("/"):
            link = "https://elpais.com" + link
        if today in link:  # only include today's articles
            links.append(link)
        if len(links) == 5:
            break

    results = []

    # Visit each article
    for i, link in enumerate(links):

        print(f"\n-> Opening article {i+1} / {len(links)}: {link}")

        driver.get(link)
        
        # Explicitly wait for the article h1 to load (max 10s) instead of hard sleeping
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
        except:
            print("-> Warning: Article h1 took too long or failed to load")

        article = BeautifulSoup(driver.page_source, "html.parser")

        # -------- TITLE --------
        title = article.find("h1").text.strip()
        print(f"-> SPANISH TITLE: {title}")

        # -------- CONTENT --------
        paragraphs = article.find_all("p")
        content = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])
        if content:
            print(f"-> SPANISH CONTENT: {content[:300]}...")
        else:
            print("-> SPANISH CONTENT: [Not available - article may be behind a paywall]")

        # -------- IMAGE EXTRACTION (REAL FIX) --------
        figure = article.find("figure")

        if figure:
            img_tag = figure.find("img")

            if img_tag and img_tag.get("srcset"):

                srcset = img_tag.get("srcset")

                # split responsive images
                sources = srcset.split(",")

                # take highest resolution (last one = 1200w)
                highest_quality_url = sources[-1].strip().split(" ")[0]

                print("-> Downloading image...")
                save_image(highest_quality_url, i)

            else:
                print("Image not found")

        else:
            print("No figure tag found")

        results.append((title, content))

    driver.quit()
    return results


# ---------------- IMAGE DOWNLOADER ----------------

def save_image(url, i):

    os.makedirs("images", exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/145.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Referer": "https://elpais.com/",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            filepath = f"images/cover_{i+1}.jpg"

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"-> Image saved: {filepath}")

        else:
            print(f"-> Image blocked. Status: {response.status_code}")

    except Exception as e:
        print(f"-> Image download failed: {e}")
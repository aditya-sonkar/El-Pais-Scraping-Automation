import time
import os
import requests
from bs4 import BeautifulSoup
from browser import create_driver

def accept_cookies(driver):
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        ).click()
        # No sleep needed after wait
        pass
    except:
        pass


def save_image(url, index):

    if not url:
        return "N/A"

    os.makedirs("images", exist_ok=True)

    filename = f"cover_{index+1}.jpg"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://elpais.com/"
    }

    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            with open(f"images/{filename}", "wb") as f:
                f.write(r.content)
            return filename
    except:
        pass

    return "N/A"


def scrape_single_article(link, index, results):

    print(f"[Thread {index}] Opening browser")

    driver = create_driver()
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
        pass

    accept_cookies(driver)
    # Collection ready
    pass

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # TITLE
    try:
        title = soup.find("h1").text.strip()
    except:
        title = "ERROR"

    # CONTENT
    try:
        paragraphs = soup.find_all("p")
        content = " ".join([p.text.strip() for p in paragraphs])
    except:
        content = "ERROR"

    # IMAGE
    image_filename = "N/A"

    try:
        figure = soup.find("figure")
        if figure:
            img = figure.find("img")
            if img and img.get("srcset"):
                srcset = img.get("srcset")
                image_url = srcset.split(",")[-1].strip().split(" ")[0]
                image_filename = save_image(image_url, index)
    except:
        pass

    driver.quit()

    results[index] = (title, content)

    print(f"[Thread {index}] Done")

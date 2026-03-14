import time
from threading import Thread
from bs4 import BeautifulSoup
from browser import create_driver
from parallel_scraping_executor import scrape_single_article


def run_parallel_scraper():

    print("PARALLEL MODE ENABLED")

    driver = create_driver()
    driver.get("https://elpais.com/opinion/")

    # Wait for the page body to be present instead of hard sleeping
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except:
        pass

    # accept cookies for link collection
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        ).click()
    except:
        pass

    # Collection ready
    pass

    from datetime import datetime
    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = soup.select("article h2 a")
    
    # Get today's date to filter out old articles
    today_stamp = datetime.now().strftime("%Y-%m-%d")

    links = []
    
    for a in articles:
        link = a["href"]
        if link.startswith("/"):
            link = "https://elpais.com" + link
            
        # Only add articles from today
        if f"/{today_stamp}/" in link:
            links.append(link)
            if len(links) == 5:
                break

    driver.quit()

    # parallel execution
    threads = []
    results = [None] * 5

    for i, link in enumerate(links):
        t = Thread(target=scrape_single_article, args=(link, i, results))
        t.start()
        threads.append(t)
        
    print() # Visual gap between opening and done logs

    for t in threads:
        t.join()

    print("All 5 threads finished")
    
    return [r for r in results if r is not None]

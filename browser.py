from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver():

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Silence ChromeDriver debug logs (like "DevTools listening on ws://..." and SSL errors)
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Selenium 4.6+ automatically manages chromedriver — no manual path needed
    driver = webdriver.Chrome(options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver
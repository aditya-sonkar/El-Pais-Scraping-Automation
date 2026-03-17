import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")


def get_driver(cap):

    bstack_options = {
    
        "userName": USERNAME,
        "accessKey": ACCESS_KEY,
        "sessionName": cap.get("name", "ElPais Test"),
        "buildName": "ElPais Automation Assignment - Aditya",
        "source": "selenium-python",
        "debug": True,
        "networkLogs": True,
        "consoleLogs": "info" 
    }
    
    if "browserName" in cap:
        browser = cap["browserName"].lower()
        options = FirefoxOptions() if browser == "firefox" else Options()
        options.set_capability("browserName", cap["browserName"])
        options.set_capability("browserVersion", cap.get("browserVersion", "latest"))
        bstack_options["os"] = cap["os"]
        bstack_options["osVersion"] = cap["osVersion"]

    elif "deviceName" in cap:
        options = Options()
        bstack_options["deviceName"] = cap["deviceName"]
        bstack_options["osVersion"] = cap["osVersion"]
        bstack_options["realMobile"] = "true"

    options.set_capability("bstack:options", bstack_options)

    driver = webdriver.Remote(
        command_executor="https://hub.browserstack.com/wd/hub",
        options=options
    )

    return driver


def mark_session(driver, status, reason=""):
    script = f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status": "{status}", "reason": "{reason}"}}}}'
    try:
        driver.execute_script(script)
    except:
        pass
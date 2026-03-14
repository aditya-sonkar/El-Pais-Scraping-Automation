import time
from threading import Thread, Lock
from selenium.webdriver.common.by import By
from bs_config import get_driver, mark_session

lock = Lock()
results = {}

capabilities = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "11",
        "name": "Win11 Chrome"
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "10",
        "name": "Win10 Firefox"
    },
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "os": "OS X",
        "osVersion": "Monterey",
        "name": "Mac Safari"
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "osVersion": "12.0",
        "name": "Android S22"
    },
    {
        "deviceName": "iPhone 14",
        "osVersion": "16",
        "name": "iPhone 14"
    },
]


def run_test(cap):
    name = cap["name"]
    start = time.time()
    driver = None

    print(f"Starting: {name}")

    try:
        driver = get_driver(cap)
        driver.get("https://elpais.com/opinion/")
        
        # Professional dynamic wait for BrowserStack workers
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            ).click()
            # Wait for cookie banner to disappear instead of hard sleep
            WebDriverWait(driver, 5).until_not(
                EC.presence_of_element_located((By.ID, "didomi-notice-agree-button"))
            )
        except:
            pass

        body = driver.find_element(By.TAG_NAME, "body").text.lower()

        if "opinion" in body or "opinión" in body:
            count = len(driver.find_elements(By.CSS_SELECTOR, "article h2 a"))
            reason = f"{count} articles found"
            mark_session(driver, "passed", reason)
            log(name, "PASS", reason, time.time() - start)
        else:
            mark_session(driver, "failed", "opinion content not found")
            log(name, "FAIL", "content not found", time.time() - start)

    except Exception as e:
        if driver:
            mark_session(driver, "failed", str(e))
        log(name, "FAIL", str(e), time.time() - start)

    finally:
        if driver:
            driver.quit()


def log(name, status, reason, duration):
    tag = "PASS" if status == "PASS" else "FAIL"
    print(f"[{tag}] {name} ({duration:.1f}s) - {reason}")
    with lock:
        results[name] = {"status": status, "reason": reason, "duration": duration}


def print_summary():
    passed = sum(1 for r in results.values() if r["status"] == "PASS")
    failed = len(results) - passed

    print("\n--- Results ---")
    for name, r in results.items():
        print(f"  [{r['status']}] {name} - {r['duration']:.1f}s - {r['reason']}")

    print(f"\n{passed} passed, {failed} failed out of {len(results)} tests\n")


threads = []
for cap in capabilities:
    t = Thread(target=run_test, args=(cap,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print_summary()
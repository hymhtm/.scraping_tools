import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Chrome WebDriver
def setup_chrome_webdriver():
    """
    Setup Chrome WebDriver for local GUI usage
    """
    #chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# WebDriver instancee
driver = setup_chrome_webdriver()

driver.get("https://www.google.com")

time.sleep(5)

driver.quit()


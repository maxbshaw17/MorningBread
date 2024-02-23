from selenium import webdriver
"""
from selenium.webdriver.chrome.options import Options

options = Options()
options.page_load_strategy = "eager"
options.add_argument("--disable-gpu")
"""

driver = webdriver.Chrome()
url = "https://www.investing.com/news/latest-news"
driver.get(url)

print(driver.title)

driver.close()
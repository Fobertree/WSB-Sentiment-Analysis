from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm
import os
import numpy as np
import pandas as pd
import re

"""
--Links--
https://www.selenium.dev/documentation/webdriver/interactions/windows/

"""
# apparently there's a selenium manager

start_time = time.time()

# -- Config -- #
headless_mode = False

website = "https://www.reddit.com/r/wallstreetbets/"
path = r"Chromedriver\chromedriver.exe"

dest_path = "Data"
scrolls = 5

webdriver_service = Service(path)
chrome_options = Options()

if headless_mode:
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")

xpaths = {
    "Post": "//*[contains(@id, 'post-title')]",
    "Comment": "//*[@id='-post-rtjson-content']",
}

# ------------- #
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

driver.set_window_size(1024, 768)
wait = WebDriverWait(driver, 10)

driver.implicitly_wait(10)
driver.get(website)

"""
Class for comment wrapper (unecessary): shreddit-comment
Posts XPATH: //*[contains(@id, "post-title")]/text()
Post comment XPATH: //*[@id="-post-rtjson-content"]/p

Locate comment, store post

"""


def scroll(xpath_type="Post"):
    driver.execute_script(
        "window.scroll(0,document.body.scrollHeight);"
    )  # scroll entire website to load elements
    print(xpaths[xpath_type])
    time.sleep(3)
    wait.until(EC.visibility_of_all_elements_located((By.XPATH, xpaths[xpath_type])))


for _ in range(scrolls):
    scroll()

containers = []
posts = []

time.sleep(10)

containers = driver.find_elements(By.XPATH, "//*[contains(@id, 'post-title')]")

for container in tqdm(containers):
    new_text = re.sub("\,", "", container.text)
    print(new_text)
    posts.append(new_text)

try:
    np.savetxt(
        os.path.join(dest_path, "unlabelled_data.csv"),
        np.array(posts),
        delimiter=",",
        fmt="%s",
        encoding="utf8",
    )
except Exception as e:
    print("AN ERROR HAS OCCURRED IN SAVING TO CSV: ", e)


def scrape_post():
    pass


print(
    f"Scraping finished in {time.time()- start_time:.2f} seconds.\nHere is the list: {posts}.\nNumber of posts scraped: {len(posts)}."
)

input()

driver.quit()

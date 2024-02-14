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
wait = WebDriverWait(driver, 20)

driver.implicitly_wait(10)
driver.get(website)

original_window = driver.current_window_handle

"""
Class for comment wrapper (unecessary): shreddit-comment
Posts XPATH: //*[contains(@id, "post-title")]/text()
Post comment XPATH: //*[@id="-post-rtjson-content"]/p

Locate comment, store post

"""


def scroll(xpath_type="Post", n_scrolls=scrolls):
    driver.execute_script(
        "window.scroll(0,document.body.scrollHeight);"
    )  # scroll entire website to load elements
    print(xpaths[xpath_type])
    time.sleep(n_scrolls)
    try:
        wait.until(
            EC.visibility_of_all_elements_located((By.XPATH, xpaths[xpath_type]))
        )  # doesn't properly work. For now using manual time.sleep()
    except Exception as e:
        print(
            f"ERROR IN SCROLL: {e}.\nParams:\nXpath{xpaths[xpath_type]}\nNum. Scrolls: {scrolls}."
        )


def scrape_post():
    scroll("Comment", 2)

    comment_containers = driver.find_elements(By.XPATH, xpaths["Comment"])
    for container in tqdm(comment_containers):
        new_text = re.sub("\,", "", container.text)
        print(new_text)
        posts.append(new_text)


for _ in range(scrolls):
    scroll()

containers = []
posts = []
post_urls = []

time.sleep(10)

containers = driver.find_elements(By.XPATH, "//*[contains(@id, 'post-title')]")

for container in containers:
    try:
        new_text = re.sub("\,", "", container.text)
        print(new_text)
        posts.append(new_text)
        post_urls.append((container.get_attribute("href"), new_text))
    except Exception as e:
        print(
            "ERROR IN FETCHING POST/POST URL: ",
            new_text,
            "TAG NAME: ",
            container.tag_name,
        )

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

### Begin scraping each post

for i, url_container in enumerate(tqdm(post_urls)):
    url, title = url_container
    n = EC.number_of_windows_to_be(i + 2)
    print(f"Getting new url: {url}")

    driver.switch_to.new_window(driver.window_handles[-1])
    driver.get(url)

    scrape_post()
    driver.close()

    driver.switch_to.window(original_window)

print(
    f"Scraping finished in {time.time()- start_time:.2f} seconds.\nNumber of posts scraped: {len(posts)}."
)

driver.quit()

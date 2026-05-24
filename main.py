import time

from selenium import webdriver

from db import init_db
from scraper import scrapper
from filters import set_filter


def setup_driver():
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = 'eager' 
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    return driver


if __name__ == "__main__":
    init_db()
    driver = setup_driver()
    try:
        driver.get('https://dobro.ru/search?t=vl')
        set_filter(driver)
    except Exception as e:
        print(f"Cайт недоступен: {e}")

    time.sleep(1)
    scrapper(driver)
    driver.quit()
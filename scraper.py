import os
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from collector import volunteer_collector


def scrapper(driver):
    try:
        driver = driver

        wait = WebDriverWait(driver, 15)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "volunteer-card_volunteer__name__RJIdR")))

        links = driver.find_elements(By.CLASS_NAME, "volunteer-card_volunteer__name__RJIdR")

        main_handle = driver.current_window_handle

        for link in links:
            url = link.get_attribute('href')
            link.click()
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])

            volunteer_collector(driver,url)

            driver.close()
            driver.switch_to.window(main_handle)
    except Exception as e:
        print(f"Ошибка при получении списка волонтеров: {e}")

import os
import time

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


load_dotenv()


def set_filter(driver):
    
    driver=driver
    wait = WebDriverWait(driver,10)
    actions = ActionChains(driver)

    try:
        education = wait.until(EC.element_to_be_clickable((By.XPATH, 
                        '//*[@id="react-select-institution_id-input"]')))
        education.clear()
        education.send_keys(os.getenv("EDUCATION") )
        time.sleep(1)
        #Выбираем первый предложенный вариант
        actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        print(f"Невозможно установить учебное заведение: {e}")

    try:
        #Подтверждаем куки
        cookies = driver.find_element(By.XPATH, "//button[text()='Принять']")
        cookies.click()
    except Exception as e:
        print(f"Невозможно подтвердить куки: {e}")

    try:
        #Выбираем город
        location = driver.find_element(By.XPATH, "//input[@placeholder='В каком месте?']")
        location.clear()
        location.send_keys(os.getenv("LOCATION"))
        #Подтверждаем выбор города
        time.sleep(1)
        exact_location = driver.find_element(By.ID, "base-ui-\\:Rhubejd6\\:-0")
        exact_location.click()
    except Exception as e:
        print(f"Невозможно выбрать город: {e}")

    try:
        #Поиск по имени волонтера
        search = driver.find_element(By.XPATH, "//input[@placeholder='Имя, фамилия или ID']")
        search.clear()
        search.send_keys(os.getenv("SEARCH_QUERY"))
        time.sleep(1)
        #Выбираем первое предложенное имя
        if os.getenv("SEARCH_QUERY"):
            name = driver.find_element(By.CSS_SELECTOR, "div#base-ui-\\:R3iubejd6\\:-0")
            name.click()
        #Применяем в случе, если предложенные вырианты не высветились
        #actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        print(f"Невозможно установить поиск по ФИО: {e}")

    try:
        #Выбираем все элементы с выбором диапозона
        RangeSelectors = driver.find_elements(By.CLASS_NAME, "DoubleRangeInputs_input__7_Xqp")
        #Возраст[0,1] Рейтинг[2,3] Рейтинг по городу[4,5]
        min_raiting, max_raiting = (os.getenv("RATING")).split("-")
        #Выбираем минимальный рейтинг
        RangeSelectors[2].clear()
        RangeSelectors[2].send_keys(min_raiting)
        #Выбираем максимальный рейтинг
        RangeSelectors[3].clear()
        RangeSelectors[3].send_keys(max_raiting)

        #Выбираем региональный рейтинг
        min_regional_raiting, max_regionsal_raiting = (os.getenv("REGIONAL_RATING")).split("-")
        #Выбираем минимальный региональный рейтинг
        RangeSelectors[4].clear()
        RangeSelectors[4].send_keys(min_regional_raiting)
        #Выбираем максимальный региональный рейтинг
        RangeSelectors[5].clear()
        RangeSelectors[5].send_keys(max_regionsal_raiting)
    except Exception as e:
        print(f"Невозможно установить рейтинг: {e}")

    try:
        #Развертываем список направлений
        menu = driver.find_element(By.XPATH, "//span[text()='Что интересно?']")
        menu.click()
        #Выбираем список всех направлений
        directions = [item.strip().lower() for item in 
                      os.getenv('DIRECTION', '').split(',') if item.strip()]
        #Находим все кнопки
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "direction-text")))
        directionButtons = driver.find_elements(By.CLASS_NAME, "direction-text")
        
        for direction in directions:
            match direction:
                case "зож":
                    Button=directionButtons[0]
                case "чс":
                    Button=directionButtons[1]
                case "ветераны":
                    Button=directionButtons[2]
                case "дети":
                    Button=directionButtons[3]
                case "спорт":
                    Button=directionButtons[4]
                case "животные":
                    Button=directionButtons[5]
                case "старшее поколение":
                    Button=directionButtons[6]
                case "овз":
                    Button=directionButtons[7]
                case "экология":
                    Button=directionButtons[8]
                case "культура":
                    Button=directionButtons[9]
                case "поиск пропавших"|"поиск":
                    Button=directionButtons[10]
                case "урбанистика":
                    Button=directionButtons[11]
                case "интеллектуальная помощь":
                    Button=directionButtons[12]
                case "права человека"|"права":
                    Button=directionButtons[13]
                case "образование":
                    Button=directionButtons[14]
                case "другое":
                    Button=directionButtons[15]
                case "коронавирус":
                    Button=directionButtons[16]
                case "наука":
                    Button=directionButtons[17]
                case "наставничество":
                    Button=directionButtons[18]
                case "сво":
                    Button=directionButtons[19]
            Button.click()
        menu.click()
        #Применяем фильтры
        driver.find_element(By.XPATH, "//button[.//span[text()='Найти']]").click()

    except Exception as e:
        print(f"Невозможно установить фильтры направлений: {e}")

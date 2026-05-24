from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from db import save_volunteer


def volunteer_collector(driver, link):
    volunteer = {'full_name': None,'birth_date': None,'profile_url': link,
                 'volunteer_id': link.rsplit('/', 1)[-1],'city': None,
                 'organization': None,'social_links': []}
    wait = WebDriverWait(driver,10)

    try:#Не находим имя через wait, иногда странится обновляется и вылетает ошибка
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,"tw\\:block" )))
        name = driver.find_element(By.CLASS_NAME,"tw\\:block" ).text
        volunteer['full_name'] = name
    except Exception as e:
        print(f"Ошибка, страница волонтера заблокирована или отсутствует: {e}")
        return
    
    try:# Находим список полей даты рождения и города
        info = driver.find_elements(By.CSS_SELECTOR, 
            '[class*="tw\\:text-icon-grayed tw\\:lg\\:font-normal tw\\:lg\\:text-inherit"]')
        if len(info) >= 1: 
            volunteer['birth_date'] = info[0].text
        if len(info) >= 2: 
            volunteer['city'] = info[1].text
    except Exception as e:
        print(f"Ошибка при получении города/даты рождения волонтера: {e}")

    try:#Находим ссылки на соц сети волонтера
        social_media = driver.find_elements(By.XPATH, '//a[@rel="noopener noreferrer"]')
        for social_link in social_media:
            volunteer['social_links'].append(social_link.get_attribute('href'))
    except Exception as e:
        print(f"Ошибка при получении социальных сетей волонтера: {e}")

    try:#Находим организацию, на которую работает волонтер
        org = driver.find_elements(By.CSS_SELECTOR, 
            '[class*="tw\\:text-sm tw\\:leading-5 tw\\:font-normal tw\\:text-text-default"]')
        if len(org) > 1:
            volunteer['organization'] = org[-2].text
    except Exception as e:
        print(f"Ошибка при получении волонтерской организации: {e}")

    try:
        save_volunteer(volunteer)
    except Exception as e:
        print(f"Ошибка при экспорте данных: {e}")
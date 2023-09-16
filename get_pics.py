from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import requests
import os
import time
from PIL import Image
from urllib.request import urlopen



def get_pics(URL:str, to_dir:str, type:str='', need_pics:int=200):
    another_page_pics = need_pics
    dir_path = os.path.abspath(os.getcwd())
    with webdriver.Firefox() as driver:
        driver.get(URL)
        driver.implicitly_wait(5)
        try:
            driver.find_element(By.ID, 'onetrust-pc-btn-handler').click()
            driver.find_element(By.CSS_SELECTOR, "button[class='ot-pc-refuse-all-handler']").click()
        except:
            pass

        def save_pics(need_pics, plus_i, type):
            print('-'*8, driver.window_handles)
            try:
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except:
                pass
            plus_i = plus_i - need_pics
            pics = driver.find_elements(By.CSS_SELECTOR, '.landscape, .portrait, .loaded')
            pics_on_page = len(pics)

            cycle_range = pics_on_page if pics_on_page < need_pics else need_pics

            for i in range(cycle_range):
                pic = pics[i].get_attribute('data-src')
                try:
                    rpic = requests.get(pic, stream=True, timeout=10).raw
                    img = Image.open(rpic)
                    if img.height == 1:
                        continue
                    img.save(f'{dir_path}\\{to_dir}\\{type}_{i+plus_i}.png', format='PNG')
                    print(f'{i+plus_i}.png downloaded')
                except BaseException as ex:
                    print(ex)
                    continue

            return pics_on_page

        another_page_pics -= save_pics(need_pics, need_pics, type)

        while another_page_pics > 0:
            nextpage = driver.find_element(By.CSS_SELECTOR, "a[class='pagination__next button floatl pd-y-none-i']")
            nextpage.click()
            another_page_pics -= save_pics(another_page_pics, need_pics, type)



categories = [
    ('https://www.freepik.com/search?format=search&query=0-6+years+old+male+face+live+photo', '0-6 yo', 'male'),
    ('https://www.freepik.com/search?format=search&query=0-6+years+old+female+face+live+photo', '0-6 yo', 'female'),

    ('https://www.freepik.com/search?format=search&query=7-17+years+old+male+face+live+photo', '7-17 yo', 'male'),
    ('https://www.freepik.com/search?format=search&query=7-17+years+old+female+face+live+photo', '7-17 yo', 'female'),

    ('https://www.freepik.com/search?format=search&query=18-50+years+old+male+face+live+photo', '18-50 yo', 'male'),
    ('https://www.freepik.com/search?format=search&query=18-50+years+old+female+face+live+photo', '18-50 yo', 'female'),
    
    ('https://www.freepik.com/search?format=search&query=51-90+years+old+male+face+live+photo', '51-90 yo', 'male'),
    ('https://www.freepik.com/search?format=search&query=51-90+years+old+female+face+live+photo', '51-90 yo', 'female')
]

for url, dir_name, type in categories:
    get_pics(url, dir_name, type)
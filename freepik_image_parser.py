import os
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By


def save_pics(driver, need_pics, plus_i, img_name, save_path):
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

            for i in range(cycle_range+1):
                pic = pics[i].get_attribute('data-src')
                try:
                    rpic = requests.get(pic, stream=True, timeout=10).raw
                    img = Image.open(rpic)
                    if img.height == 1:
                        continue
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    img.save(f'{save_path}\\{img_name}_{i+plus_i}.png', format='PNG')
                    print(f'{i+plus_i}.png downloaded')
                except BaseException as ex:
                    print(ex)
                    continue

            return pics_on_page


def get_pics(driver, URL:str, to_dir:str, img_name:str='', need_pics:int=200):
    another_page_pics = need_pics
    with driver:
        driver.get(URL)
        driver.implicitly_wait(5)
        try:
            driver.find_element(By.ID, 'onetrust-pc-btn-handler').click()
            driver.find_element(By.CSS_SELECTOR, "button[class='ot-pc-refuse-all-handler']").click()
        except:
            pass

        another_page_pics -= save_pics(driver, need_pics, need_pics, img_name, to_dir)

        while another_page_pics > 0:
            nextpage = driver.find_element(By.CSS_SELECTOR, "a[class='pagination__next button floatl pd-y-none-i']")
            nextpage.click()
            another_page_pics -= save_pics(driver, another_page_pics, need_pics, img_name, to_dir)


def main(save_path, categories):
    driver = webdriver.Firefox()

    for url, dir_name, img_name in categories:
        get_pics(driver, url, save_path+dir_name, img_name)


if __name__ == '__main__':
    save_path = os.path.abspath(os.getcwd()) # save to project dir

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

    main(save_path, categories) 

# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.request import urlretrieve
# from bs4 import BeautifulSoup
import os


# get search page
def set_driver():
    driver = webdriver.Safari()
    return driver

# inspect file_path is or not is exists
def make_file(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print("$INFO - File is exist !")

# capture image
def capture_img(src, path, img, num, skip):
    # download img - 1
    urlretrieve(src, path + img + f"_{num-skip}.jpg")
    print(f"$INFO - Download Image -- {num-skip}")


def main():
    # 300 --> 222 images add some NoSuchElement and url 'None' skip images
    # 550 --> 390 images
    limit = 550   
    search_img = 'dog'
    file_path = f'/Users/tony/Desktop/Capture_img/google_{search_img}_img/'

    # inspect file_path is or not is exists
    make_file(file_path)

    driver = set_driver()
    driver.maximize_window()
    # driver.set_page_load_timeout(60)
    driver.get(f"https://www.google.com/search?tbm=isch&as_q={search_img}")
    driver.implicitly_wait(10)
    
    # current scrollHeight
    current_h = driver.execute_script("return document.body.scrollHeight")
    print(f"# document.body.scrollHeight: {current_h}")

    # start spider
    skip = 0
    
    # scroll down the page ≈ 7
    scroll = 0
    load_page = 5

    # store update_h
    update = []
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # avoid being banned by google --> type: <class 'NoneType'>
        time.sleep(5)

        update_h = driver.execute_script("return document.body.scrollHeight")
        print(f"** scrollHeight --> {update_h}")
            
        # scroll down 5 times appear a load button
        if scroll == load_page:
            load_page_css = "#islmp > div > div > div > div.gBPM8 > div.qvfT1 > div.YstHxe > input"
            button = driver.find_element_by_css_selector(load_page_css)
            
            # True or False
            if button.is_enabled():
                button.send_keys(Keys.ENTER)
                print("# load page button is clicked !")
        
        # update_h type: int --> str
        if str(update_h) == "".join(update[-2:-1]):
            break

        update.append(str(update_h))
        print(update[-2:-1])

        scroll += 1
        print(f"** scroll down --> {scroll}")

    n = 's' if scroll> 1 else ''
    print(f"# Total run --> '{scroll}' loop{n} !")

    # limit increase 50 --> skip img ≈ 2
    alpha = 5
    skip_not_find = 4 * alpha + 2 
    for idx in range(1, limit+1+skip_not_find):
        # img_xpath = f"//*[@id='islrg']/div[1]/div[{idx}]/a[1]/div[1]/img"
        img_css_selector = f'#islrg > div.islrc > div:nth-child({idx}) > a.wXeWr.islib.nfEiy > div.bRMDJf.islir > img'
        try:
            img = driver.find_element_by_css_selector(img_css_selector)
            src = img.get_attribute('src')

            # catch img
            capture_img(str(src), file_path, search_img, idx, skip)
            print(type(src))
        
            # download img - 2
            # with open(file_path + search_img + f'_{idx}.png', 'wb') as f:
            #     f.write(src.screenshot_as_png)

            if idx == (limit+1+skip_not_find):
                break

        except (NoSuchElementException, TypeError, ValueError) as e:
            # if catch NoSuchElementException --> statistic {skip_img} total
            # being banned by google --> TypeError: <class 'NoneType'>
                                   # --> ValueError: unknown url type --> 'None'
            skip += 1
            print(f'current skip img: {skip}')
            print("# NoSuchElement or Type Error or ValueError --> ", e)
        
        except TimeoutException as e:
            print("# TimeoutException massage: ", e)

    s = 's' if skip > 1 else ''
    print(f"$INFO - Download Image Complete ! -- Skip {skip} NoSuchElement, TypeError, ValueError Image{s} !")

    # close driver
    driver.quit()

if __name__ == '__main__':
    import time
    s = time.time()
    main()
    t = time.time()
    print(f"*** Capture Image Takes: {(t - s):.2f} Seconds ! ***")


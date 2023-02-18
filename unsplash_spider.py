# from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
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
    # image size --> 640, 1920, 2400, original: 3000x ~ 5000x, ex: 640 x 440, 2400 x 1651
    img_size = 640 
    search_img = 'dog'  # 'cat'
    file_path = f'/Users/tony/Desktop/Capture_img/unsplash_{search_img}_img/'

    # inspect file_path is or not is exists
    make_file(file_path)

    driver = set_driver()
    driver.maximize_window()
    driver.get(f"https://unsplash.com/s/photos/{search_img}")
    driver.implicitly_wait(10)

    current_h = driver.execute_script("return document.body.scrollHeight")
    print(f"# document.body.scrollHeight: {current_h}")

    # start spider
    skip_img = 0

    # scroll 2 times --> search 60 images, 10 times --> 220 images, 
                    #    30 times --> 520 images (20 minutes), 60 times --> 1220 images (44.5 minutes)
    scroll = 60
    for num in range(1, scroll+1):   
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-3000)")

        # wait some time for the -- page load -- 
        time.sleep(5)

        update_h = driver.execute_script("return document.body.scrollHeight")
        print(f"** scrollHeight --> {update_h}")

        current_h = update_h
        print(f"** scroll down --> {num}")

    n = 's' if num > 1 else ''
    print(f"# Total run --> '{num}' loop{n} !")

    # image = soup.select("img.oCCRx")
    # image = driver.find_elements_by_css_selector("img.oCCRx")
    # image = driver.find_elements_by_xpath("img[@class="oCCRx"]")

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    index = 1
    img_res = []
    for res in soup.find_all('a', {"class": "_2Mc8_"}):
        href = res['href']
        # driver.get("https://unsplash.com" + href)

        # button = driver.find_element_by_css_selector('#popover-download-button')
        # print(button.is_enabled())
        # button.click()
        
        # image size --> 640, 1920, 2400, original: 3000x ~ 5000x, ex: 640 x 440, 2400 x 1651
        res_url = "https://unsplash.com" + href + f"/download?force=true&w={img_size}"
        print(res_url, f"## img --> {index}")
        
        img_res.append(res_url)
        index += 1

    img_src = list(set(img_res))
    print("# Capture Image URL: Total --> ", len(img_src))

    try:
        for idx, src in enumerate(img_src, start=1):
            capture_img(src, file_path, search_img, idx, skip_img)

        # download img - 2
        # with open(file_path + search_img + f'_{idx}.png', 'wb') as f:
        #     f.write(src.screenshot_as_png)
        
    except (NoSuchElementException, TypeError) as e:
        # if catch NoSuchElementException --> statistic {skip_img} total
        skip_img += 1
        print(f'current skip img: {skip_img}')
        print(e)

    s = 's' if skip_img > 1 else ''
    print(f"$INFO - Download Image Complete ! -- Skip {skip_img} Image{s} !")

    # close driver
    driver.quit()

if __name__ == '__main__':
    import time
    s = time.time()
    main()
    t = time.time()
    print(f"*** Capture Image Takes: {(t - s):.2f} Seconds ! ***")
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from fake_useragent import UserAgent
import os


print(os.getcwd())
file_path = '/Users/tony/Desktop/Capture_img/unsplash_dog_img/'
try:
    os.makedirs(file_path, exist_ok = True)
except FileExistsError:
    print("*** File is exist ! ***")

limit = 30
search_img = 'dog'
url = f'https://unsplash.com/s/photos/{search_img}'
ua = UserAgent()

# "user-agent": 'Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
headers = {"content-type": "text/html; charset=UTF-8",
           "user-agent": ua.random,
           "Referer": "https://unsplash.com/"}

req = requests.get(url, headers = headers)   # text, content, status_code, headers, encoding
html = req.content
soup = BeautifulSoup(html, 'lxml')

img_res = []
# image size --> original: 3000x ~ 5000x
for res in soup.find_all('a', {"class": "_2Mc8_"}, limit = 30):
    res_url = "https://unsplash.com" + res['href'] +"/download?force=true"
    print(res_url)
    img_res.append(res_url)
img_src = list(set(img_res))
print(len(img_src))

for n, res in enumerate(img_src, start=1):
    urlretrieve(res, file_path + search_img + f"_{n}.jpg")
    print(f"### Capture Image -- {n}")

print("*** Download Image Complete ! ***")


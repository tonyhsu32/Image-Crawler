import requests
from bs4 import BeautifulSoup
import os
import re


print(os.getcwd())
dir_path = '/Users/tony/Desktop/Capture_img/'
os.makedirs(dir_path, exist_ok = True)

search_text = 'C++'
url = f'https://www.google.com/search?q={search_text}'
headers = {"content-type": "text/html; charset=UTF-8",
           "user-agent": 'Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}

req = requests.get(url, headers = headers)   # text, content, status_code, headers, encoding
html = req.content
soup = BeautifulSoup(html, 'lxml')
# print(soup.prettify())

# catch link text, href
for link in soup.find_all('a')[19:-5]:
    s_link = link.get('href')
    if re.search('/search?', s_link) == None:
        if re.search('/imgres?', s_link) == None:
            print(link.text)
            print(f'Search link : {s_link}', end = "\n"*2)
    



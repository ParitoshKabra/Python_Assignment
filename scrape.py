import requests
from bs4 import BeautifulSoup
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}

URL = 'https://m.facebook.com/timeline/app_section/?section_token=100026749267170:2409997254'
r = requests.get(URL, headers=headers)
# print(r.json())
soup = BeautifulSoup(r.content, 'html5lib')
print(soup.prettify())

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

#드라이버를 실행한다.
options = webdriver.ChromeOptions()
options.add_argument('headless')

try:
    driver = webdriver.Chrome('chromedriver_win32\chromedriver.exe',chrome_options=options)
except :
    driver = webdriver.Chrome('/home/ainochi/Desktop/project/HowToFuzzy/Project/04_BusStop_Infomation/chromedriver_linux64/chromedriver',chrome_options=options)
url = "https://m.map.naver.com/bus/lane.nhn?busID=71014"
driver.get(url)

html = driver.page_source
print(html)
soup = BeautifulSoup(html, 'html.parser')
busStop = []
count = 0
num = soup.select(
    '#ct > div > div.busdlst.bus_route_1._busGraph > ul > li > a > div.busmap_txt > span'
)
name = soup.select(
    '#ct > div > div.busdlst.bus_route_1._busGraph > ul > li > a > div.busmap_txt > strong'
)

for item in zip(num, name):
    busStop.append(
        {
            'num': item[0].text,
            'name': item[1].text
        }
    )
data = pd.DataFrame(busStop)
print(data)
data.to_csv('busStop_by68.csv',encoding="euc-kr")
driver.quit()

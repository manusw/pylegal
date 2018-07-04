from selenium import webdriver
from bs4 import BeautifulSoup


driver = webdriver.Chrome('E:/SOFTWARE/chromedriver_win32/chromedriver.exe')
url= "https://www.appearhere.co.uk/spaces/north-kensington-upcycling-store-and-cafe"
driver.maximize_window()
driver.get(url)

content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content,"html.parser")
price=soup.find("select",{"id":"space-prices"})
options = price.find_all("option")
options1=[y.text for y in options]
values = [o.get("value") for o in options]
for x in range(5):
    print( options1[x], values[x].encode('utf8'));
driver.quit()


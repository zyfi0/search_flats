import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


ZILLOW_URL = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.88728233651892%2C%22east%22%3A-122.23248568896484%2C%22south%22%3A37.663131671800414%2C%22west%22%3A-122.63417331103516%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A603045%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D"

headrs = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

response = requests.get(url=ZILLOW_URL, headers=headrs)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")


all_links = []
all_link = soup.find_all(name="a",  class_ = "property-card-link", tabindex = "0")
for link in all_link:
    href = link["href"]
    if href[0] == "h":
        all_links.append(href)
    else:
        all_links.append(f"https://www.zillow.com{href}")


all_address1 = []
all_address = soup.find_all(name = "address")
for adres in all_address:
    all_address1.append(adres.text)
ufedng = all_address1[0]


all_price1 = []
all_price = soup.find_all(name = 'div', class_ = "StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0 bqsBln")
print(all_price)
for price in all_price:
    only_price = price.text.split("+")
    all_price1.append(only_price[0]) 
# print(all_price1)

  


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_driver_path = "C: \development\chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdQ_y9MyIeHYWQZHdDu0lWr0N-9ENJbqD1XtPKzKxfssr3voQ/viewform?usp=sf_link")
time.sleep(1)
for i in range(len(all_links)):   
    quastion1 = driver.find_element(By.XPATH , '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    quastion1.send_keys(all_address1[i])
    quastion2 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    quastion2.send_keys(all_price1[i])
    quastion3 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    quastion3.send_keys(all_links[i])
    button_send = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    button_send.click()
    time.sleep(3)
    continue_send = driver.find_element(By.LINK_TEXT, 'Prześlij kolejną odpowiedź')
    continue_send.click()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time

form_link = "https://docs.google.com/forms/d/e/1FAIpQLSdDhKZSz9NYvnN224gXK7eABsEADHL4xzrMrBG_dBafpUvR2Q/viewform?usp=sf_link"
zillow_link = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
list_add = []
list_price = []
list_links = []

headers = {
   "User-Agent": "Chrome",
    "Accept-Language": "pl-PL"
}

# soup scrap zillow
response = requests.get(zillow_link, headers=headers)
zupka = BeautifulSoup(response.text, "html.parser")

# linki
linki = zupka.select('.list-card-top a')

for link in linki:
    href = link["href"]
    # obejscie na skrocone linki
    if "http" not in href:
        list_links.append(f"https://www.zillow.com{href}")
    else:
        list_links.append(href)

# adresy list-card-price
adresy = zupka.select('.list-card-info address')
list_add = [adr.get_text() for adr in adresy]

# ceny
ceny = zupka.select('.list-card-price')
list_price = [cena.get_text() for cena in ceny]

# selenium fill form
service = Service("C:/Users/mboja/Desktop/chromedriver.exe") #path do Webdrivera
driver = webdriver.Chrome(service=service)

# sheet create click
for n in range(len(list_links)):
    driver.get(form_link)

    time.sleep(2)
    address = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    ling = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    nextb = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    address.send_keys(list_add[n])
    price.send_keys(list_price[n])
    ling.send_keys(list_links[n])
    nextb.click()

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import requests
import time
from pprint import pprint

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url="https://appbrewery.github.io/Zillow-Clone/",headers=header)
data = response.text
soup = BeautifulSoup(data,"html.parser")

all_links_list = []
links = soup.find_all("a",{"class":["StyledPropertyCardDataArea-anchor"]})
for link in links:
    all_links_list.append(link["href"])

price_list = []
prices = soup.find_all("span",{"class":["PropertyCardWrapper__StyledPriceLine"]})
for price in prices:
    rent_price = price.get_text().split("/mo")[0].strip("+ 1 bd")
    price_list.append(rent_price)

address_list = []
addresses = soup.find_all("address",{"data-test":["property-card-addr"]})
for address in addresses:
    new_address = address.get_text().strip("\n ")
    address_list.append(new_address)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)

driver = webdriver.Chrome(options=chrome_options)
for form in range(len(price_list)):
    driver.get(url="https://docs.google.com/forms/d/e/1FAIpQLSe9tEHHCxdCR6yU8Ca6iUc6ibATsAof-AmPo9Kasgb1g9ua0A/viewform")
    time.sleep(2)
    driver_address = driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    driver_price = driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    driver_link = driver_price.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    driver_address.send_keys(address_list[form])
    driver_price.send_keys(price_list[form])
    driver_link.send_keys(all_links_list[form])
    submit_button.click()
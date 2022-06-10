from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from datetime import datetime as dt


class OtoDomScrapper():

    def __init__(self, path: str, city: str, limit: int = None):
        self.DRIVER_PATH = path
        self.city = city
        self.limit = limit
        self.html_houses_list = []

        options = Options()
        options.add_argument("window-size=800,600")
        
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        self.driver.implicitly_wait(10)


    def accept_cookies(self):
        try:
            self.driver.find_element(by=By.ID, value="onetrust-accept-btn-handler").click()
        except ElementClickInterceptedException:
            pass
        time.sleep(5)


    def get_number_of_houses(self):
        # go to otodom page 
        self.driver.get(f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{self.city.lower()}')

        # accept cookies
        try:
            self.driver.find_element(by=By.ID, value="onetrust-accept-btn-handler").click()
        except ElementClickInterceptedException:
            pass
        time.sleep(5)

        # check how many houses are available
        try:
            num = self.driver.find_element(by=By.XPATH, value="//span[@class='css-klxieh e1ia8j2v11']").text
        except NoSuchElementException:
            return None
        


    def create_house_list(self):
        
        houses_limit = self.limit
        if self.limit == None:
            houses_limit = self.get_number_of_houses()

        assert houses_limit != None
        print(houses_limit)
        path = f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{self.city}?limit={int(houses_limit)}'

        print(path)
        self.driver.get(path)
        
        # get links to each house 
        html_list = self.driver.find_elements(by=By.XPATH, value="//a[@class='css-rvjxyq es62z2j14']")
        for item in html_list:
            self.html_houses_list.append(item.get_attribute('href'))
        print(f"list with html links created, {len(self.html_houses_list)}")

    
    def get_house_info(self, path: str):
        self.driver.get(path)

        try:
            title = self.driver.find_element(by=By.CSS_SELECTOR, value='[data-cy="adPageAdTitle"]').text
        except NoSuchElementException:
            title = -1

        try:
            address = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Adres"]').text
        except NoSuchElementException:
            address = -1

        try:
            price = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Cena"]').text
        except NoSuchElementException:
            price = -1

        try:
            price_m2 = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Cena za metr kwadratowy"]').text
        except NoSuchElementException:
            price_m2 = -1

        try:
            area_m2 = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Powierzchnia"]').text.split()[1]
        except NoSuchElementException:
            area_m2 = -1

        try:
            rooms = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Liczba pokoi"]').text.split()[2]
        except NoSuchElementException:
            rooms = -1

        try:
            floor = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Piętro"]').text
        except NoSuchElementException:
            floor = -1

        try:
            outdoors = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Balkon / ogród / taras"]').text.split("\n")[1]
        except NoSuchElementException:
            outdoors = -1

        try:
            parking = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Miejsce parkingowe"]').text.split("\n")[1]
        except NoSuchElementException:
            parking = -1

        try:
            market = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Rynek"]').text.split()[1]
        except NoSuchElementException:
            market = -1

        try:
            build_yr = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Rok budowy"]').text.split()[2]
        except NoSuchElementException:
            build_yr = -1

        try:
            building_type = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Rodzaj zabudowy"]').text.split()[2]
        except NoSuchElementException:
            building_type = -1

        try:
            elevator = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Winda"]').text.split()[1]
        except NoSuchElementException:
            elevator = -1

        try:
            heating_type = self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Ogrzewanie"]').text.split()[1]
        except NoSuchElementException:
            heating_type = -1

        return {
            'title' : title,
            'address' : address,
            'price' : price,
            'price_m2' : price_m2,
            'area_m2' : area_m2,
            'rooms' : rooms,
            'floor' : floor,
            'outdoors' : outdoors,
            'parking' : parking,
            'market' : market,
            'build_yr' : build_yr,
            'building_type' : building_type,
            'elevator' : elevator,
            'heating_type' : heating_type
        }

    
    def get_df(self):
        data = []

        for idx, link in enumerate(self.html_houses_list, start=1):
            print(f"No. {idx} started at {dt.now()}")
            data.append(self.get_house_info(link))
        
        return pd.DataFrame(data)

        
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
        options.add_argument("window-size=1920,1080")
        
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
        control_sum = 0
        self.driver.get(path)

        # title - tytul ogloszenia
        # try:
        #     title = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/header/h1').text
        # except NoSuchElementException:
        #     title = -1
        #     control_sum += 1

        # address
        try:
            address = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/header/div[3]/a').text
        except NoSuchElementException:
            address = -1
            control_sum += 1

        # price - cena 
        try:
            price = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/header/strong').text
        except NoSuchElementException:
            price = -1
            control_sum += 1

        # price per square meter - cena za metr
        try:
            price_m2 = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/header/div[4]').text
        except NoSuchElementException:
            price_m2 = -1
            control_sum += 1

        if control_sum == 3:
            print("record broken ",path)
            return {}

        # square meters - powierzchnia
        try:
            m2 = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/div[1]/div/div[1]/div[2]/div').text
        except NoSuchElementException:
            m2 = -1

        # rooms - pokoje
        try:
            rooms = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/div[1]/div/div[3]/div[2]/div').text
        except NoSuchElementException:
            rooms = -1

        # floor - pietro 
        try:
            floor = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/div[1]/div/div[5]/div[2]/div').text
        except NoSuchElementException:
            floor = -1

        # balkon / ogrod / taras
        try:
            balcony = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/div[1]/div/div[6]/div[2]/div').text
        except NoSuchElementException:
            balcony = -1

        # parking space / garage
        try:
            garage = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/div[1]/div/div[8]/div[2]/div').text
        except NoSuchElementException:
            garage = -1

        # market - rynek - pierwotny / wtorny
        try:
            market = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/div[3]/div/div[1]/div[2]/div').text
        except NoSuchElementException:
            market = -1

        # build_yr - rok budowy
        try:
            build_yr = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/div[3]/div/div[4]/div[2]/div').text
        except NoSuchElementException:
            build_yr = -1

        # rodzaj zabudowy
        try:
            building_type = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/div[3]/div/div[5]/div[2]/div').text
        except NoSuchElementException:
            building_type = -1

        # winda
        try:
            elevator = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/div[3]/div/div[7]/div[2]/div').text
        except NoSuchElementException:
            elevator = -1

        # heating_type
        try:
            heating_type = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div[2]/div[2]/div[1]/div/div[10]/div[2]/div').text
        except NoSuchElementException:
            heating_type = -1

        return {
            # 'title' : title,
            'address' : address,
            'price' : price,
            'price_m2' : price_m2,
            'm2' : m2,
            'rooms' : rooms,
            'floor' : floor,
            'balcony' : balcony,
            'garage' : garage,
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

        
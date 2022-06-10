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
        offers = []
        
        self.driver = webdriver.Chrome(executable_path=path)
        self.driver.implicitly_wait(10)
        self.driver.get(f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{self.city.lower()}')

        time.sleep(3)
        self.driver.find_element(by=By.ID, value="onetrust-accept-btn-handler").click()
        time.sleep(3)


    def accept_cookies(self):
        try:
            self.driver.find_element(by=By.ID, value="onetrust-accept-btn-handler").click()
        except ElementClickInterceptedException:
            pass
        time.sleep(5)


    def get_number_of_pages(self):
        # read number of last page from buttons at the end of the page
        pages = self.driver.find_elements(by=By.CSS_SELECTOR, value='[class="eoupkm71 css-1lc8b1f e11e36i3"]')[-2].text
        return int(pages)


    def get_offers_from_page(self):
        html_on_page = []

        # get list of all houses (not promoted)
        listing = self.driver.find_elements(By.CSS_SELECTOR, value='[data-cy="search.listing"]')[1]
        offers = listing.find_elements(by=By.TAG_NAME, value='li')

        for offer in offers:
            if offer.get_attribute('class') == 'css-p74l73 es62z2j17':
                link = offer.find_element(by=By.CSS_SELECTOR, value='[class="css-rvjxyq es62z2j14"]').get_attribute('href')
                html_on_page.append(link)
                print('+', end='', flush=True)
                time.sleep(.2)
        print()

        return html_on_page


    def get_offers(self):
        offers = []
        pages = self.get_number_of_pages()
        if self.limit != None:
            pages = self.limit

        print(f'-- pages to check: {pages} --', '\n')
    
        for page in range(pages):
            print(f"searching for offers on page {page+1}")
            offers += self.get_offers_from_page()
            time.sleep(2)

            self.driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="następna strona"]').click()
            time.sleep(.2)

        print(f'-- offers: {len(offers)} --\n')
        self.offers = offers
        

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

    
    def create_df(self):
        data = []

        for idx, link in enumerate(self.offers, start=1):
            print(f"Offer No. {idx}\tstarted at {dt.now().strftime('%X')}")
            data.append(self.get_house_info(link))
        
        return pd.DataFrame(data)

        
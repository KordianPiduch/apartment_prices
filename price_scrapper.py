from selenium import webdriver
from selenium.webdriver.common.by import By
import time

DRIVER_PATH = '/Users/kordianpiduch/Downloads/chromedriver'


class OtoDomScrapper():
    def __init__(self, DRIVER_PATH: str, city: str):
        self.DRIVER_PATH = DRIVER_PATH
        self.city = city
        self.html_houses_list = []

        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.implicitly_wait(10)


    def get_number_of_houses(self):
        # go to otodom page 
        self.driver.get(f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{self.city.lower()}')

        # accept cookies
        self.driver.find_element(by=By.ID, value="onetrust-accept-btn-handler").click()
        time.sleep(5)

        # check how many houses are available 
        num = self.driver.find_element(by=By.XPATH, value="//span[@class='css-klxieh e1ia8j2v11']")
        if num.is_displayed():
            # print(num.text)
            return num.text
        return None


    def get_house_list(self):
        houses = self.get_number_of_houses()
        path = f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{self.city}?limit={int(houses)}'

        assert houses != None

        print(path)
        self.driver.get(path)
        
        # get links to each house 
        html_list = self.driver.find_elements(by=By.XPATH, value="//a[@class='css-rvjxyq es62z2j14']")
        for item in html_list[:10]:
            self.html_houses_list.append(item.get_attribute('href'))

    
    def get_house_info(self, path: str):
        self.driver.get(path)

        # TO DO 
        





def main():
    test_link = 'https://www.otodom.pl/pl/oferta/2-pokojowe-mieszkanie-spoldzczielczo-wlasnosciowe-ID4gOX7'

    x = OtoDomScrapper(DRIVER_PATH, 'gdynia')
 
    x.get_house_info(path = test_link)

    

if __name__ == "__main__":
    main()
    














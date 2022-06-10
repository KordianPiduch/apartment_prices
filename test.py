from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('/Users/kordianpiduch/Downloads/chromedriver')


driver.get('https://www.otodom.pl/pl/oferta/2-pokojowe-mieszkanie-spoldzczielczo-wlasnosciowe-ID4gOX7')

rynek = driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Powierzchnia"]')
# adres = driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Piętro"]')
# cena = driver.find_element(by=By.CSS_SELECTOR, value='[aria-label="Winda"]')



print(rynek.text.split()[1])
# print(adres.text)
# print(cena.text)

driver.quit()
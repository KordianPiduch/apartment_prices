from otodom_scraper import OtoDomScrapper

DRIVER_PATH = '/Users/kordianpiduch/Downloads/chromedriver'

ods = OtoDomScrapper(
    path = DRIVER_PATH, 
    city = "Gdynia",
    limit = None)

ods.get_offers()
df = ods.create_df()

df.to_csv('./data/raw/otodom_df.csv')

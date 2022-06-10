from otodom_scraper import OtoDomScrapper

DRIVER_PATH = '/Users/kordianpiduch/Downloads/chromedriver'

ods = OtoDomScrapper(
    path = DRIVER_PATH, 
    city = "Gdynia",
    limit = 10)

# ods.create_house_list()
# test zestaw
ods.html_houses_list = [
    'https://www.otodom.pl/pl/oferta/mieszkanie-gdynia-chylonia-do-zamieszkania-ID4gml5', 
    'https://www.otodom.pl/pl/oferta/prestizowe-mieszkanie-na-osiedlu-fikakowo-w-gdyni-ID4h1Db', 
    'https://www.otodom.pl/pl/oferta/super-lokalizacja-okazja-ID4gRW1', 
    'https://www.otodom.pl/pl/oferta/nowoczesne-mieszaknie-3-pokojowe-okazja-ID4gVpv', 
    'https://www.otodom.pl/pl/oferta/mieszkanie-4-pokojowe-ul-abrahama-ID4h4nt', 
    'https://www.otodom.pl/pl/oferta/3-pokojowe-mieszkanie-po-remoncie-na-grabowku-ID4h6QV', 
    'https://www.otodom.pl/pl/oferta/sprzedam-mieszkanie-gdynia-redlowo-ID4h6Qe', 
    'https://www.otodom.pl/pl/oferta/osiedla-zamek-3-pok-gdynia-pustki-cisowskie-ID4h6PY', 
    'https://www.otodom.pl/pl/oferta/piekne-3-pok-mieszkanie-po-generalnym-remoncie-ID4gk1q', 
    'https://www.otodom.pl/pl/oferta/mieszkanie-37-m-gdynia-ID4gkJh', 
    'https://www.otodom.pl/pl/oferta/dwupokojowe-mieszkanie-w-scislym-centrum-gdyni-ID4h6N5', 
    'https://www.otodom.pl/pl/oferta/maly-kack-2-pokoje-zamkniete-osiedle-ID4h6MY', 
    'https://www.otodom.pl/pl/oferta/m1-dwupokojowe-mieszkanie-z-ogrodem-ID4gxFL']

df = ods.get_df()

df.to_csv("df.csv")


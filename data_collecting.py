from otodom_scraper import OtoDomScrapper

DRIVER_PATH = '/Users/kordianpiduch/Downloads/chromedriver'
RAW_PATH = './data/raw/otodom_df.csv'
city = "Gdynia"
limit = None


def main():
    ods = OtoDomScrapper(path=DRIVER_PATH, city=city, limit=limit)

    ods.get_offers()
    df = ods.create_df()

    # save raw data as csv file
    df.to_csv(RAW_PATH)


if __name__ == '__main__':
    main()

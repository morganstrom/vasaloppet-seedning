from src.scraper import *

VASALOPPET_2022_LAST_PAGE = 121
VASALOPPET_2022_START_LIST_LAST_PAGE = 157
VASALOPPET_2022_EVENT_ID = "VL_9999991678887600000008EZ"

VASALOPPET_2023_LAST_PAGE = 121
VASALOPPET_2023_START_LIST_LAST_PAGE = 152
VASALOPPET_2023_EVENT_ID = "VL_HCH8NDMR2300"

ENGELBREKT_LAST_PAGE = 28

# Results from Moraloppet are available as csv
# https://live.eqtiming.com/64250#result


def get_engelbrekt_2023():
    scraper = EngelbrektScraper(ENGELBREKT_LAST_PAGE)
    df = scraper.paginate()
    df.to_csv("../data/engelbrekt_2023.csv", index=False)


def get_vasaloppet_2022():
    scraper = VasaloppetScraper(VASALOPPET_2022_EVENT_ID, VASALOPPET_2022_LAST_PAGE)
    df = scraper.paginate()
    df.to_csv("../data/vasaloppet_2022.csv", index=False)


def get_vasaloppet_2023():
    scraper = VasaloppetScraper(VASALOPPET_2023_EVENT_ID, VASALOPPET_2023_LAST_PAGE)
    df = scraper.paginate()
    df.to_csv("../data/vasaloppet_2023.csv", index=False)


def get_vasaloppet_2023_startlist():
    scraper = VasaloppetStartlistScraper(
        VASALOPPET_2023_EVENT_ID, VASALOPPET_2023_START_LIST_LAST_PAGE)
    df = scraper.paginate()
    df.to_csv("../data/vasaloppet_2023_startlist.csv", index=False)


def get_vasaloppet_2022_startlist():
    scraper = VasaloppetStartlistScraper(
        VASALOPPET_2022_EVENT_ID, VASALOPPET_2022_START_LIST_LAST_PAGE)
    df = scraper.paginate()
    df.to_csv("../data/vasaloppet_2022_startlist.csv", index=False)


def main():
    get_vasaloppet_2022_startlist()
    get_vasaloppet_2023_startlist()


if __name__ == "__main__":
    main()

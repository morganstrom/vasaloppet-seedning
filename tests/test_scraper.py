from src.scraper import *


def test_vasaloppet_results_to_dataframe():
    # given
    scraper = VasaloppetScraper()
    page = open("resources/vasaloppet.html").read()

    # when
    df = scraper.table_to_dataframe(page)

    # then
    assert df.shape == (25, 5)


def test_vasaloppet_paginate():
    # given
    scraper = VasaloppetScraper("VL_9999991678887600000008EZ", 2)

    # when
    df = scraper.paginate()

    # then
    assert df.shape == (200, 5)


def test_engelbrekt_results_to_dataframe():
    # given
    scraper = EngelbrektScraper()
    page = open("resources/engelbrektsloppet.html").read()

    # when
    df = scraper.table_to_dataframe(page)

    # then
    assert df.shape == (25, 7)


def test_engelbrekt_paginate():
    # given
    scraper = EngelbrektScraper(2)

    # when
    df = scraper.paginate()

    # then
    assert df.shape == (50, 7)


def test_vasaloppet_start_list_to_dataframe():
    # given
    scraper = VasaloppetStartlistScraper()
    page = open("resources/vasaloppet_startlist.html").read()

    # when
    df = scraper.table_to_dataframe(page)
    print(df.head())

    # then
    assert df.shape == (25, 3)


def test_vasaloppet_start_list_paginate():
    # given
    scraper = VasaloppetStartlistScraper("VL_HCH8NDMR2300", 2)

    # when
    df = scraper.paginate()

    # then
    assert df.shape == (200, 3)

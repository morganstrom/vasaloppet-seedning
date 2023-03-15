import time
from src.client import Client


def test_get_page_source():
    # given
    client = Client()
    client.goto_page(
        "https://results.neptron.se/#/engelbrektsloppet_30_45_2023/results?pageSize=25&raceId=102")
    time.sleep(1)

    # when
    source = client.get_page_source()
    client.close()

    # then
    assert "Engelbrektsloppet" in source
    assert "results table row" in source


def test_click_link():
    # given
    client = Client()
    client.goto_page(
        "https://results.neptron.se/#/engelbrektsloppet_30_45_2023/results?pageSize=25&raceId=102")
    time.sleep(1)

    # when
    client.click_link("45km")
    time.sleep(1)

    # then
    client.close()

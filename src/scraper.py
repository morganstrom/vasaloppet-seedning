import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from src.client import Client


class Scraper(object):
    def __init__(self, base_url: str, params: list = None, last_page: int = None):
        self.base_url = base_url
        self.params = params
        self.last_page = last_page

    def table_to_dataframe(self, source: str) -> pd.DataFrame:
        raise NotImplementedError()

    def paginate(self) -> pd.DataFrame:
        raise NotImplementedError()


class VasaloppetScraper(Scraper):
    def __init__(self, event_id: str = None, last_page: int = None):
        super().__init__(
            base_url="https://results.vasaloppet.se/2023/",
            params=[f"event={event_id}", "num_results=100", "pid=list",
                    "ranking=time_finish_brutto", "search%5Bsex%5D=%25", "search%5Bage_class%5D=%25",
                    "search%5Bnation%5D=%25"],
            last_page=last_page)

    def table_to_dataframe(self, source: str) -> pd.DataFrame:
        soup = BeautifulSoup(source, "html.parser")
        name = soup.body.find_all("h4", class_="list-field type-fullname")
        place = soup.body.find_all("div", class_="list-field type-place place-primary numeric")  # By gender
        team = soup.body.find_all("div", class_="list-field type-priority")
        _ = team.pop(0)  # off by one
        age_class = soup.body.find_all("div", class_="list-field type-age_class")
        _ = age_class.pop(0)  # off by one
        time = soup.body.find_all("div", class_="right list-field type-time")
        _ = time.pop(0)
        _ = time.pop(0)  # off by two

        return pd.DataFrame({
            "Name": [entry.a.text for entry in name],
            "Team": [entry.contents[1] for entry in team],
            "Age class": [entry.contents[1] for entry in age_class],
            "Place (gender)": [entry.text for entry in place],
            "Time": [entry.contents[1] for entry in time if entry.contents[0].text == "Finish"]
        })

    def page_url(self, page: int) -> str:
        return f"{self.base_url}?page={page}&{'&'.join(self.params)}"

    def paginate(self) -> pd.DataFrame:
        results = []
        for i in range(1, self.last_page + 1):
            print(f"Fetching page {i}")
            url = self.page_url(i)
            page = requests.get(url).text
            results.append(
                self.table_to_dataframe(page)
            )
            time.sleep(0.5)
        return pd.concat(results).reset_index(drop=True)


class VasaloppetStartlistScraper(Scraper):
    def __init__(self, event_id: str = None, last_page: int = None):
        super().__init__(
            base_url="https://results.vasaloppet.se/2023/",
            params=[f"event={event_id}", "num_results=100", "pid=startlist_list"],
            last_page=last_page
        )

    def table_to_dataframe(self, source: str) -> pd.DataFrame:
        soup = BeautifulSoup(source, "html.parser")
        name = soup.body.find_all("h4", class_="list-field type-fullname")
        age_class = soup.body.find_all("div", class_="list-field type-age_class")
        _ = age_class.pop(0)  # off by one
        fields = soup.body.find_all("div", class_="list-field type-field")
        start_group = [field.contents[1] for field in fields if field.contents[0].text == "Start Group"]
        _ = start_group.pop(0)  # off by one

        return pd.DataFrame({
            "Name": [entry.a.text for entry in name],
            "Age class": [entry.contents[1] for entry in age_class],
            "Start group": start_group
        })

    def page_url(self, page: int) -> str:
        return f"{self.base_url}?page={page}&{'&'.join(self.params)}"

    def paginate(self) -> pd.DataFrame:
        results = []
        for i in range(1, self.last_page + 1):
            print(f"Fetching page {i}")
            url = self.page_url(i)
            page = requests.get(url).text
            results.append(
                self.table_to_dataframe(page)
            )
            time.sleep(0.5)
        return pd.concat(results).reset_index(drop=True)


class EngelbrektScraper(Scraper):
    def __init__(self, last_page: int = None):
        super().__init__(
            base_url="https://results.neptron.se/#/engelbrektsloppet_30_45_2023/results",
            params=["pageSize=25", "raceId=102"],
            last_page=last_page
        )

    def table_to_dataframe(self, source: str) -> pd.DataFrame:
        soup = BeautifulSoup(source, "html.parser")
        results_table = soup.find("div", class_="results table row")
        table_body = results_table.find("tbody")
        rows = table_body.find_all("tr")
        out = []
        for row in rows:
            if not row.find("td", class_="res-status").div.text == "Finished":
                continue
            out.append(
                {
                    "Place (total)": int(row.find("td", class_="res-placeByRace").div.text),
                    "Place (class)": int(row.find("td", class_="res-placeByCategory").div.text),
                    "Category": row.find("td", class_="res-category").div.text,
                    "Start Number": int(row.find("td", class_="res-startNo").div.text),
                    "Name": row.find("td", class_="res-name").div.text,
                    "Team": row.find("td", class_="res-association").div.text,
                    "Time": row.find("td", class_="res-time").div.text
                }
            )
        return pd.DataFrame(out)

    def page_url(self) -> str:
        return f"{self.base_url}?{'&'.join(self.params)}"

    def paginate(self) -> pd.DataFrame:
        client = Client()
        client.goto_page(self.page_url())
        time.sleep(1)
        client.click_link("45km")
        time.sleep(1)
        results = []
        for i in range(self.last_page):
            print(f"Fetching page {i}")
            page = client.get_page_source()
            results.append(
                self.table_to_dataframe(page)
            )
            client.click_link("»")
            time.sleep(2)
        client.close()
        return pd.concat(results).reset_index(drop=True)

import pandas as pd
import numpy as np

from constants import START_GROUPS, SEEDNING_VL_2022


class VasaStartGroup(object):
    def __init__(self, result_df: pd.DataFrame, seeding_table: dict = SEEDNING_VL_2022):
        assert "Name" in result_df.columns, "Name column is missing"
        assert "Time" in result_df.columns, "Time column is missing"
        self.result_df = result_df
        self.seeding_table = pd.DataFrame(seeding_table)
        self.enrich_results()

    def enrich_results(self) -> None:
        self._add_time_in_hours()
        self._add_first_last_name()
        self._add_start_group()

    def _add_time_in_hours(self) -> None:
        """
        Assumes a Time column in the format HH:MM:SS
        """
        tmp = self.result_df.copy()
        tmp[["hours", "minutes", "seconds"]] = self.result_df["Time"].str.split(":", expand=True)
        self.result_df["TimeInHours"] = (
                tmp["hours"].astype(float) +
                tmp["minutes"].astype(float) / 60 +
                tmp["seconds"].astype(float) / (60*60)
        )

    def _add_first_last_name(self) -> None:
        """
        Assumes a Name column in the format Last, First (Country)
        """
        # Splitting Name into Last and First names
        self.result_df[["Last", "First"]] = self.result_df["Name"].str.split(",", expand=True)

        # Stripping any leading or trailing spaces
        self.result_df["First"] = self.result_df["First"].str.strip()

        # Extracting Country and removing the enclosing parentheses
        self.result_df[["First", "Country"]] = self.result_df["First"].str.split("(", expand=True)
        self.result_df["Country"] = self.result_df["Country"].str.replace(")", "", regex=False)

    def _add_start_group(self) -> None:
        """
        Adds a StartGroup column to the results dataframe
        """
        time_limit = (
                self.seeding_table["hours"] +
                self.seeding_table["minutes"] / 60 +
                self.seeding_table["seconds"] / (60 * 60)
        )
        conditions = [
            self.result_df["TimeInHours"] < time_limit.iloc[i]
            for i in range(10)
        ]
        self.result_df["StartGroup"] = np.select(conditions, START_GROUPS[:-1], default=START_GROUPS[-1])

    def merge_on_name(self, other: pd.DataFrame) -> pd.DataFrame:
        """
        Merges the seeding data with the result data on the columns First and Last
        :param other:
        :return:
        """
        pass

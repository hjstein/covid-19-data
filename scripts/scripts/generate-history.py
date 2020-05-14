#  -*- coding: utf-8 -*-

"""Generate full history
"""

import glob
import pandas as pd

tmpdir = "all_versions_exported"

datasets = []

for filename in glob.glob(tmpdir + "/*.csv"):
    print(filename)
    df = pd.read_csv(filename)
    df["as_of"] = filename.split(".")[1].replace("_", ":")

    # df.rename(columns={df.columns[0]: "DATE_OF_INTEREST",
    #                    "CASE_COUNT": "NEW_COVID_CASE_COUNT",
    #                    "HOSPITALIZED_COUNT": "HOSPITALIZED_CASE_COUNT"},
    #           inplace=True)

    df["as_of"] = pd.to_datetime(df["as_of"])
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    cpd = df[["location", "new_cases"]].groupby("location").rolling(window="7D").mean()
    dpd = df[["location", "new_deaths"]].groupby("location").rolling(window="7D").mean()
    rollingperday = cpd.merge(dpd, how="outer", left_index=True, right_index=True)

    rollingperday = rollingperday.rename(columns={"new_cases": "Cases/day, 7 day avg",
                                                  "new_deaths": "Deaths/day, 7 day avg"})

    df = df.merge(rollingperday, how="left", left_on=["location", "date"],right_index=True)

    datasets.append(df)

df = pd.concat(datasets, sort=True)

df.sort_values(["as_of", "date"], inplace=True)

df.to_csv("public/data/history-full.csv")

# File is too large to push to github, so just save data currently being used
df = df[["location", "as_of", "new_cases", "Cases/day, 7 day avg", "new_deaths", "Deaths/day, 7 day avg"]]
df.to_csv("public/data/history.csv")


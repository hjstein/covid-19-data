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

#    df["Cases/day, 7 day avg"] = df["new_cases"].rolling(window="7D").mean()
#    df["Deaths/day, 7 day avg"] = df["new_deaths"].rolling(window="7D").mean()
    datasets.append(df)

df = pd.concat(datasets, sort=True)

df.sort_values(["as_of", "date"], inplace=True)

df.to_csv("public/data/history.csv")

import pandas as pd
from os import listdir
from os.path import join

COLUMN_NAMES = ["Year", "Age Group", "Males", "Females"]
rename_dict = {
    "0-4": "0 to 4 years old",
    "5-9": "5 to 9 years old",
    "10-14": "10 to 14 years old",
    "15-19": "15 to 19 years old",
    "20-24": "20 to 24 years old",
    "25-29": "25 to 29 years old",
    "30-34": "30 to 34 years old",
    "35-39": "35 to 39 years old",
    "40-44": "40 to 44 years old",
    "45-49": "45 to 49 years old",
    "50-54": "50 to 54 years old",
    "55-59": "55 to 59 years old",
    "60-64": "60 to 64 years old",
    "65-69": "65 to 69 years old",
    "70-74": "70 to 74 years old",
    "75-79": "75 to 79 years old",
    "80-84": "80 to 84 years old",
    "85-89": "85 to 89 years old",
    "90-94": "90 to 94 years old",
    "95-99": "95 to 99 years old",
    "100+": "Over 100 years old",
}


def OutputDataFrame(df):
    """Outputs the dataframe fully without truncation"""
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(df)


def CreateDataFrame(path_to_census=r".\Census"):
    """Creates a dataframe using excel tables for every year of the population, adding year column,
    changing Age Group column to more readable one and combining all tables into one"""
    df_main = pd.DataFrame()
    file_paths = [
        join(path_to_census, f) for f in listdir(path_to_census) if f.endswith(".xlsx")
    ]
    all_dfs = []
    for f in file_paths:
        year = "".join(n for n in f if n.isdigit())
        df = pd.read_excel(f, skiprows=1, header=None)
        df.columns = ["Age Group", "Males", "Females"]
        df["Age Group"] = df["Age Group"].replace(rename_dict)
        df.insert(0, "Year", int(year))
        all_dfs.append(df)
    df_main = pd.concat(all_dfs, axis=0, ignore_index=True)
    df_main = df_main[COLUMN_NAMES]
    return df_main


if __name__ == "__main__":
    df = CreateDataFrame()

import pandas as pd
from datasets import DatasetDict
import matplotlib.pyplot as plt 

UNIQUE_PROBLEM_LABEL = "unique_problem_label"
PROBLEM_IDX = "problem_idx"
COMPETITION = "competition"


def create_unique_problem_label_and_return_df(data_dict: dict) -> pd.DataFrame:
  all_data = []
  for competition, dataset in data_dict.items():
    df: pd.DataFrame = dataset["train"].to_pandas()
    df[UNIQUE_PROBLEM_LABEL] = df[PROBLEM_IDX].map(lambda x : f"{competition.replace("_outputs", "")}: {x}") # Apex: 1
    df[COMPETITION] = competition
    all_data.append(df)
  return pd.concat(all_data)


def clean_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
   df[column] = df[column].map(lambda x : x.replace("-", "_"))
   return df

def drop_judge_column_rows(df: pd.DataFrame) -> pd.DataFrame:
  judge_columns = [x for x in df.columns if "judge" in x]
  return df[df[judge_columns].isna().all(axis=1)]

def drop_judge_columns(df:pd.DataFrame) -> pd.DataFrame:
    print("here")
    judge_columns = [x for x in df.columns if "judge" in x]
    return df.drop(judge_columns, axis=1)



def remove_kangaroo_competitions(df: pd.DataFrame) -> pd.DataFrame:
   return df[~df[UNIQUE_PROBLEM_LABEL].str.contains("kangaroo", case=False, na=False)]



def find_missing_value_ratios(df: pd.DataFrame) -> pd.DataFrame:
   return df.isna().mean().sort_values(ascending=False)



def plot_missing(missing_ratio: pd.DataFrame) -> pd.DataFrame:
    (missing_ratio*100).plot.bar()
    plt.ylabel("Missing ratio %")
    plt.title("Mission value ratio per col")
    plt.show()




def prune_missing(df: pd.Dataframe, missing_ratio: pd.DataFrame, threshold: float) -> pd.DataFrame:
  cols_to_keep = []
  for col, ratio in missing_ratio.to_dict().items():
    if ratio<=threshold:
      cols_to_keep.append(col)
  return df[cols_to_keep]

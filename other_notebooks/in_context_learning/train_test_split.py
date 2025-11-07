
import sys
from pathlib import Path

# Add parent of folder A to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from datasets import load_dataset
from math_arena_datasets import problem_datasets_2025
import pandas as pd
import re
from typing import Any
from datasets import DatasetDict
import itertools
from datasets import Dataset, DatasetDict




PROBLEM_TYPE_COL = "problem_type"
def make_test_train_split() -> tuple[pd.DataFrame, pd.DataFrame]:
  data_dict = make_data_dict()
  # Create a dataframe of all of the data

  pruned_dataset_dict = prune_non_category_rows(data_dict)
  full_data_pd = create_dataframe(pruned_dataset_dict)

  train_df = full_data_pd.sample(frac=0.5, random_state=42)
  test_df = full_data_pd.drop(train_df.index)
  print(len(full_data_pd))
  print(f"{len(train_df)=}, {len(test_df)=}")

  return train_df, test_df


def create_dataframe(pruned_dataset_dict):
    frames = []
    for k, dataset in pruned_dataset_dict.items():
      dfs = {split: dataset.to_pandas() for split, dataset in dataset.items()}
      dfs = dfs["train"]
      dfs = dfs[["problem", "problem_type"]]
      frames.append(dfs)
    return pd.concat(frames).reset_index()

def prune_non_category_rows(data_dict):
    n_of_has_problem_type_col = 0
    n_of_has_not_problem_type_col = 0
    datastes_which_has_problem_type = []

    for name, dataset in data_dict.items():
      rows = len(dataset["train"])
      if PROBLEM_TYPE_COL in dataset["train"].column_names:
        n_of_has_problem_type_col += rows
        datastes_which_has_problem_type.append(name)
      else:
        n_of_has_not_problem_type_col+=rows

    pruned_dataset_dict = {
      name: dataset for (name, dataset) in data_dict.items() 
      if name in datastes_which_has_problem_type
  }

    return pruned_dataset_dict

def make_data_dict() -> dict[str, Any]:
    data_dict: dict[str, Any] = {}

    for dataset_name in problem_datasets_2025:
      data_dict[dataset_name] = load_dataset(f"{dataset_name}")
    return data_dict



from typing import Literal
from typing import Any
from datasets import DatasetDict

from datasets import load_dataset


problem_datasets_2025 = [
    "MathArena/apex_2025",
    "MathArena/aime_2025",
    "MathArena/aime_2025_I",
    "MathArena/aime_2025_II",
    "MathArena/hmmt_feb_2025",
    "MathArena/cmimc_2025",
    "MathArena/usamo_2025",
    "MathArena/imo_2025",
    "MathArena/brumo_2025",
    "MathArena/imc_2025",
    "MathArena/kangaroo_2025",
    "MathArena/kangaroo_2025_1_2",
    "MathArena/kangaroo_2025_3_4",
    "MathArena/kangaroo_2025_5_6",
    "MathArena/kangaroo_2025_7_8",
    "MathArena/kangaroo_2025_9_10",
    "MathArena/kangaroo_2025_11_12",
]

output_datasets_2025 = [
    "MathArena/apex_2025_outputs",
    "MathArena/aime_2025_outputs",
    "MathArena/aime_2025_I_outputs",
    "MathArena/aime_2025_II_outputs",
    "MathArena/hmmt_feb_2025_outputs",
    "MathArena/cmimc_2025_outputs",
    "MathArena/usamo_2025_outputs",
    "MathArena/imo_2025_outputs",
    "MathArena/brumo_2025_outputs",
    "MathArena/imc_2025_outputs",
    "MathArena/kangaroo_2025_1-2_outputs",
    "MathArena/kangaroo_2025_3-4_outputs",
    "MathArena/kangaroo_2025_5-6_outputs",
    "MathArena/kangaroo_2025_7-8_outputs",
    "MathArena/kangaroo_2025_9-10_outputs",
    "MathArena/kangaroo_2025_11-12_outputs",
]

categories_2025 = [
    "MathArena/aime_2025",
    "MathArena/hmmt_feb_2025",
    "MathArena/cmimc_2025",
    "MathArena/brumo_2025"
    ]
PROBLEM = "problem"
OUTPUTS = "outputs"


def load_data_dict(table_type: Literal["problem", "outputs"]):
    assert table_type in [PROBLEM, OUTPUTS]
    if table_type == PROBLEM:
        dataset = problem_datasets_2025
    if table_type == OUTPUTS:
        dataset = output_datasets_2025

    data_dict: dict[str, DatasetDict] = {}

    for dataset_name in dataset:
        data_dict[dataset_name] = load_dataset(f"{dataset_name}")
    return data_dict


def get_all_cols_from_data_dict(data_dict: dict[str, DatasetDict]) -> set[str]:
    all_column_names: set[str] = set()
    for name, dataset in data_dict.items():
        cols = dataset["train"].column_names
        all_column_names = all_column_names.union(cols)

    return all_column_names


def pick_competition_element(n: int, d: dict[DatasetDict]) -> tuple[str, DatasetDict]:
    i = 0
    for k, _ in d.items():
        if i == n:
            return k, d[k]
    raise (ValueError(f"{n=} is larger than number of dict eleents"))

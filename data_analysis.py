import pandas as pd
from data_processing_utils import UNIQUE_PROBLEM_LABEL 
CORRECT = "correct"
def create_ten_percentile_group(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(UNIQUE_PROBLEM_LABEL)[CORRECT].mean()
    TEN_PERCENTILE_GROUP = "ten_percentile_group"
    percentiles = pd.qcut(grouped,q=10, labels=False, duplicates="drop") +1
    q_dict = percentiles.to_dict()
    df[TEN_PERCENTILE_GROUP] = df[UNIQUE_PROBLEM_LABEL].map(lambda x : q_dict[x])
    df[TEN_PERCENTILE_GROUP]
    return df


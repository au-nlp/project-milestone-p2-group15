import pandas as pd
from data_processing.data_processing_utils import UNIQUE_PROBLEM_LABEL 
from typing import Literal
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
import itertools


CORRECT = "correct"

MODEL_NAME = "model_name"
PROBLEM_PATH = "data/all_problems_pd/all_problems.csv"
OUTPUTS_PATH = "data/all_answers_pd/all_answers_pruned.csv"


Model_names = Literal['Claude-Sonnet-4.5 (Think)',
 'DeepSeek-v3.1 (Think)',
 'DeepSeek-R1-0528',
 'DeepSeek-v3.2 (Think)',
 'gemini-2.5-pro',
 'GPT-5 (high)',
 'GPT OSS 120B (high)',
 'GPT-5-mini (high)',
 'GPT-5 (High) Agent',
 'GLM 4.6',
 'GLM 4.5',
 'Qwen3-235B-2507-Think',
 'Grok 4 Fast (Reasoning)',
 'Grok 4',
 'Claude-Opus-4.0 (Think)',
 'Claude-3.7-Sonnet (Think)',
 'Claude-3.5-Sonnet',
 'DeepSeek-R1-Distill-14B',
 'DeepSeek-R1-Distill-32B',
 'DeepSeek-R1-Distill-1.5B',
 'DeepSeek-V3',
 'DeepSeek-R1-Distill-70B',
 'DeepSeek-V3-03-24',
 'DeepSeek-R1',
 'Llama-4-Maverick',
 'gemini-2.5-flash (think)',
 'gemini-2.5-pro-05-06',
 'gemini-2.0-pro',
 'gemini-2.0-flash',
 'gemini-2.0-flash-thinking',
 'GPT OSS 20B (high)',
 'o3 (high)',
 'o3-mini (low)',
 'o3-mini (medium)',
 'o4-mini (medium)',
 'o4-mini (high)',
 'o4-mini (low)',
 'o1 (medium)',
 'GPT-5-nano (high)',
 'gpt-4o',
 'o3-mini (high)',
 'GLM 4.5 Air',
 'LIMO',
 's1.1-32B',
 'K2-Think',
 'OpenThinker-32B',
 'Phi-4-reasoning-plus',
 'Qwen3-235B-A22B',
 'QwQ-32B-Preview',
 'Qwen3-30B-A3B',
 'QwQ-32B',
 'Grok 3 Mini (low)',
 'Grok 3 Mini (high)',
 'gemini-2.5-pro*',
 'GLM 4.5V',
 'Qwen3-VL-235B Instruct']

TEN_PERCENTILE_GROUP = "ten_percentile_group"
def create_ten_percentile_group(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(UNIQUE_PROBLEM_LABEL)[CORRECT].mean()
    TEN_PERCENTILE_GROUP = "ten_percentile_group"
    percentiles = pd.qcut(grouped,q=10, labels=False, duplicates="drop") +1
    q_dict = percentiles.to_dict()
    df[TEN_PERCENTILE_GROUP] = df[UNIQUE_PROBLEM_LABEL].map(lambda x : q_dict[x])
    df[TEN_PERCENTILE_GROUP]
    return df




def select_only_single_model_stats(df_outputs, model_name: Model_names) -> pd.DataFrame:
    names = list(df_outputs[MODEL_NAME].unique())
    assert model_name in names
    return df_outputs[df_outputs[MODEL_NAME]==model_name]



PROBLEM_TYPE = 'problem_type'

def count_categories(df_problem: pd.DataFrame) -> pd.DateOffset:
    PROBLEM_TYPE = 'problem_type'
    df_problem = df_problem.copy()
    df_problem = df_problem.dropna(subset=[PROBLEM_TYPE])
    df_problem[PROBLEM_TYPE] = df_problem[PROBLEM_TYPE].map(lambda x : str(x))

    return df_problem[[PROBLEM_TYPE]].reset_index().groupby(PROBLEM_TYPE).count()


def visualize_problem_counts(category_counts: pd.DataFrame) -> None: 
    plt.figure(figsize=(10, 6))
    xs = [x for x in list(category_counts.index)]
    ys = list(x[0] for x in category_counts.values)
    sns.barplot(x=xs, y=ys, palette="Set2")
    plt.title('Problem Categories in the pruned problem dataset', fontsize=16)
    plt.xlabel('Problem Category', fontsize=14)
    plt.ylabel('Number of Occurrences', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show() 



    


def select_only_false(df: pd.DataFrame) -> pd.DataFrame:
    df_new = df.copy()
    falses = df_new[df_new[CORRECT]==False]["unique_problem_label"]
    trues = df_new[df_new[CORRECT] == True]["unique_problem_label"]
    only_false = set(falses).difference(trues)
    df_new_false = df_new[df_new["unique_problem_label"].isin(only_false)]
    mask = ~df_new_false["unique_problem_label"].str.contains("kangaroo", case=False, na=False)
    df_new_false = df_new_false[mask]
    return df_new_false




def select_problem_sample(df_new_false: pd.DataFrame, all_problems: pd.DataFrame) -> pd.DataFrame:
  
  """Here we just try to selct problems it could not answer"""
  problems_it_could_not_anwer = df_new_false["unique_problem_label"].unique()
  df = df_new_false
  difficulty_levels = list(df[TEN_PERCENTILE_GROUP].unique())
  selected_problems = []
  for lvl in difficulty_levels:
    # select a problem with this level 
    selected_problem= df[df[TEN_PERCENTILE_GROUP]==lvl].head(1)
    index = list(selected_problem["unique_problem_label"])[0]
    
    problem = all_problems[all_problems["unique_problem_label"]==index].iloc[0]["problem"]

    selected_problem["problem"] = problem

    selected_problems.append(selected_problem)
    
  return pd.concat(selected_problems)




def select_problem_sample_for_model(model_name: str):
   outputs_df = pd.read_csv("data/all_answers_pd/all_answers_pruned.csv")
   problem_df = pd.read_csv("data/all_problems_pd/all_problems.csv")

   outputs_df = select_only_single_model_stats(outputs_df, model_name)
   outputs_df = select_only_false(outputs_df)
   return select_problem_sample(outputs_df, problem_df)

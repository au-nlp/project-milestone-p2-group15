import argparse
import sys
from pathlib import Path
print("path", Path.cwd())
# sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from baselines.tot.tree_of_thought_llm_master.src.tot.methods.bfs import BFSToTSolver
from baselines.tot.math_arena_task import MathAarenaToTTask
from openai import AzureOpenAI

from dataclasses import dataclass

@dataclass
class ToTConfig:
    key_env_name: str
    endpoint_env_name: str
    api_version: str
    model_name: str
    n_generate_sample: int 
    n_evaluate_sample: int
    n_select_sample: int
    steps: int
    client_type: type[AzureOpenAI] = AzureOpenAI


def run_math_arena_tot(
    ToTConfig: ToTConfig,
    problem_descr: str,
    answer: str

    ):

  tot = BFSToTSolver(
    key_env_name=ToTConfig.key_env_name,
    endpoint_env_name=ToTConfig.endpoint_env_name,
    api_version=ToTConfig.api_version,
    client_type=ToTConfig.client_type,
    model_name=ToTConfig.model_name)

  task = MathAarenaToTTask(ToTConfig.steps, problem_descr, answer)
  ys, infos = tot.solve(
    task=task,
    idx=0,
    n_generate_sample=ToTConfig.n_generate_sample,
    n_select_sample=ToTConfig.n_select_sample,
    prompt_sample=problem_descr,
    n_evaluate_sample=ToTConfig.n_evaluate_sample,
    
    model = ToTConfig.model_name,
  )
  print(ys[0])
  return ys, infos
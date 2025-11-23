import argparse
from tree_of_thought_llm_master.src.tot.methods.bfs import solve
from math_arena_task import MathAarenaToTTask

def run_math_arena_tot():
  args = argparse.Namespace(backend='gpt-4', temperature=0.7, task='game24', naive_run=False, prompt_sample=None, method_generate='propose', method_evaluate='value', method_select='greedy', n_generate_sample=1, n_evaluate_sample=3, n_select_sample=5)

  task = MathAarenaToTTask()
  ys, infos = solve(args, task, 900)
  print(ys[0])
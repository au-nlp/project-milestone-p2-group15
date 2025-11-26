
from models.mock_model import MockClient
from baselines.tot.math_arena_tot_setup import ToTConfig, run_math_arena_tot
if __name__ == "__main__":
  config = ToTConfig(
    key_env_name="something",
    endpoint_env_name="someting",
    model_name="model",
    n_evaluate_sample=2,
    n_select_sample=2,
    n_generate_sample=2,
    steps=2,
    api_version="2022-01-01",
    client_type=MockClient
  )
  ys, infos = run_math_arena_tot(ToTConfig=config, problem_descr="What is 2+2", answer="4")

  print(ys)
  print(infos)

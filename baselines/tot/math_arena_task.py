
import re
from baselines.tot.tree_of_thought_llm_master.src.tot.tasks.base import Task
BETTER_FIRST = "more promising/correct step is 1"
BETTER_SECOND = 'more promising/correct step is 2'
EQUAL = "two reasoning steps are similarly promising/correct"
class MathAarenaToTTask(Task):
  steps: int 
  data: list[str]

  def __init__(self, steps: int,  problem_descr: str, answer: str):
    """
    Args:
      steps: number of thought steps - this is equal to the tree depth
      stops: stops model generation is the stops token is generated - is there to keep the steps short. Ex stops = ['\n'] or stops = [";"]
      problem_descr: The problem the model should solve
      answer: the answer to the problem (only used at the very end to check if it got the final right answer)
    """
    self.steps = steps
    self.data = [problem_descr]
    self.answer = [answer]

  def __len__(self) -> int:
    """Number of problems - we just parse 1 problem at a time here"""
    return 1

  def get_input(self, idx: int) -> str:
    """Given a problem index, idx, returns the input text for that problem"""
    return self.data[idx]
  
  def test_output(self, idx: int, output: str) -> dict[str, int]:
    """Given a model final output, check if its correct"""
    correct = False
    ground_truth = self.answer[0]
    last_line = output.strip().split("\n")[-1].lower()
    if ground_truth in last_line: # This will also be manually veryfied
        correct = True
    return {"r: ": int(correct)}
      
  @staticmethod
  def standard_prompt_wrap(question: str, current_steps:str='') -> str:
        return standard_prompt(question, current_steps)

  @staticmethod
  def vote_prompt_wrap(x: str, ys: list) -> str:
          prompt = vote_prompt
          for i, y in enumerate(ys, 1):
              # y = y.replace('Plan:\n', '')
              # TODO: truncate the plan part?
              prompt += f'Choice {i}:\n{y}\n'
          return prompt
      
  @staticmethod
  def vote_outputs_unwrap(vote_outputs: list, n_candidates: int) -> list:
      vote_results = [0] * n_candidates
      for vote_output in vote_outputs:
          pattern = r".*best choice is .*(\d+).*"
          match = re.match(pattern, vote_output, re.DOTALL)
          if match:
              vote = int(match.groups()[0]) - 1
              if vote in range(n_candidates):
                  vote_results[vote] += 1
          else:
              print(f'vote no match: {[vote_output]}')
      return vote_results

  @staticmethod
  def compare_prompt_wrap(x: str, ys: list) -> str:
      assert len(ys) == 2, 'compare prompt only supports 2 candidates'
      ys = [y.split('Reasoning step:\n')[-1] for y in ys]
      prompt = compare_prompt + f'Reasoning step 1:\n{ys[0]}\n\nReasoning step 2:\n{ys[1]}\n'
      return prompt



  @staticmethod
  def compare_output_unwrap(compare_output: str):
      if BETTER_FIRST in compare_output:
          return 0
      elif BETTER_SECOND in compare_output:
          return 1
      elif EQUAL in compare_output:
          return 0.5
      else:
          print(f'-----------------compare no match: {[compare_output]}')
          return -1


  # @staticmethod
  # def propose_promt_wrap(x: str, y: str="") -> str:
  #   """
  #   Args:
  #     x: The original problem input
  #     y: A partial reasoning trace
  #   """
  #   return propose_promt(x, y)
    
  # @staticmethod
  # def value_prompt_wrap(x: str, y:str ) -> str:
  #   """
  #   Given the init problem x, and the partial soltuion / reasoning steps so far, y, 
  #   returns a promt which asks a the model to rate how good the y is
  #   """

  #   # first check if we are already done:
  #   last_line = y.strip().split("\n")[-1]
  #   if "answer:" in last_line.lower():
  #     return value_last_step_prompt(x, y)
  #   return value_promt(x, y)


  # @staticmethod
  # def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
  #   value_names = [_.split('\n')[-1] for _ in value_outputs]
  #   value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20} 
  #   value = sum(value * value_names.count(name) 
  #           for name, value in value_map.items())
  #   return float(value)
  
  
example_problem = "Alice has 5 apples. John eates 2, but buys 4 more for Alice. Now Alice eats half. How many whole apples does Alice have left?"



standard_prompt = lambda question, current_steps: f""" 
Use mathematical reasoning to solve problems in steps. If you think you have a final answer, format as Answer: [your answer]. If not, just write the step.
Example qustion:
Question: {example_problem}

Current steps: 
If John eates 2 of Alices' 5 apples, then she has so far 5-2=3 left.
He buys 4 more, so now she has 3+4=7

Next possible step: 
 7/2 = 3.5

Now your turn
Question: {question}

Current steps: {current_steps}

Next possible step:
"""

vote_prompt = '''Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line "The best choice is {s}", where s the integer id of the choice.
'''

compare_prompt = F'''Briefly analyze the correctness of the following two math reasoning steps. Conclude in the last line "{BETTER_FIRST}", "{BETTER_SECOND}", or "{EQUAL}".
'''

score_prompt = '''Analyze the following math reasoning step, then at the last line conclude "Thus the promise/correctness score is {s}", where s is an integer from 1 to 10.
'''


# propose_promt = lambda input, current_steps:  (
# f"""Use mathematical reasoning to solve problems step by step.
# Example: 
# Question: {example_problem}

# Current steps: 
# If John eates 2 of Alices' 5 apples, then she has so far 5-2=3 left.
# He buys 4 more, so now she has 3+4=7

# Next possible steps: 
# 7/2 = 3.5

# Question: {input}

# current_steps {current_steps}
# """
# )

# value_promt = lambda problem, current_steps:  f"""Given the current partial reasoning, evaluate if this is going in the right direction. 
# Responds with one word (sure/likely/impossible)

# {example_problem}
# Alice eats half of 5 apples, so now she has 2.5 left. 
# impossible

# {example_problem}
# Alice eats half of 5 apples, so now she has 2.5 left. 
# Alice has 5 apples. n_apples=5
# John eates 2. n_apples-2 = 3. 
# sure

# {example_problem}
# Alice eats half of 5 apples, so now she has 2.5 left. 
# alice_apples = 5
# 5 - 2 + 4 = 7
# Now I want to devide the result by 2, but I have to handle the fractions. The question said whole apples.
# likely 


# {example_problem}
# Alice eats half of 5 apples, so now she has 2.5 left. 
# 5 - 2 = 3
# 3 + 4 = 7
# 7 / 2 = 3.5
# round(3.5)= 3
# sure

# {problem}
# {current_steps}
# # """

# value_last_step_prompt = lambda problem, answer: f'''Use mathematical reasoning. Given an input and an answer, give a judgement (sure/impossible) if the answer is correct, i.e. it reasoning is sound and achives the right answer.
# Input: {example_problem}
# Answer: (5-2+4)//2 = 3
# Judge: 
# sure
# Input: {example_problem}
# Answer: 5 apples, minus 2 is 3, then add 4 is 7. Devide by 2 and round, 3. 
# Judge: 
# sure
# Input: {example_problem}
# Answer: 5/2 is 2.5
# Judge: 
# impossible
# Input: {problem}
# Answer: {answer}
# Judge:'''



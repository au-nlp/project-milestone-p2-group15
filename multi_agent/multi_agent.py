from dataclasses import dataclass
from itertools import cycle
import textwrap
from time import sleep

from models.model_base import ModelBase
@dataclass
class Role:
  name: str 
  behavior: str

  def instruction(self) -> str:
    return f"You are are {self.name}. {self.behavior}"
  def __str__(self):
    return f"Role: {self.name}\n{textwrap.fill(self.behavior, width=80)}"
  



class Problem:
  roles_cycle: cycle
  all_roles: list[Role]
  problem_description: str
  welcome: str
  answer: str
  def __init__(self, roles: list[Role], problem_descr: str, answer: str):
    self._set_all(roles, problem_descr, answer)

  def _set_all(self, roles: list[Role], problem_descr: str, answer:str):
      self.roles_cycle = cycle(roles)
      self.all_roles = roles
      self.problem_description = problem_descr
      last = self.all_roles[-1]
      others = ", ".join([x.name for x in self.all_roles[:-1]])  
      self.welcome = f"Welcome {others}, and {last.name}.\nTogether, you should solve the following problem: >>\n{problem_descr}.<<" 
      self.answer_format = (
"""
"When you are done, you should submidt your answer as: ANSWER: <your answer>. 
No latex formatting, just the raw number/numbers or strings at the very end. 
Before you start sharing your toughts, give a little summary of the conversation so far. 
Give a list of the currently suggested answers. Everytime you propose an aswer, check this list. 
You proposal cannot be in this this list. Try again and submit a new unique answer."
"""
      )

      self.answer = answer
  def next_agent(self) -> Role: # this just loops over agents - can be changes to something smarter
    return next(self.roles_cycle) 
  
  def reset_cycle(self):
    self.roles_cycle = cycle(self.all_roles)
  
  def pose_problem(self) -> str:
    return f"{self.welcome}\n{self.answer_format}\n"
  
  def add_agent(self,role: Role): 
    self._set_all(roles=self.all_roles + [role], problem_descr=self.problem_description, answer=self.answer)
  
  def __str__(self) -> str:
    return textwrap.fill(self.pose_problem(), width=80)
  


def conversation(model:ModelBase, name:str, n_steps: int, problem: Problem, wait:int = 5, continue_from: str | None = None):
      if continue_from is None:
        problem.reset_cycle()
        roles = problem.all_roles
        raws = []
        messages =[
            {"role": "system", "content": role.instruction()} for role in roles
          ] + [{"role": "user", "content": problem.pose_problem()}]

      else:
        messages, raws = ModelBase.load_conv(continue_from)  

      for step in range(n_steps):
        print(f"\nSTEP {step}: \n")
        next_agent = problem.next_agent()
        reply, raw = model.send_msg_and_get_contnent(messages+[{"role": "user", "content": f"What do you say, {next_agent}"}])
        raws.append(raw)
        print(f"{next_agent}: {reply}")
        messages.append({"role": "assistant", "content": reply})
        path = ModelBase.save_conv(name=name, raw=raws, messages=messages)
      return messages, raw, path
# messages = conversation(2, twoplustwo)

rater_prompt = (
    """You have gone through several different choices for an answer. While the rejector rejected all of the answers, one among them is actually correct.
    Your job is to go through all of these answers using the knowledge you have acquired, try to argue how each of the answers could be true,
    then, rate and rank these answers. I want to see a list of all answers ranked on plausibility."""
)

def rank_answer(model:ModelBase, conversation: list[str]):
    reply, raw = model.send_msg_and_get_contnent(conversation+[{"role": "user", "content": f"{rater_prompt}"}])
    print(f"{reply}")
    return reply, raw



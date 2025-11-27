from dotenv import load_dotenv
import os, re, string
from enum import Enum
from datasets import load_dataset
from math_arena_datasets import categories_2025
import pandas as pd
from sklearn.model_selection import train_test_split
from time import sleep
from openai import AzureOpenAI
from multi_agent import Role, Problem
from prompt_template import Reflector

load_dotenv()

# From the GitHub of refexion: https://github.com/noahshinn/reflexion
class ReflexionStrategy(Enum):
    """
    NONE: No reflection
    LAST_ATTEMPT: Use last reasoning trace in context 
    REFLEXION: Apply reflexion to the next reasoning trace 
    LAST_ATTEMPT_AND_REFLEXION: Use last reasoning trace in context and apply reflexion to the next reasoning trace 
    """
    NONE = 'base'
    LAST_ATTEMPT = 'last_trial' 
    REFLEXION = 'reflexion'
    LAST_ATTEMPT_AND_REFLEXION = 'last_trial_and_reflexion'

class ReflexionAgent:
    def __init__(
        self,
        llm,
        strategy: ReflexionStrategy,
        evaluator_fn,
        reflector_prompt=Reflector,
        max_attempts=5,
    ):
        self.llm = llm
        self.strategy = strategy
        self.evaluator_fn = evaluator_fn
        self.reflector_prompt = reflector_prompt
        self.max_attempts = max_attempts

        # memory
        self.attempts = []
        self.reflections = []
        self.feedback = None


    def reflect(self, task: str):
        prompt = f"""
                      {self.reflector_prompt.behavior}

                      Task:
                      {task}

                      Attempts & reasoning:
                      {self.attempts}

                      Feedback from evaluator or environment:
                      {self.feedback}

                      Return a short self-reflection that improves the solver.
                  """
        reflection = self.llm(prompt)
        self.reflections.append(reflection.strip())
        return reflection.strip()


    def solve(self, task: str):
        """
        Run the Reflexion loop.
        """
        for i in range(self.max_attempts):
            base_prompt = f"Task: {task}\n"

            if self.strategy in [ReflexionStrategy.LAST_ATTEMPT, ReflexionStrategy.LAST_ATTEMPT_AND_REFLEXION]:
                base_prompt += f"\nPrevious attempt:\n{self.attempts[-1] if self.attempts else ''}"

            if self.strategy in [ReflexionStrategy.REFLEXION, ReflexionStrategy.LAST_ATTEMPT_AND_REFLEXION]:
                base_prompt += f"\nReflection:\n{self.reflections[-1] if self.reflections else ''}"

            base_prompt += "\nGive step-by-step solution and a final answer."

            print(f"\n=== Attempt {i+1} ===")
            attempt = self.llm(base_prompt).strip()
            print(attempt)

            self.attempts.append(attempt)

            # 3) Evaluate
            score, feedback = self.evaluator_fn(task, attempt)
            self.feedback = feedback

            print(f"Score: {score}")
            print(f"Feedback: {feedback}")

            if score is True:  # solved!
                return attempt

            # 4) If failed — apply reflection
            if self.strategy in [ReflexionStrategy.REFLEXION, ReflexionStrategy.LAST_ATTEMPT_AND_REFLEXION]:
                reflection = self.reflect(task)
                print(f"Reflection: {reflection}")

        # failsafe
        return self.attempts[-1]
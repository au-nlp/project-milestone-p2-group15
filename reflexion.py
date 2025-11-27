from dotenv import load_dotenv
from enum import Enum
from prompt_template import Reflector
from models.azure_api import Model

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
        llm : Model,
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
        messages = [{"role": "user", "content": prompt}]
    
        # call the method on your Model object
        reply, raw = self.llm.send_msg_and_get_contnent(messages)
        
        reflection = reply.strip() if reply else ""
        self.reflections.append(reflection)
        return reflection

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
            messages = [{"role": "user", "content": base_prompt}]
            reply, raw = self.llm.send_msg_and_get_contnent(messages)
            attempt = reply or ""
            print(attempt)
            self.attempts.append(attempt)

            # 3) Evaluate
            score, feedback = self.evaluator_fn(task, attempt)
            self.feedback = feedback

            print(f"Score: {score}")
            print(f"Feedback: {feedback}")

            if score == "true":  # solved!
                return attempt

            # 4) If failed — apply reflection
            if self.strategy in [ReflexionStrategy.REFLEXION, ReflexionStrategy.LAST_ATTEMPT_AND_REFLEXION]:
                reflection = self.reflect(task)
                print(f"Reflection: {reflection}")

        # failsafe
        return self.attempts[-1]
import os
from abc import ABC, abstractmethod
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

class Task(ABC):
    value_cache: list 
    steps: list 

    def __init__(self):
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass
    
    @abstractmethod
    def get_input(self, idx: int) -> str:
        pass
    
    @abstractmethod
    def test_output(self, idx: int, output: str):
        pass

    @abstractmethod
    @staticmethod
    def value_promt_wrap(x: str, y: str) -> str:
        pass

    @abstractmethod
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> str:
        pass

    @abstractmethod
    @staticmethod
    def cot_promt_wrap(x: str, y: str) -> str:
        pass

    @abstractmethod
    @staticmethod
    def vote_prompt_wrap(x: str, ys: list[str]) -> str:
        pass
    @abstractmethod
    @staticmethod
    def vote_outputs_unwrap(x: str, ys: list[str]) -> str:
        pass

    
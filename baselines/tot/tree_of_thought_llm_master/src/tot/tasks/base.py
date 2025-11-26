import os
from abc import ABC, abstractmethod
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

class Task(ABC):
    value_cache: list 
    steps: list 


    @abstractmethod
    def __len__(self) -> int:
        pass
    
    @abstractmethod
    def get_input(self, idx: int) -> str:
        pass
    
    @abstractmethod
    def test_output(self, idx: int, output: str):
        pass

    @staticmethod
    @abstractmethod
    def standard_prompt_wrap(question: str, current_steps:str='') -> str:
        pass

    @staticmethod
    @abstractmethod
    def vote_outputs_unwrap(vote_outputs: list, n_candidates: int) -> list:
        pass

    @staticmethod
    @abstractmethod
    def compare_prompt_wrap(x: str, ys: list) -> str: 
        pass

    @staticmethod
    def compare_output_unwrap(compare_output: str):
        pass

    @staticmethod
    @abstractmethod
    def vote_prompt_wrap(x: str, ys: list[str]) -> str:
        pass

    @staticmethod
    @abstractmethod
    def vote_outputs_unwrap(vote_outputs: list, n_candidates: int) -> list:
        pass

    
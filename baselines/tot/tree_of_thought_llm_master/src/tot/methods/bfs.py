import itertools
import numpy as np
from functools import partial
from tot.tasks.base import Task
from typing import Callable
from tot.models import promt_model
from openai import AzureOpenAI



class BFSToTSolver():
    promt_model: Callable[[str, int], str]
    def __init__(
            self,
            key_env_name: str, 
            endpoint_env_name: str,
            api_version: str,
            client_type: type[AzureOpenAI],
            model_name: str
            ):
        
        self.promt_model = lambda promt, n :  promt_model(
            key_env_name=key_env_name,
            endpoint_env_name=endpoint_env_name,
            api_version=api_version, 
            client_type=AzureOpenAI,
            model=model_name,
            promt=promt,
            n=n
        )


    def get_value(
        self,
        task: Task, x: str, y: str, n_evaluate_sample: int,  cache_value=True
    ) -> str:
        value_prompt = task.value_promt_wrap(x, y)

        if cache_value and value_prompt in task.value_cache:
            return task.value_cache[value_prompt]
        value_outputs = self.promt_model(value_prompt, n=n_evaluate_sample)
        value = task.value_outputs_unwrap(x, y, value_outputs)
        if cache_value:
            task.value_cache[value_prompt] = value
        return value


    def get_values(
                self,
                task: Task, 
                x: str, 
                ys: list[str], 
                n_evaluate_sample: int, 
                cache_value: bool = True
    ) -> list[str]:
        values = []
        local_value_cache = {}
        for y in ys:  # each partial output
            if y in local_value_cache:  # avoid duplicate candidates
                value = 0
            else:
                value = self.get_value(task, x, y, n_evaluate_sample, cache_value=cache_value)
                local_value_cache[y] = value
            values.append(value)
        return values


    def get_votes(
            self,
            task: Task, 
            x: str, 
            ys: list[str], 
            n_evaluate_sample: int
            ):
        vote_prompt = task.vote_prompt_wrap(x, ys)
        vote_outputs = self.promt_model(vote_prompt, n=n_evaluate_sample)
        values = task.vote_outputs_unwrap(vote_outputs, len(ys))
        return values


    def get_samples(
        self,
        task: Task,
        x: str,
        y: str,
        n_generate_sample: int,
        prompt_sample: str,
    ) -> list[str]:
        prompt = task.cot_promt_wrap(x, y)
        samples = self.promt_model(prompt, n=n_generate_sample)
        return [y + _ for _ in samples]


    def solve(
        self,
        task: Task,
        idx: int,
        n_generate_sample: int,
        prompt_sample: str,
        n_evaluate_sample: str,
        n_select_sample: str,
        model,
        to_print=True,
    ):
        x = task.get_input(idx)  # input
        ys = [""]  # current output candidates
        infos = []
        for step in range(task.steps):
            # generation
            new_ys = [
                self.get_samples(
                    task,
                    x,
                    y,
                    n_generate_sample,
                    prompt_sample=prompt_sample,
                )
                for y in ys
            ]
            new_ys = list(itertools.chain(*new_ys))
            ids = list(range(len(new_ys)))
            # evaluation
            values = self.get_votes(task, x, new_ys, n_evaluate_sample)

            # selection
            select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[
                :n_select_sample
            ]
            select_new_ys = [new_ys[select_id] for select_id in select_ids]

            # log
            if to_print:
                sorted_new_ys, sorted_values = zip(
                    *sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True)
                )
                print(
                    f"-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n"
                )

            infos.append(
                {
                    "step": step,
                    "x": x,
                    "ys": ys,
                    "new_ys": new_ys,
                    "values": values,
                    "select_new_ys": select_new_ys,
                }
            )
            ys = select_new_ys

        if to_print:
            print(ys)
        return ys, {"steps": infos}


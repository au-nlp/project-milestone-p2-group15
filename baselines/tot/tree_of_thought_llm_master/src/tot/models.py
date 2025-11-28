import os
import openai
from openai import AzureOpenAI
from functools import lru_cache

completion_tokens = prompt_tokens = 0

from time import sleep

mult_response = False # set to False if using something like groq to debug

def promt_model(
        key_env_name: str,
        endpoint_env_name: str,
        api_version: str,
        client_type: type[AzureOpenAI],
        promt: str,
        model: str, 
        n: int
    ):

    completion_tokens = prompt_tokens = 0

    client = make_client(key_env_name, endpoint_env_name, api_version, client_type)

    def completions_with_backoff(**kwargs):
        result = None
        
        for attempt in range(10):
            try:
                delay = attempt
                sleep(delay)
                print(">>>tries to call client.. Attempt>", attempt, "<<<")
                if mult_response:
                    result = client.chat.completions.create(**kwargs)
                else:
                    result = run_one_at_a_time(kwargs)

                print(">>>succesfully called client<<<")
                break
            except Exception as e:
                print(f">>>failed call to client., {e}<<<")

        assert result is not None, f">>>All 10 attemps to call client failed<<<"
        return result

    def run_one_at_a_time(kwargs):
        outputs = []
        n = kwargs["n"]
        while n>0:
            kwargs["n"]=1
            result = client.chat.completions.create(**kwargs)
            outputs.append(result.choices[0].message.content)
            n-=1
        return result
    

    def promt_model(prompt, model="gpt-4",  n=1) -> list:
        messages = [{"role": "user", "content": prompt}]
        return chatgpt(messages, model=model, n=n)
        
    def chatgpt(messages, model="gpt-4",  n=1) -> list:
        global completion_tokens, prompt_tokens
        outputs = []
        while n > 0:
            cnt = min(n, 20)
            n -= cnt
            res = completions_with_backoff(model=model, messages=messages,  n=cnt)
            outputs.extend([choice.message.content for choice in res.choices])
            # log completion tokens
            completion_tokens += res.usage.completion_tokens
            prompt_tokens += res.usage.prompt_tokens
        return outputs
    return promt_model(promt, model, n)

@lru_cache
def make_client(key_env_name: str, endpoint_env_name: str | None, api_version: str | None, client_type) :
    api_key = os.getenv(key_env_name) 
    if endpoint_env_name:
        api_base = os.getenv(endpoint_env_name)
    else:
        api_base = None

    kwargs = {k: v for k, v in {
        "api_key": api_key,
        "api_version": api_version,
        "azure_endpoint": api_base,
    }.items() if v is not None}

    client = client_type(**kwargs)
        

    return client
        
def gpt_usage():
    global completion_tokens, prompt_tokens
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens}

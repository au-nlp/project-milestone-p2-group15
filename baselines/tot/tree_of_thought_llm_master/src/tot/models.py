import os
import openai
import backoff 
from openai import AzureOpenAI
from functools import lru_cache

completion_tokens = prompt_tokens = 0



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

    @backoff.on_exception(backoff.expo, openai.error.OpenAIError)
    def completions_with_backoff(**kwargs):
        return client.chat.completions.create(kwargs)

    def promt_model(prompt, model="gpt-4",  n=1) -> list:
        messages = [{"role": "user", "content": prompt}]
        return chatgpt(messages, model=model, max_tokens=max_tokens, n=n)
        
    def chatgpt(messages, model="gpt-4",  n=1) -> list:
        global completion_tokens, prompt_tokens
        outputs = []
        while n > 0:
            cnt = min(n, 20)
            n -= cnt
            res = completions_with_backoff(model=model, messages=messages,  n=cnt, stop=stop)
            outputs.extend([choice.message.content for choice in res.choices])
            # log completion tokens
            completion_tokens += res.usage.completion_tokens
            prompt_tokens += res.usage.prompt_tokens
        return outputs
    return promt_model(promt, model, n)

@lru_cache
def make_client(key_env_name: str, endpoint_env_name: str, api_version: str, client_type) :
    api_key = os.getenv(key_env_name) 
    api_base = os.getenv(endpoint_env_name)

    client = client_type(
      api_key= api_key,
      api_version=api_version,
      azure_endpoint=(api_base)
    )
    
    return client
        
def gpt_usage(backend):
    global completion_tokens, prompt_tokens
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens}

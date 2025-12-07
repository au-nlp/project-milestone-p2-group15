import os
import openai
from openai import AzureOpenAI
from google.genai import Client as GoogleClient
from functools import lru_cache
from models.azure_api import azure_user_format
from models.google_api import google_user_format
completion_tokens = prompt_tokens = 0

from time import sleep

mult_response = True # set to False if using something like groq to debug

def promt_model(
        key_env_name: str,
        endpoint_env_name: str,
        api_version: str,
        client_type: type[AzureOpenAI] | type[GoogleClient],
        promt: str,
        model: str, 
        n: int
    ):

    completion_tokens = prompt_tokens = 0
    candidates_token_count, prompt_token_count, thoughts_token_count, total_token_count, cached_content_token_count = 0

    client = make_azure_client(key_env_name, endpoint_env_name, api_version, client_type) if client_type == AzureOpenAI else make_google_client(key_env_name=key_env_name)

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
    

    def send_promt(prompt, model="gpt-4",  n=1) -> list:
        if client_type == AzureOpenAI:
            messages = [azure_user_format(prompt)]
            return chatgpt(messages, model=model, n=n)
        if client_type == GoogleClient:
            messages = [google_user_format(prompt)]
            return google(messages, model=model, n=n)
        else:
            raise ValueError("not valid client")
        
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
    def google(messages, model, n=1) -> list:
        global candidates_token_count, prompt_token_count, thoughts_token_count, total_token_count, cached_content_token_count
        outputs = []
        while n > 0:
            cnt = min(n, 20)
            n -= cnt
            res = completions_with_backoff(model=model, contents=messages,  candidate_count=cnt)
            outputs.extend([choice.text for choice in res.candidates])
            # log completion tokens
            candidates_token_count+= res.candidates_token_count
            prompt_token_count += res.prompt_token_count
            thoughts_token_count += res.thoughts_token_count
            total_token_count += res.total_token_count
            cached_content_token_count +=res.cached_content_token_count
        return outputs
    return send_promt(promt, model, n)



@lru_cache
def make_azure_client(key_env_name: str, endpoint_env_name: str | None, api_version: str | None, client_type) :
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

@lru_cache
def make_google_client(key_env_name: str):
    api_key = os.getenv(key_env_name) 
    client = GoogleClient(
        api_key=api_key
    )
    return client
        
def gpt_usage():
    global completion_tokens, prompt_tokens
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens}

def google_usage():
     global candidates_token_count, prompt_token_count, thoughts_token_count, total_token_count, cached_content_token_count
    return {
        "candidates_token_count": candidates_token_count, 
        "prompt_token_count": prompt_token_count,
        "thoughts_token_count": thoughts_token_count,
        "total_token_count": total_token_count,
        "cached_content_token_count": cached_content_token_count}

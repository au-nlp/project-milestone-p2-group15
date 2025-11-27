from openai import AzureOpenAI
import os
from typing import Callable


class Model:
  model_name: str 
  _send_messages: Callable[[list[dict[str, str]]], dict]
  num_tokens: dict

  def __init__(self, model_name:str, send_messages: Callable[[list[dict[str, str]]], dict]):
    self.model_name = model_name
    self._send_messages = send_messages
    self.num_tokens = []

  def _raw_response(self, msg: list[dict[str, str]]) -> dict:
    result = self._send_messages(msg)
    self.num_tokens.append(result.usage)
    return result
  
  def send_msg_and_get_contnent(self, msg: list[dict[str, str]]) -> tuple[str, dict]:
    """returns both the message conent and the raw resonse"""
    raw = self._raw_response(msg)
    content = raw.choices[0].message.content
    return content, raw


class Client:
  client: AzureOpenAI
  def __init__(self, api_version: str):
    with open("azure/key.txt") as f:
      key = f.read().strip()

    with open("azure/endpoint.txt") as f:
      endpoint = f.read().strip()

    self.client =  AzureOpenAI(
      api_key= (key),
      api_version=api_version,
      azure_endpoint=(endpoint)
  )
    
  def select_model(self, model_name: str) -> Model:
    def send_messages(msgs: list[dict[str, str]]) -> dict: #Json
      return self.client.chat.completions.create(
        model=model_name,  # or your deployment name
        messages=msgs
        )
    return Model(
      model_name=model_name,
      send_messages=send_messages
    )
      



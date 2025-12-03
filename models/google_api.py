
import os
from typing import Callable
from google import genai
from google.genai import types
from models.model_base import ModelBase

class GoogleModel(ModelBase):
  model_name: str 
  num_tokens: list
  _send_messages: Callable[[list[dict[str, str]], str], dict]

  def __init__(self, model_name:str, send_messages: Callable[[list[dict[str, str]], str], dict]):
    self.model_name = model_name
    self._send_messages = send_messages
    self.num_tokens = []

  def _raw_response(self, msg: list[dict[str, str]], instruction: str) -> dict:
    response = self._send_messages(msg, instruction )


    self.num_tokens.append(response.usage_metadata)
    return response
  
  def send_msg_and_get_contnent(self, msg: list[dict[str, str]], instruction: str) -> tuple[str, dict]:
    """returns both the message conent and the raw resonse"""
    raw = self._raw_response(msg, instruction)
    content = raw.text
    return content, raw



class GoogleClient:
  client: genai.Client
  def __init__(self):
    api_key = os.getenv("GEMINI_API_KEY")

    self.client =  genai.Client(
      api_key= (api_key),

  )
    
  def select_model(self, model_name: str) -> GoogleModel:
    def send_messages(msgs: list[dict[str, str]], instruction: str) -> dict: #Json
      return self.client.models.generate_content(
        model=model_name,  # or your deployment name
        contents=msgs,
        config=types.GenerateContentConfig(
        system_instruction=instruction
        )
      )
    return GoogleModel(
      model_name=model_name,
      send_messages=send_messages
    )
      
def google_user_format(user_msg: str) -> dict[str, str]:
  return {"role": "user", "parts": [{"text": user_msg}]}

def google_assistant_format(assistant: str) -> dict[str, str]:
    return  {"role": "model", "parts": [{"text": assistant}]}


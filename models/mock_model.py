from models.model_base import ModelBase
import json
from types import SimpleNamespace
class MockModel(ModelBase):
  """A model outputing a mock string - no need API call"""

  def __init__(self): 
    pass 

  def send_msg_and_get_contnent(self, msg: list[dict[str, str]]) -> tuple[str, dict]:
    raw =""" 
    {
    "id": "some_id",
    "model": "gpt-5",
    "choices": [
      {
        "index": 0,
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": "A mock response"
        }
      }
    ],
    "usage": {
      "prompt_tokens": 123,
      "completion_tokens": 456,
      "total_tokens": 789
    }
  }
  """

    response = [
    {
      "role": "system",
      "content": "system mock message 1"
    },
    {
      "role": "system",
      "content": "System mock message 2"
    },
    {
      "role": "user",
      "content": "User mock message 1"
    },
    {
      "role": "assistant",
      "content": "Assisent mock message 1"
    },
      ]
  
    return response, json.loads(raw, object_hook=lambda d: SimpleNamespace(**d))
  


class MockCompletions:
  def create(model, messages):
    return MockModel().send_msg_and_get_contnent(msg = [])[1]
class MockChat:
  completions =  MockCompletions()




class MockClient:
    chat = MockChat()
    def __init__(self, api_key, api_version, azure_endpoint):
      pass


      
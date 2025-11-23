from model_base import ModelBase

class MockModel(ModelBase):
  """A model outputing a mock string - no need API call"""

  def __init__(self): 
    pass 

  def send_msg_and_get_contnent(self, msg: list[dict[str, str]]) -> tuple[str, dict]:
    raw = {
      "completion_tokens":11348,
       "prompt_tokens":2112,
       "total_tokens":13460,
    }
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
  
    return response, raw
  


class MockCompletions:
  def create(model, messages):
    return {}
class MockChat:
  completion =  MockCompletions()




class MockClient:
    chat = MockChat()
    def __init__(self, api_key, api_version, azure_endpoint):
      pass


      
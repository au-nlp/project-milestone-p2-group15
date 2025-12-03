from abc import ABC, abstractmethod
import json
from pathlib import Path

class ModelBase(ABC):
  model_name: str 
  num_tokens: dict

  @abstractmethod
  def send_msg_and_get_contnent(*args) -> tuple[str, dict]:
      pass

  @staticmethod
  def save_conv(name: str, messages: list[dict[str, str]], raw) -> Path:
      base = Path("data") / "conversations" / name
      base.mkdir(parents=True, exist_ok=True)

      (base / "message.json").write_text(json.dumps(messages, indent=2))
      (base / "raw.json").write_text(json.dumps([r.model_dump_json() for r in raw], indent=2))

      return base
  
  @staticmethod
  def load_conv(base: str | Path) -> tuple[list, list]:
      base = Path(base)
      with open(base / "message.json") as f1:
          messages = json.load(f1)
      with open(base / "raw.json") as f2:
          raw = json.load(f2)
      return messages, raw



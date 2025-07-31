
# import json
# from pathlib import Path
# from typing import Type, TypeVar
# from rm.memo import MemoFactory
# from pydantic import BaseModel, PrivateAttr

# def test_pydantic_memo():
#     T = TypeVar("T", bound="AutoSavingModel")


#     class AutoSavingModel(BaseModel):
#         _memo_factory: MemoFactory = PrivateAttr()
#         _suspend_sync: bool = PrivateAttr(default=False)

#         def __init__(self, **data):
#             path = data.pop("__path__")
#             super().__init__(**data)
#             self._path = Path(path)
#             self._save()

#         def __setattr__(self, name, value):
#             super().__setattr__(name, value)
#             if not name.startswith("_") and not self._suspend_sync:
#                 self._save()

#         def _save(self):
#             with self._path.open("w", encoding="utf-8") as f:
#                 json.dump(self.model_dump(), f, ensure_ascii=False, indent=2)

#         @classmethod
#         def load(cls: Type[T], path: str) -> T:
#             path = Path(path)
#             if not path.exists():
#                 raise FileNotFoundError(f"No config found at {path}")
#             with path.open("r", encoding="utf-8") as f:
#                 data = json.load(f)
#             return cls(__path__=path, **data)

#     class ModelConfig(AutoSavingModel):
#         name: str
#         layers: int


#     x = ModelConfig(_memo_factory=MemoFactory(), name="resnet", layers=50)
#     assert 1 == 1



from pathlib import Path

from pydantic import Field
from rm.memo import MemoFactory
from rm.resource_db.base_model import AutoSavingModel

class ModelConfig(AutoSavingModel):
    name: str
    age: int
    path: Path = Field(default_factory=lambda: Path("aaa.bbb.json"))


def test_model_config():


    file_path = Path("test.json")
    assert not file_path.exists()

    memo = MemoFactory().make_file_memo(file_path)


    x = ModelConfig(_memo=memo, name="resnet", age=50)
    x.name = "tester"
    x.age = 20

    x = ModelConfig.load(memo)
    assert x.name == "tester"
    assert x.age == 20

    memo.remove()







def path_auto_rel_abs_convert_test():


    file_path = Path("aaa/bbb/ccc.json")
    memo = MemoFactory().make_file_memo(file_path)

    x = ModelConfig(_memo=memo, name="resnet", age=50, path="ddd.json")
    
    # 속성 반환시 path는 모두 절대 경로화
    assert x.path == Path("aaa/bbb/ccc/ddd.json")

    # dump 시 path는 모두 상대 경로화 및 str으로 변환환
    assert x.model_dump()["path"] == "ddd.json"


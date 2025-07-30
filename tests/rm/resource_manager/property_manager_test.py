from pathlib import Path
import shutil
from rm.memo.factory import MemoFactory
from rm.resource_db.property_manager import PathHandling_PropertyManager, PropertyManager

DIR_PATH = Path("test_dir")
KEY = "key"
VALUE = "value"


def test_property_manager():
    factory = MemoFactory()
    pm = PropertyManager(DIR_PATH, factory)

    # 객체 생성과 동시에 파일이 생성됨


    # key-value를 저장하면 객체를 새로 만들어도 로드가 가능해야 함
    assert pm.file_memo.file_path.exists() is True
    pm.set(KEY, VALUE)

    assert pm.content == {KEY: VALUE}

    pm = PropertyManager(DIR_PATH, factory)
    assert pm.get(KEY) == VALUE

    shutil.rmtree(DIR_PATH)
    assert pm.file_memo.file_path.exists() is False

    # assert pm.get("test") == "test"


def test_path_handling_property_manager():
    factory = MemoFactory()

    pm = PathHandling_PropertyManager(DIR_PATH, factory)
    abs_path = pm.dir_path / Path(VALUE)
    pm.set_as_relative_path(KEY, abs_path)
    assert pm.get(KEY) == VALUE
    assert pm.get_as_absolute_path(KEY) == abs_path

    shutil.rmtree(DIR_PATH)

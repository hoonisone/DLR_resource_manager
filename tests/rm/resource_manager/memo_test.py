from rm.memo import MemoFactory
from pathlib import Path

from rm.memo.file_io import YamlFileIO


def test_file_io():
    file_path = Path("test_memo.yaml")
    io = YamlFileIO()
    assert file_path.exists() is False
    io.create(file_path)
    assert file_path.exists() is True

    assert io.read(file_path) == {}

    io.write(file_path, {"test": "test"})
    assert io.read(file_path) == {"test": "test"}
    file_path.unlink()



def test_memo():
    factory = MemoFactory()
    memo = factory.make_file_memo(Path("test_memo"))
    assert memo.file_path.exists() is True

    assert memo.get() == {}

    memo.set({"test": "test"})
    assert memo.get() == {"test": "test"}

    memo.remove()
    assert memo.file_path.exists() is False


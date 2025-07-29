from rm.memo import MemoFactory
from pathlib import Path


def test_memo():
    factory = MemoFactory()
    memo = factory.make_file_json_file_memo(Path("test_memo"))
    assert memo.file_path.exists() is True

    assert memo.get() == {}

    memo.set({"test": "test"})
    assert memo.get() == {"test": "test"}

    memo.remove()
    assert memo.file_path.exists() is False

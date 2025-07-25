from pathlib import Path
from .memo import FileMemo
from .file_io import JsonFileIO, YamlFileIO


class MemoFactory:
    def make_file_json_file_memo(self, file_path:Path)->FileMemo:
        return FileMemo(file_path.with_suffix(".json"), JsonFileIO(), None)

    def make_file_yaml_file_memo(self, file_path:Path)->FileMemo:
        return FileMemo(file_path.with_suffix(".yaml"), YamlFileIO(), None)


if __name__ == "__main__":
    factory = MemoFactory()
    memo = factory.make_file_json_file_memo(Path("test_memo"))
    memo.set({"test": "test"})
    print(memo.get())
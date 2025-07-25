import re
from pathlib import PurePath, Path
import shutil
from typing import Callable, Generic, Optional, Type
from dataclasses import dataclass, field
from typing import TypeVar

ID = Optional[int]
NAME = str

PATH = TypeVar('PATH', bound=PurePath)

@dataclass
class Name_ID_Parser():
    # path로 부터 id와 name 추출
    ID_PATTERN: str

    def extract_id_and_name(self, path:PurePath)->tuple[ID, NAME]:
        path_str = str(path)
        match = re.search(self.ID_PATTERN, path_str)
        id = int(match.group(1)) if match else None
        name = path_str.replace(f"___id_{id}", "")
        return (id, name)

    def merge_id_and_name(self, id:ID, name:NAME)->PurePath:
        if id is None:
            return PurePath(name)
        else:
            return PurePath(f"{name}___id_{id}")



class FileSystemManager:        
    @classmethod
    def is_empty(cls, path:Path)->bool:        
        return not any(path.iterdir())
    
    
    @classmethod
    def delete_within_given_root(cls, path:Path):
        parents = list(path.parents)
        shutil.rmtree(path)
        for parent in parents[:-1]:
            if cls.is_empty(parent):
                shutil.rmtree(parent)
            else:
                break

if __name__ == "__main__":
    parser = Name_ID_Parser(ID_PATTERN = r'___id_(\d+)$')
    assert parser.merge_id_and_name(1, "test") == Path("test___id_1")
    assert parser.extract_id_and_name(Path("test___id_1")) == (1, "test")
    assert parser.extract_id_and_name(Path("test___id_1/test___id_20")) == (20, "test___id_1/test")
    del parser


class ID_Name_Manager:
    # path를 관리하며 id와 name 계산 및 조작

    def __init__(self, path:PurePath, parser: Name_ID_Parser):
        self.parser = parser
        self._id: ID = None
        self._name: NAME = ""
        self.path = path


    @property
    def id_name(self)->tuple[ID, NAME]:
        return (self._id, self._name)
    
    @property
    def id(self)->ID:
        return self._id
    
    @property
    def name(self)->NAME:
        return self._name
    
    @property
    def has_id(self)->bool:
        return self._id is not None

    @property
    def path(self)->PurePath:
        return self.parser.merge_id_and_name(self._id, self._name)

    @id.setter
    def id(self, id:ID):
        if id is None:
            raise ValueError("For assign id, id bust not be None. But it is None.")
        self._id = id

    @name.setter
    def name(self, name:NAME):
        self._name = name
        
    @path.setter
    def path(self, path:PurePath):
        """
        path를 설정하면 id와 name을 자동으로 추출하여 설정합니다.
        """
        id, name = self.parser.extract_id_and_name(path)
        self._id = id
        self._name = name

if __name__ == "__main__":
    parser = Name_ID_Parser(ID_PATTERN = r'___id_(\d+)$')
    assert ID_Name_Manager(Path("test___id_1"), parser).id == 1
    assert ID_Name_Manager(Path("test___id_1"), parser).name == "test"
    assert ID_Name_Manager(Path("test___id_1"), parser).path == Path("test___id_1")
    assert ID_Name_Manager(Path("test"), parser).id is None
    assert ID_Name_Manager(Path("test"), parser).name == "test"
    del parser
    
class Linked_ID_Name_Manager(ID_Name_Manager):
    # 실제 폴더에 연결되어 경로로 조작 가능
    @property
    def path(self)->Path:
        return Path(super().path)

    @path.setter
    def path(self, path: Path):
        ID_Name_Manager.path.fset(self, path)
        # super(Linked_ID_Name_Manager, Linked_ID_Name_Manager).path.__set__(self, path)

    @property
    def exists(self)->bool:
        return self.path.exists() # type: ignore

    def _rename(self, callback:Callable[[], None])->None:
        old_path = self.path
        callback()
        new_path = self.path
        if old_path != new_path:
            old_path.rename(new_path)
    
    @property
    def id(self)->ID:
        return self._id

    @id.setter
    def id(self, id:ID):
        if id is None:
            raise ValueError("For assign id, id bust not be None. But it is None.")
        def callback():
            self._id = id
        self._rename(callback)

    @property
    def name(self)->NAME:
        return self._name

    @name.setter
    def name(self, name:NAME):
        def callback():
            self._name = name
        self._rename(callback)

    def remove(self)->None:
        if self.exists:
            FileSystemManager.delete_within_given_root(self.path)
            
    def create(self)->None:
        self.path.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    parser = Name_ID_Parser(ID_PATTERN = r'___id_(\d+)$')
    assert Linked_ID_Name_Manager(Path("test___id_1"), parser).id == 1
    assert Linked_ID_Name_Manager(Path("test___id_1"), parser).name == "test"
    assert Linked_ID_Name_Manager(Path("test___id_1"), parser).path == Path("test___id_1")
    Linked_ID_Name_Manager(Path("test/aaa/bbb"), parser).create()
    Linked_ID_Name_Manager(Path("test/aaa/bbb"), parser).remove()

    Linked_ID_Name_Manager(Path("testAAA"), parser).create()
    assert Linked_ID_Name_Manager(Path("testAAA"), parser).exists is True
    Linked_ID_Name_Manager(Path("testAAA"), parser).id = 1
    assert Linked_ID_Name_Manager(Path("testAAA___id_1"), parser).exists is True
    Linked_ID_Name_Manager(Path("testAAA___id_1"), parser).name = "renamed"
    assert Linked_ID_Name_Manager(Path("renamed___id_1"), parser).exists is True
    Linked_ID_Name_Manager(Path("renamed___id_1"), parser).remove()
    assert Linked_ID_Name_Manager(Path("renamed___id_1"), parser).exists is False
    del parser

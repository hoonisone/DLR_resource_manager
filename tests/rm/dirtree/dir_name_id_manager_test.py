from rm.dirtree import DirTree, DirTreeFactory
from pathlib import Path


def test_name_id_parser():
    factory = DirTreeFactory()
    parser = factory.dir_name_id_parser
    assert parser.merge(1, "test") == Path("test___id_1")
    assert parser.split(Path("test___id_1")) == (1, "test")
    assert parser.split(Path("test___id_1/test___id_20")) == (20, "test___id_1/test")

def test_name_id_manager():
    factory = DirTreeFactory()

    # split 기능 확인 (id가 없는 경우 )
    manager = factory.dir_id_name_manager(Path("test"))
    assert manager.id is None
    assert manager.name == "test"
    assert manager.path == Path("test")


    # split 기능 확인 (id가 배정 된 경우)
    manager = factory.dir_id_name_manager(Path("test___id_1"))
    assert manager.id == 1
    assert manager.name == "test"
    assert manager.path == Path("test___id_1")

    manager.id = 10
    assert manager.id == 10

    manager.name = "renamed"
    assert manager.name == "renamed"

    assert manager.path == Path("renamed___id_10")




def test_linked_name_id_manager():
    factory = DirTreeFactory()
    
    manager = factory.dir_linked_id_name_manager(Path("test/aaa/bbb"))
    assert manager.exists is False
    manager.create()
    assert manager.exists is True

    # id 변경 시 실제 파일 경로 변경 확인
    manager.id = 1
    assert Path("test/aaa/bbb___id_1").exists()

    # 이름 변경 시 실제 파일 변경 확인
    manager.name = "renamed"
    assert Path("test/aaa").exists() is False
    assert Path("test").exists() is False
    assert Path("renamed___id_1").exists()

    manager.remove()
    assert manager.exists is False
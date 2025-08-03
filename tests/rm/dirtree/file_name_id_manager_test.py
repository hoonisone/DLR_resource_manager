from rm.dirtree.file_name_id_manager import File_Name_ID_Manager, File_Name_ID_Parser, Linked_File_Name_ID_Manager
from pathlib import Path

def test_file_name_id_parger():
    parser = File_Name_ID_Parser()
    assert parser.split(Path("test___id_1.yaml")) == (1, "test", "yaml")
    assert parser.merge(1, "test", "yaml") == Path("test___id_1.yaml")


def test_name_id_manager():

    manager = File_Name_ID_Manager(Path("test"), File_Name_ID_Parser())
    manager = Linked_File_Name_ID_Manager(manager)

    # split 기능 확인 (id가 없는 경우 )

    assert manager.name == "test"
    assert manager.path == Path("test")

    assert manager.path.exists() is False
    manager.create()
    assert manager.path.exists() is True

    manager.id = 10
    assert manager.id == 10
    assert manager.path == Path("test___id_10")
    assert manager.path.exists() is True

    manager.name = "renamed"
    assert manager.name == "renamed"
    assert manager.path == Path("renamed___id_10")
    assert manager.path.exists() is True

    manager.ext = "yaml"
    assert manager.ext == "yaml"
    assert manager.path == Path("renamed___id_10.yaml")
    assert manager.path.exists() is True

    manager.remove()
    assert manager.path.exists() is False




# def test_linked_name_id_manager():
#     factory = DirTreeFactory()
    
#     manager = factory.linked_id_name_manager(Path("test/aaa/bbb"))
#     assert manager.exists is False
#     manager.create()
#     assert manager.exists is True

#     # id 변경 시 실제 파일 경로 변경 확인
#     manager.id = 1
#     assert Path("test/aaa/bbb___id_1").exists()

#     # 이름 변경 시 실제 파일 변경 확인
#     manager.name = "renamed"
#     assert Path("test/aaa").exists() is False
#     assert Path("test").exists() is False
#     assert Path("renamed___id_1").exists()

#     manager.remove()
#     assert manager.exists is False
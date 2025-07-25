from functools import cached_property
from pathlib import Path, PurePath
from typing import Type
from .dir_tree import DirTree, TerminalCheker
from .name_id_manager import ID_Name_Manager, Linked_ID_Name_Manager, Name_ID_Parser


class DirTreeFacotry:
    @cached_property
    def parser_id_pattern(self)->str:
        return r'___id_(\d+)$'

    @cached_property
    def name_id_parser(self)->Name_ID_Parser:
        return Name_ID_Parser(ID_PATTERN = self.parser_id_pattern)

    def id_name_manager(self, path:PurePath)->ID_Name_Manager:
        return ID_Name_Manager(path, self.name_id_parser)

    def linked_id_name_manager(self, path:Path)->Linked_ID_Name_Manager:
        return Linked_ID_Name_Manager(path, self.name_id_parser)

    @cached_property
    def terminal_node_checker(self)->TerminalCheker:
        f = self.name_id_parser.extract_id_and_name
        return lambda path : f(path)[0] is not None

    def get_dir_tree(self, dir_path:Path)->DirTree:
        return DirTree(dir_path, self.terminal_node_checker)

if __name__ == "__main__":
    factory = DirTreeFacotry()
    parser = factory.name_id_parser
    assert parser.merge_id_and_name(1, "test") == Path("test___id_1")
    assert parser.extract_id_and_name(Path("test___id_1")) == (1, "test")
    assert parser.extract_id_and_name(Path("test___id_1/test___id_20")) == (20, "test___id_1/test")


    assert factory.id_name_manager(Path("test___id_1")).id == 1
    assert factory.id_name_manager(Path("test___id_1")).name == "test"
    assert factory.id_name_manager(Path("test___id_1")).path == Path("test___id_1")
    assert factory.id_name_manager(Path("test")).id is None
    assert factory.id_name_manager(Path("test")).name == "test"

    assert factory.linked_id_name_manager(Path("test___id_1")).id == 1
    assert factory.linked_id_name_manager(Path("test___id_1")).name == "test"
    assert factory.linked_id_name_manager(Path("test___id_1")).path == Path("test___id_1")
    assert factory.linked_id_name_manager(Path("test/aaa/bbb")).exists is False
    factory.linked_id_name_manager(Path("test/aaa/bbb")).create()
    assert factory.linked_id_name_manager(Path("test/aaa/bbb")).exists is True
    factory.linked_id_name_manager(Path("test/aaa/bbb")).id = 1
    assert factory.linked_id_name_manager(Path("test/aaa/bbb")).id == 1
    assert factory.linked_id_name_manager(Path("test/aaa/bbb")).name == "test/aaa/bbb"
    factory.linked_id_name_manager(Path("test/aaa/bbb")).remove()
    assert factory.linked_id_name_manager(Path("test/aaa/bbb")).exists is False

    tree = factory.get_dir_tree(Path("aaa"))
    print(tree.all_violating_paths)
    
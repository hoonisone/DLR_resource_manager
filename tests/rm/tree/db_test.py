from pathlib import Path
from rm.db.db import FileSystemDB
from rm.db.db_tree import DBTreeNode
from rm.db.record import DirRecord, ElementType, FileRecord


def test_terminal_nodes():
    db = FileSystemDB(root_dir_path=Path("root"), RecordClass=DirRecord, element_type=ElementType.DIR)
    record = db.create("1/2/3/4/5/6/7/8/9/10")
    assert record.name == "1/2/3/4/5/6/7/8/9/10"









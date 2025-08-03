from pathlib import Path
from rm.tree.db import DBTreeNode


def test_terminal_nodes():
    root = DBTreeNode(name="root")
    leaf1 = root.create(Path("1/2/3/4/5/6/7/8/9/10"))
    leaf2 = root.create(Path("1/2/3/4/5/a/b/c/d/e"))
    assert root.terminal_nodes() == [leaf1, leaf2]

    root.clear()


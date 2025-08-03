
from pathlib import Path
from rm.tree.path_tree import PurePathTreeNode





def test_create():
    root = PurePathTreeNode(name="root")
    leaf = root.create(Path("1/2/3/4/5/6/7/8/9/10"))
    assert root.size == 11
    assert root.get(Path("1/2/3/4/5/6/7/8/9/10")) == leaf


def test_unlink():
    root = PurePathTreeNode(name="root")
    leaf1 = root.create(Path("1/2/3/4/5/6/7/8/9/10"))
    leaf2 = root.create(Path("1/2/3/4/5/a/b/c/d/e"))
    root.unlink(Path("1/2/3/4/5/6/7/8"))
    assert root.size == 13










from rm.tree.tree import ExtendedTreeNode

def is_root(node:ExtendedTreeNode)->bool:
    if node.parent is not None:
        return False
    if node.depth != 0:
        return False
    if node.root != node:
        return False
    return True



def test_create():
    root = ExtendedTreeNode(name="root")
    leaf = root.create(["a", "b", "c"])
    assert root.get("a").get("b").get("c") == leaf

    leaf = root.create(["a", '1', '2', '3'])
    assert root.size == 7


def test_get():
    root = ExtendedTreeNode(name="root")
    leaf = root.create(["a", "b", "c"])

    c = root.get(["a", "b", "c"])
    assert c == leaf
    


def test_remove():
    root = ExtendedTreeNode(name="root")
    a = root.create(["a"])
    b = a.create(["b"])
    c = b.create(["c"])
    root.unlink(["a", "b"])

    b.print_tree()
    

    assert is_root(a) == False
    assert is_root(b) == True
    assert is_root(c) == False


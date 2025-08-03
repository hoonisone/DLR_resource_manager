

from rm.tree.tree import LikableTreeNode

def is_root(node:LikableTreeNode)->bool:
    assert node.parent == None
    assert node.depth == 0
    assert node.root == node

def test_root()->None:
    root = LikableTreeNode(name="root")
    assert root.parent == None
    assert root.depth == 0
    assert root.root == root


def test_link_child()->None:
    root = LikableTreeNode(name="root")
    child = LikableTreeNode(name="a")

    root.link_child(child)
    assert child.parent == root
    assert child.depth == 1
    assert child.root == root

    assert root.size == 2
    assert child.size == 1

def test_unlink_child()->None:
    root = LikableTreeNode(name="root")
    child = LikableTreeNode(name="a")

    root.link_child(child)
    removed_child = root.unlink_child("a")

    assert child == removed_child
    assert child.root == child
    assert child.parent == None
    assert child.depth == 0

def test_create_child()->None:
    root = LikableTreeNode(name="root")
    a = root.create_child("a")
    b = a.create_child("b")

    assert a.parent == root
    assert a.depth == 1
    assert a.root == root

    assert b.parent == a
    assert b.depth == 2
    assert b.root == root

    a.unlink_child("b")

    is_root(b)

# def test_tree():
#     root = TreeNode(root=None, parent=None, name="root", depth=0)
#     root.create("a")
#     root.create("b")
#     assert root.size == 2

#     root.print_tree()

#     root.create(Path("a/b/c/d/1/2/3/v.txt"))
#     root.print_tree()


#     assert root.size == 9


#     root.create(Path("a/b/c/d/3/4/5/v.txt"))
#     root.print_tree()
#     assert root.size == 13
    
#     root.remove(["a", "b", "c", "d", "1", "2"])
#     root.print_tree()
#     assert root.size == 10

# def test_hooking_tree():
#     root = HookingTreeNode(root=None, parent=None, name="root", depth=0)

#     after_create = 0
#     after_remove = 0

#     def after_create_callback(node:TreeNode):
#         nonlocal after_create
#         after_create += 1

#     def after_remove_callback(node:TreeNode):
#         nonlocal after_remove
#         after_remove += 1

#     root.hook.register___after_node_create(after_create_callback)
#     root.hook.register___after_node_removed(after_remove_callback)

#     root.create_child("a")
#     assert after_create == 1

#     root.remove_child("a")
#     assert after_remove == 1

# def test_path_tree():
#     root = PurePathTreeNode(root=None, parent=None, name="root", depth=0)
#     child = root.create_child(Path("a"))
#     assert root.is_empty == False
#     assert child.path == Path("root/a")
#     root.remove(Path("a"))
#     assert root.size == 0
#     assert root.is_empty == True

#     root.create_child(Path("a/b/c/d/e/f/g.txt"))
#     root.remove(Path("a/b/c/d/e/f"))
#     assert root.size == 0



# def test_path_tree():
#     root = PathTreeNode(root=None, parent=None, name="root", depth=0)
#     assert root.is_empty == True
#     assert root.path.exists()

#     child = root.create_child("a")
#     assert root.is_empty == False
#     assert child.path.exists()

#     root.remove("a")
#     assert not child.path.exists()
#     assert root.is_empty == True

#     (root.path/"temp").touch()
#     assert root.is_empty == False

#     shutil.rmtree(root.path)


# def link_unlink_test():
#     root = PathTreeNode(root=None, parent=None, name="root", depth=0)
#     root.create_child(["a", "b", "c"])


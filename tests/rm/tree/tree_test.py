import os
import shutil
os.chdir("W:/RM/src")

from rm.tree.tree import TreeNode




def make_root_tree():
    return TreeNode(name="root")
    


def test_add_and_get_child()->None:
    root = make_root_tree()
    child = root.append_child(TreeNode(name="a"))
    assert root.get_child("a") == child


def test_has_and_remove_child():
    root = make_root_tree()
    assert root.has_child('a') == False

    root.append_child(TreeNode(name="a"))
    assert root.has_child('a') == True

    root.remove_child("a")
    assert root.has_child('a') == False


def test_size()->None:
    root = make_root_tree()
    root.append_child(TreeNode(name="a")).append_child(TreeNode(name="a"))
    root.get_child("a").append_child(TreeNode(name="b"))
    root.append_child(TreeNode(name="b"))
    assert root.size == 5



def test_print_tree()->None:
    root = make_root_tree()
    root.append_child(TreeNode(name="a"))
    root.append_child(TreeNode(name="b"))
    root.get_child("a").append_child(TreeNode(name="c"))
    root.get_child("a").append_child(TreeNode(name="d"))
    root.get_child("b").append_child(TreeNode(name="e"))
    root.get_child("b").append_child(TreeNode(name="f"))
    root.print_tree()





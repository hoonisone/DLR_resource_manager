
from pathlib import Path
import shutil
from rm.tree.path_tree import PathTreeNode


def test_sync_file_system_path():
    root_path = Path("root")
    if root_path.exists():
        shutil.rmtree(root_path)

    assert root_path.exists() == False
    root = PathTreeNode(name=root_path, _init_file_system_sync_on=False)
    assert root_path.exists() == False
    root.file_system_sync_on = True
    assert root_path.exists() == True
    shutil.rmtree(root_path)


    path = Path("1/2/3/4/5/6/7/8/9/10")
    assert (root_path/path).exists() == False
    root.create(path)
    assert (root_path/path).exists() == True

    child = root.unlink(path)
    assert (root_path/path).exists() == False

    root.clear()
    child.clear()





def test_rename():
    root = PathTreeNode(name="root")
    leaf = root.create(Path("1/2/3/4/5/6/7/8/9/10"))
    
    a = root.get(Path("1/2/3/4/5"))
    b = a.rename("a")
    c = root.get(Path("1/2/3/4/a"))

    assert a == b
    assert a == c

    assert root.has(Path("1/2/3/4/a/6/7/8/9/10"))

    root.clear()
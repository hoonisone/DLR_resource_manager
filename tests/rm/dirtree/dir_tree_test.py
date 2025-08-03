# from pathlib import Path
# import shutil
# from rm.dirtree import DirTree, DirTreeFactory


# def test_dir_tree_factory():
#     factory = DirTreeFactory()

#     # factory.get_dir_tree(Path("test")).create()

    
#     # assert factory.get_dir_tree(Path("test")).exists() is True
#     # factory.get_dir_tree(Path("test")).remove()
#     # assert factory.get_dir_tree(Path("test")).exists() is False


# def test_file_tree():
#     Path("a/a").mkdir(exist_ok=True, parents=True)
#     Path("a/a/a___id_0.yaml").touch()
#     Path("a/a/b___id_1.yaml").touch()
#     Path("a/a/c").touch()
#     Path("a/b___id_2.yaml").touch()

#     tree = DirTreeFactory().get_file_tree(Path("a"))
#     print(tree.terminal_nodes)

#     assert len(tree.terminal_nodes) == 3
#     assert len(tree.all_violating_paths) == 1


#     shutil.rmtree("a")




# # from resource_manager.dirdb import DirDB, DirDBFactory
# # from pathlib import Path

# # def test_dir_db_factory():
# #     factory = DirDBFactory(Path("test"))
# #     assert factory.dir_db is not None


# # def test_dir_db():
# #     factory = DirDBFactory(Path("test"))
# #     assert factory.dir_db is not None

# from pathlib import Path
# import shutil
# from rm.dirdb import DirDBFactory


# def test_file_db():
#     Path("a/a").mkdir(exist_ok=True, parents=True)
#     Path("a/a/a___id_0.yaml").touch()
#     Path("a/a/b___id_1.yaml").touch()
#     Path("a/b___id_2.yaml").touch()

#     db = DirDBFactory().make_filedb(Path("a"), "yaml")

#     db.metadata.last_id = 2
#     db.create_new("hello")
#     print(db.names)
#     print(db.ids)
#     # assert len(tree.terminal_nodes) == 3
#     # assert len(tree.all_violating_paths) == 1


#     shutil.rmtree("a")
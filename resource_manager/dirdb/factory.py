
from functools import cached_property
from pathlib import Path
from resource_manager.dirdb.dirdb import DirDB, DirTreeFacotry


class DirDBFactory:
    @cached_property
    def dir_tree_factory(self)->DirTreeFacotry: return DirTreeFacotry()

    def make_dirdb(self, dir_path:Path)->DirDB: return DirDB(dir_path, self.dir_tree_factory)
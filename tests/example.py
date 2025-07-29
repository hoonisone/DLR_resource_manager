from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Type

from resource_manager import ConfigManager, ResourceDBFactory, ResourceRecord, ResourceDB, ID, NAME


@dataclass
class WorkConfigKey:
    DATASET_ID: str = "dataset_id"
    LOG_FILE_NAME: str = "log_file_name"
    TRAIN_FILE_PATH: str = "train_code_path"
    MODEL_ID: str = "model_id"

@dataclass
class WorkConfigManager(ConfigManager):
    # 데이터 셋 리소스에 대한 config를 관리하는 객체

    @cached_property
    def dataset_id(self)->Path:
        if WorkConfigKey.DATASET_ID in self.config:
            return self.config[WorkConfigKey.DATASET_ID]
        else:
            raise ValueError("Dataset ID is not set")

    @cached_property
    def model_id(self)->str:
        if WorkConfigKey.MODEL_ID in self.config:
            return self.config[WorkConfigKey.MODEL_ID]
        else:
            raise ValueError("Model ID is not set")

    @property
    def log_file_name(self)->str:
        if WorkConfigKey.LOG_FILE_NAME in self.config:
            return self.config[WorkConfigKey.LOG_FILE_NAME]
        else:
            return "log.txt"

    @property
    def log_file_path(self)->Path:
        return self.dir_path / self.log_file_name

    @cached_property
    def train_code_path(self)->Path:
        if WorkConfigKey.TRAIN_FILE_PATH in self.config:
            return self.config[WorkConfigKey.TRAIN_FILE_PATH]
        else:
            project_root = Path("/home/workspace/mmdetection")
            return project_root/"tools/train.py"


class WorkRecord(ResourceRecord):
    def make_train_bash_code(self)->str:
        train_code_path = self.config_manager.train_code_path #type: ignore
        dataset_id = self.config_manager.dataset_id #type: ignore
        log_file_path = self.config_manager.log_file_path #type: ignore
        model_id = self.config_manager.model_id #type: ignore

        return f"python {train_code_path} --dataset {dataset_id} --log-file {log_file_path} --model {model_id}"

    def make_val_bash_code(self)->str:
        return ""

    def make_test_bash_code(self)->str:
        return ""


class WorkDB(ResourceDB):
    pass


@dataclass
class DatasetResourceFactory(ResourceDBFactory):
    CONFIG_MANAGER_CLASS:Type[ConfigManager] = WorkConfigManager
    RECORD_CLASS:Type[ResourceRecord] = WorkRecord
    DB_CLASS:Type[ResourceDB] = WorkDB

if __name__ == "__main__":
    project_root = Path("/home/submodules/mmdetection/")
    works_dir = project_root/"works"
    factory = DatasetResourceFactory(works_dir)
    db = factory.resource_db

    db.create("AAA_model___BBB_dataset___CCC_config")
    work: WorkRecord = db.get(0)  # type: ignore

    '''
        write below config to works/AAA_model___BBB_dataset___CCC_config/config.py for test
        {
            "dataset_id": "BBB_dataset",
            "model_id": "AAA_model",
            "log_file_name": "log.txt",
            "train_code_path": "tools/train.py"
        }
    '''

    print(work.make_train_bash_code())
    print(work.make_val_bash_code())
    print(work.make_test_bash_code())
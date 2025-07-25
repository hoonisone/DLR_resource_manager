from ast import Dict
from functools import cached_property
from pathlib import Path
import shlex
from typing import Any, Optional

class DIR:
    TRAIN = "train"
    CHECKPOINT = "checkpoints"
    VAL = "val"
    TEST = "test"
    WORK_DIR = "work_dirs"



class FILE:
    LOG = "log.txt"
    MAIN_CONFIG = "main_config.py"
    # CHECKPOINT = "checkpoint.pth"
    # RESULT = "result.json"


class Record:
    def __init__(self, dir_path: Path):
        self.dir_path = dir_path

class WorkPathManager:
    def __init__(self, dir_path: Path):
        self.dir_path = dir_path

    @cached_property
    def train_dir_path(self)->Path:
        return self.dir_path/DIR.TRAIN

    @cached_property
    def checkpiont_dir_path(self)->Path:
        return self.train_dir_path/DIR.CHECKPOINT

    def checkpoint_file_path(self, epoch:int)->Path:
        return self.checkpiont_dir_path/f"epoch_{epoch}.pth"

    @cached_property
    def train_log_file_path(self)->Path:
        return self.train_dir_path/FILE.LOG

    @cached_property
    def main_config_file_path(self)->Path:
        return self.train_dir_path/FILE.MAIN_CONFIG




class MMDetectionCommandBuilder:
    TRAIN_COMMAND_FILE = "tools/train.py"
    TEST_COMMAND_FILE = "tools/test.py"
    
    @staticmethod
    def _flatten_cfg_dict(d: dict, parent_key: str = "") -> list[tuple[str, Any]]:
        """
        중첩된 dict를 'a.b.c': value 형태로 flatten
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(MMDetectionCommandBuilder._flatten_cfg_dict(v, new_key))
            else:
                items.append((new_key, v))
        return items

    @classmethod
    def build_mmdet_command(cls, script_path: str, args_list: list, options_dict: Any = None) -> str:
        """
        필요한 인자들을 받아 완전한 CLI 형식의 MMDetection 명령어를 빌드하여 반환
        """
        command = ["python", str(script_path)]  # 경로 객체도 str 처리
        command.extend(str(arg) for arg in args_list)  # Path 포함 가능성 고려

        if options_dict:
            for key, value in options_dict.items():
                if key == "--cfg-options":
                    if not isinstance(value, dict):
                        raise ValueError("--cfg-options value must be a dict")
                    # 중첩 dict flatten 후 key=value 형식으로 변환
                    flat_items = cls._flatten_cfg_dict(value)
                    cfg_str = " ".join(f"{k}={v}" for k, v in flat_items)
                    command.extend([key, cfg_str])
                elif isinstance(value, bool):
                    if value:
                        command.append(key)
                elif isinstance(value, list):
                    for v in value:
                        command.extend([key, str(v)])
                else:
                    command.extend([key, str(value)])

        return shlex.join(command)

    @classmethod
    def make_train_command(cls, config_path:Path, options:dict):
        return cls.build_mmdet_command(cls.TRAIN_COMMAND_FILE, [config_path], options)
    
    @classmethod
    def make_test_command(cls, config_path:Path, options:dict):
        return cls.build_mmdet_command(cls.TEST_COMMAND_FILE, [config_path], options)


class WorkRecord(Record):

    def __init__(self, dir_path: Path):
        super().__init__(dir_path)
        self.work_path_manager = WorkPathManager(dir_path)

    @staticmethod
    def make_command(command_file:Path, config_path:Path, options:dict):
        return f"python {command_file} {config_path} {options}"





    def make_train_command(self):
        config_path = self.work_path_manager.main_config_file_path
        options_dict={
            "--work-dir":self.work_path_manager.train_dir_path,
            "--cfg-options": {
                "custom_config":{
                    "work_id":1,
                    "model":{
                        "type":"from_model",
                        "id":1,
                        "epoch":"None",
                    },
                    "train_dataset":1
                }
            }
        }
        return MMDetectionCommandBuilder.make_train_command(config_path.as_posix(), options_dict)

    # def make_val_command(self):
    #     return f"python tools/val.py {self.config_path} --work-dir {self.work_dir}"

    # def make_test_command(self):
    #     return f"python tools/test.py {self.config_path} --work-dir {self.work_dir}"

if __name__ == "__main__":
    work_record = WorkRecord(Path("/home/submodules/mmdetection/resource/bear_train___id_1"))
    work_record = WorkRecord(Path("/home/submodules/mmdetection/resource/beverage_train_all_light___id_4"))
    work_record = WorkRecord(Path("/home/submodules/mmdetection/resource/beverage_train_L10___id_3"))

    
    print(work_record.make_train_command())
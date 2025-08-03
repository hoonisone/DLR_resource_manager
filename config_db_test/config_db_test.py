import shutil
from mmdet_rm.config.config_resource import Config_ResourceFactory
from pathlib import Path
import yaml

def save_yaml(file_path:Path, data:dict):
    with open(file_path, "w") as f:
        yaml.dump(data, f)

def make_test_env():
    paths = [
        Path("a/a/a___id_1.yaml"),
        Path("a/a/b___id_2.yaml"),
        Path("a/b___id_3.yaml"),
    ]

    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    
    save_yaml(Path("a/a/a___id_1.yaml"), {"base_ids": None,"model_id": 1, "dataset_id": 1, "work_id": 1})
    save_yaml(Path("a/a/b___id_2.yaml"), {"base_ids": 1, "model_id": 2, "dataset_id": 2})
    save_yaml(Path("a/b___id_3.yaml"), {"base_ids": [2], "model_id": 3 })


def remove_test_env():
    shutil.rmtree(Path("a"))

def test_config_db():
    make_test_env()
    factory = Config_ResourceFactory(Path("a"))
    
    config = factory.db.get(3)
    
    assert config.file_path == Path("a/b___id_3.yaml")

    print(config.load())
    
    remove_test_env()
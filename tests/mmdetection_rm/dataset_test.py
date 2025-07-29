from dataclasses import dataclass, field
from pathlib import Path
import shutil
from mmdetection_rm.dataset.dataset_resource import DatasetResourceFactory


from mmdetection_rm.settings import MMDetection_RM_Settings, get_settings, set_settings
from mmdetection_rm.factory import MMDetection_RM_Factory

def test_dataset_resource_factory():
    settings = get_settings()
    rm_factory = MMDetection_RM_Factory()
    dataset_factory = rm_factory.dataset_factory
    dataset_db = dataset_factory.resource_db


    dataset_db.create("test")
    assert dataset_factory.resource_db.exist("test")

    shutil.rmtree(settings.dataset_dir)




@dataclass
class Custom_MMDetection_RM_Settings(MMDetection_RM_Settings):
    project_root:Path = field(default=Path("W:/RM/new/resources"))




def test_dataset_resource_factory_with_custom_settings():
    origin_setting = get_settings()
    new_setting = Custom_MMDetection_RM_Settings()
    set_settings(new_setting) 

    rm_factory = MMDetection_RM_Factory()

    assert rm_factory.dataset_factory.resource_db.dir_db.dir_path == new_setting.dataset_dir    

    set_settings(origin_setting)





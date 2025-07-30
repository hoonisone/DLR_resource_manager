from dataclasses import dataclass, field
from pathlib import Path
import shutil
from mmdet_rm.dataset.dataset_resource import DatasetConfigKey, DatasetResourceFactory


from mmdet_rm.settings import MMDetection_RM_Settings, get_settings, set_settings
from mmdet_rm.factory import MMDetection_RM_Factory

def test_dataset_resource_factory():
    settings = get_settings()
    rm_factory = MMDetection_RM_Factory()
    dataset_factory = rm_factory.dataset_factory
    dataset_db = dataset_factory.db


    record = dataset_db.create("test")
    assert dataset_factory.db.exist("test")

    record.property_manager.dataset_dir_path = record.dir_path / "data"
    record.property_manager.annotation_file_path = record.dir_path / "annotation.json"

    assert record.property_manager.dataset_dir_path == record.dir_path / "data"
    assert record.property_manager.annotation_file_path == record.dir_path / "annotation.json"




    shutil.rmtree(settings.dataset_dir)






@dataclass
class Custom_MMDetection_RM_Settings(MMDetection_RM_Settings):
    project_root:Path = field(default=Path("W:/RM/new/resources"))




def test_dataset_resource_factory_with_custom_settings():
    origin_setting = get_settings()
    new_setting = Custom_MMDetection_RM_Settings()
    set_settings(new_setting) 

    rm_factory = MMDetection_RM_Factory()

    assert rm_factory.dataset_factory.db.dir_db.dir_path == new_setting.dataset_dir    

    set_settings(origin_setting)





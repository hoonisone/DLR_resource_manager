

from pathlib import Path
import shutil
from mmdet_rm.config.config_resource import ConfigRecord
from mmdet_rm.dataset.dataset_resource import DatasetRecord
from mmdet_rm.work.work_resource import WorkRecord
from mmdet_rm.work.task import TaskRecord
from mmdet_rm.factory import get_root_factory
from mmdet_rm.settings import get_settings


def test_task_record():
    
    # shutil.rmtree(get_settings().resource_dir)

    dataset_record:DatasetRecord = get_root_factory().dataset_factory.db.create("test_dataset")
    dataset_record.property_manager.annotation_file_path =  dataset_record.dir_path/Path("annotation.json")

    config_record:ConfigRecord = get_root_factory().config_factory.db.create("test_config")
    config_record.property_manager.main_config_file_path = config_record.dir_path/Path("config.py")
    

    work_record:WorkRecord = get_root_factory().work_factory.db.create("test_work")
    work_record.property_manager.config_id = config_record.id

    task_record:TaskRecord = work_record.create_train_task(dataset_record.id, 1, 10)

    assert task_record.property_manager.config_id == config_record.id
    assert task_record.property_manager.work_id == work_record.id
    assert task_record.property_manager.dataset_id == dataset_record.id
    assert task_record.property_manager.epoch == 10
    assert task_record.property_manager.task_type == "train"
    assert task_record.property_manager.mmdet_config_file_path == config_record.property_manager.main_config_file_path


    shutil.rmtree(get_settings().resource_dir)



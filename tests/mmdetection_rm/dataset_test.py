import shutil
from mmdetection_rm.dataset.dataset_resource import DatasetResourceFactory


from mmdetection_rm.settings import get_settings
from mmdetection_rm.factory import MMDetection_RM_Factory

def test_dataset_resource_factory():
    settings = get_settings()
    rm_factory = MMDetection_RM_Factory()
    dataset_factory = rm_factory.dataset_factory
    dataset_db = dataset_factory.resource_db


    dataset_db.create("test")
    assert dataset_factory.resource_db.exist("test")

    shutil.rmtree(settings.dataset_dir)










import shutil
from mmdet_rm.factory import MMDetection_RM_Factory
from mmdet_rm.settings import get_settings


def test_work_resource_factory():
    settings = get_settings()
    rm_factory = MMDetection_RM_Factory()
    work_db = rm_factory.work_factory.db
    work_db.create("test")
    assert work_db.exist("test")
    shutil.rmtree(settings.work_dir)
    shutil.rmtree(settings.resource_dir)
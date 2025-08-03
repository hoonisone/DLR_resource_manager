# from dataclasses import dataclass, field
# from pathlib import Path
# import shutil

# from mmdet_rm.settings import MMDetection_RM_Settings, get_settings, set_settings
# from mmdet_rm.factory import MMDetection_RM_Factory


# def remove_resource_dir():
#     settings = get_settings()
#     shutil.rmtree(settings.resource_dir)

# # def test_dataset_resource_refer_config_test():
# #     # 데이터셋 리소스에서 레퍼 설정이 잘 되는가?
# #     dataset_factory = DatasetResourceFactory()
# #     dataset_db = dataset_factory.db

# #     record = dataset_db.create("test")
# #     record.property_manager.dataset_dir_path = record.dir_path / "data"
# #     record.property_manager.annotation_file_path = record.dir_path / "annotation.json"

# #     assert record.property_manager.dataset_dir_path == record.dir_path / "data"
# #     assert record.property_manager.annotation_file_path == record.dir_path / "annotation.json"

# #     remove_resource_dir()
    

# def test_refer_dataset_resource():
#     rm_factory = MMDetection_RM_Factory()
#     dataset_factory = rm_factory.dataset_factory
#     dataset_db = dataset_factory.db

#     record = dataset_db.create("base")
#     record.property_manager.dataset_dir_path = "data"
#     record.property_manager.annotation_file_path = "annotation.json"
#     refer_id = record.id

#     refer_record = dataset_db.create("main")
#     refer_record.property_manager.refer_id = refer_id
#     assert refer_record.property_manager.refered_property_manager.dataset_dir_absolute_path == record.dir_path/'data'

#     remove_resource_dir()


# def test_dataset_resource_factory():
#     rm_factory = MMDetection_RM_Factory()
#     dataset_factory = rm_factory.dataset_factory
#     dataset_db = dataset_factory.db


#     record = dataset_db.create("test")
#     assert dataset_factory.db.exist("test")

#     record.property_manager.dataset_dir_path = record.dir_path / "data"
#     record.property_manager.annotation_file_path = record.dir_path / "annotation.json"

#     assert record.property_manager.dataset_dir_path == record.dir_path / "data"
#     assert record.property_manager.annotation_file_path == record.dir_path / "annotation.json"




#     remove_resource_dir()






# @dataclass
# class Custom_MMDetection_RM_Settings(MMDetection_RM_Settings):
#     project_root:Path = field(default=Path("W:/RM/new/resources"))




# def test_dataset_resource_factory_with_custom_settings():
#     origin_setting = get_settings()
#     new_setting = Custom_MMDetection_RM_Settings()
#     set_settings(new_setting) 

#     rm_factory = MMDetection_RM_Factory()

#     assert rm_factory.dataset_factory.db.dir_db.path == new_setting.dataset_dir    

#     set_settings(origin_setting)





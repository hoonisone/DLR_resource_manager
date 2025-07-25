from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Dict, Type, Any, Optional

from .config_types import ConfigTypes
from .dataset_config_db import DatasetConfigDB
from .scheduler_config_db import SchedulerConfigDB
from .default_runtime_config_db import DefaultRuntimeConfigDB
from .work_config_db import WorkConfigDB
from .path_manager import PathManager
from ..dirdb.dirdb import DirDB


@dataclass
class ConfigDBFactory:
    """
    ConfigDB 팩토리 클래스
    PathManager를 사용하여 경로 계산을 분리하고, 
    다양한 타입의 ConfigDB를 생성합니다.
    """
    BASE_RESOURCE_DIR: Path = field(default_factory=lambda: Path('resource_db'))

    # ConfigDB 타입별 클래스 매핑 (Registry 패턴 + 상수 사용)
    CONFIG_DB_REGISTRY: Dict[str, Type] = field(default_factory=lambda: {
        ConfigTypes.DATASET: DatasetConfigDB,
        ConfigTypes.SCHEDULER: SchedulerConfigDB,
        ConfigTypes.DEFAULT_RUNTIME: DefaultRuntimeConfigDB,
        ConfigTypes.WORK: WorkConfigDB,
        # 향후 추가될 config 타입들
        # ConfigTypes.MODEL: ModelConfigDB,
        # ConfigTypes.OPTIMIZER: OptimizerConfigDB,
    })
    
    @cached_property
    def path_manager(self) -> PathManager:
        return PathManager(self.BASE_RESOURCE_DIR)

    def _create_dir_db(self, config_type: str) -> DirDB:
        config_root_path = self.path_manager.get_config_root_path(config_type)
        return DirDB(config_root_path)
    
    def _create_config_db(self, config_type: str) -> Any:
        """
        특정 config 타입에 대한 ConfigDB를 생성
        
        Args:
            config_type: config 타입 (ConfigTypes 상수 사용)
            
        Returns:
            생성된 ConfigDB 인스턴스
            
        Raises:
            ValueError: 지원하지 않는 config 타입인 경우
        """
        if config_type not in self.CONFIG_DB_REGISTRY:
            raise ValueError(f"지원하지 않는 config 타입: {config_type}. "
                           f"지원되는 타입: {list(self.CONFIG_DB_REGISTRY.keys())}")
        
        # 1. 디렉터리 생성
        self.path_manager.create_config_directory(config_type)
        
        # 2. DirDB 생성
        dir_db = self._create_dir_db(config_type)
        
        # 3. ConfigDB 생성
        config_db_class = self.CONFIG_DB_REGISTRY[config_type]
        return config_db_class(dir_db)
    
    def get_dataset_config_db(self) -> DatasetConfigDB:
        """
        DatasetConfigDB 인스턴스를 생성하여 반환
        
        Returns:
            DatasetConfigDB 인스턴스
        """
        return self._create_config_db(ConfigTypes.DATASET)
    
    def get_scheduler_config_db(self) -> SchedulerConfigDB:
        """
        SchedulerConfigDB 인스턴스를 생성하여 반환
        
        Returns:
            SchedulerConfigDB 인스턴스
        """
        return self._create_config_db(ConfigTypes.SCHEDULER)
    
    def get_default_runtime_config_db(self) -> DefaultRuntimeConfigDB:
        """
        DefaultRuntimeConfigDB 인스턴스를 생성하여 반환
        
        Returns:
            DefaultRuntimeConfigDB 인스턴스
        """
        return self._create_config_db(ConfigTypes.DEFAULT_RUNTIME)

    
    def get_work_config_db(self) -> WorkConfigDB:
        """
        DefaultRuntimeConfigDB 인스턴스를 생성하여 반환
        
        Returns:
            DefaultRuntimeConfigDB 인스턴스
        """
        return self._create_config_db(ConfigTypes.WORK)

    
    def get_config_db(self, config_type: str) -> Any:
        """
        일반적인 ConfigDB 생성 메서드
        
        Args:
            config_type: 생성할 config 타입 (ConfigTypes 상수 사용)
            
        Returns:
            해당 타입의 ConfigDB 인스턴스
        """
        return self._create_config_db(config_type)
    
    def register_config_db_type(self, config_type: str, config_db_class: Type, dir_name: str):
        """
        새로운 ConfigDB 타입을 등록
        
        Args:
            config_type: config 타입 이름
            config_db_class: ConfigDB 클래스
            dir_name: 디렉터리 이름
        """
        self.CONFIG_DB_REGISTRY[config_type] = config_db_class
        self.path_manager.add_config_type(config_type, dir_name)
    
    def get_supported_config_types(self) -> list[str]:
        """
        지원되는 모든 config 타입을 반환
        
        Returns:
            지원되는 config 타입 리스트
        """
        return list(self.CONFIG_DB_REGISTRY.keys())

    
    def get_all_config_root_paths(self) -> Dict[str, Path]:
        """
        모든 config 타입의 루트 경로를 반환
        
        Returns:
            config 타입을 키로 하고 경로를 값으로 하는 딕셔너리
        """
        return self.path_manager.get_all_config_root_paths()
    
    def set_base_resource_dir(self, new_path: Path):
        """
        기본 리소스 디렉터리 경로를 변경
        
        Args:
            new_path: 새로운 기본 리소스 디렉터리 경로
        """
        self.path_manager.set_base_resource_dir(new_path)


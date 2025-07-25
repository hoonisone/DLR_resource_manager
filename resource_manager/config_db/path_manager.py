from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass, field

from .config_types import ConfigTypes, ConfigDirNames


@dataclass
class PathManager:
    """
    경로 계산을 전담하는 매니저 클래스
    복잡한 경로 계산 로직을 분리하여 관리합니다.
    """
    
    # 기본 리소스 디렉터리
    BASE_RESOURCE_DIR: Path
    
    # 각 config 타입별 하위 디렉터리 이름 (상수 사용)
    CONFIG_DIR_MAPPING: Dict[str, str] = field(default_factory=lambda: {
        ConfigTypes.DATASET: ConfigDirNames.DATASET,
        ConfigTypes.SCHEDULER: ConfigDirNames.SCHEDULER,
        ConfigTypes.DEFAULT_RUNTIME: ConfigDirNames.DEFAULT_RUNTIME,
        ConfigTypes.MODEL: ConfigDirNames.MODEL,
        ConfigTypes.OPTIMIZER: ConfigDirNames.OPTIMIZER,
    })
    
    def __post_init__(self):
        """초기화 후 기본 리소스 디렉터리 생성"""
        self._ensure_base_directory()
    
    def _ensure_base_directory(self):
        """기본 리소스 디렉터리가 존재하는지 확인하고 없으면 생성"""
        if not self.BASE_RESOURCE_DIR.exists():
            self.BASE_RESOURCE_DIR.mkdir(parents=True, exist_ok=True)
    
    def get_config_root_path(self, config_type: str) -> Path:
        """
        특정 config 타입의 루트 경로를 반환
        
        Args:
            config_type: config 타입 (ConfigTypes 상수 사용)
            
        Returns:
            해당 config 타입의 루트 경로
            
        Raises:
            ValueError: 지원하지 않는 config 타입인 경우
        """
        if not ConfigTypes.is_valid_type(config_type):
            raise ValueError(f"지원하지 않는 config 타입: {config_type}. "
                           f"지원되는 타입: {ConfigTypes.get_all_types()}")
        
        dir_name = ConfigDirNames.get_dir_name(config_type)
        return self.BASE_RESOURCE_DIR / dir_name
    
    def get_all_config_root_paths(self) -> Dict[str, Path]:
        """
        모든 config 타입의 루트 경로를 반환
        
        Returns:
            config 타입을 키로 하고 경로를 값으로 하는 딕셔너리
        """
        return {
            config_type: self.get_config_root_path(config_type)
            for config_type in ConfigTypes.get_all_types()
        }
    
    def add_config_type(self, config_type: str, dir_name: str):
        """
        새로운 config 타입을 추가
        
        Args:
            config_type: 새로운 config 타입 이름
            dir_name: 해당 config 타입의 디렉터리 이름
        """
        self.CONFIG_DIR_MAPPING[config_type] = dir_name
    
    def get_supported_config_types(self) -> list[str]:
        """
        지원되는 모든 config 타입을 반환
        
        Returns:
            지원되는 config 타입 리스트
        """
        return ConfigTypes.get_all_types()
    
    def get_base_resource_dir(self) -> Path:
        """
        기본 리소스 디렉터리 경로를 반환
        
        Returns:
            기본 리소스 디렉터리 경로
        """
        return self.BASE_RESOURCE_DIR
    
    def set_base_resource_dir(self, new_path: Path):
        """
        기본 리소스 디렉터리 경로를 변경
        
        Args:
            new_path: 새로운 기본 리소스 디렉터리 경로
        """
        self.BASE_RESOURCE_DIR = new_path
        self._ensure_base_directory()
    
    def create_config_directory(self, config_type: str) -> Path:
        """
        특정 config 타입의 디렉터리를 생성
        
        Args:
            config_type: 생성할 config 타입
            
        Returns:
            생성된 디렉터리 경로
        """
        config_path = self.get_config_root_path(config_type)
        config_path.mkdir(parents=True, exist_ok=True)
        return config_path 
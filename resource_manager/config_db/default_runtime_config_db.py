from dataclasses import dataclass, field

from resource_manager.config_db.config_db_base import ConfigDB
from resource_manager.config_db.config_types import ConfigFileNames, ConfigTypes


@dataclass
class DefaultRuntimeConfigDB(ConfigDB):
    """
    Default Runtime Config 관리 시스템
    ConfigDB를 상속받아 default runtime 전용 설정을 제공합니다.
    """
    
    # Default Runtime 전용 config 파일명
    CONFIG_NAME: str = field(default=ConfigFileNames.DEFAULT_RUNTIME, init=False)
    
    def __post_init__(self):
        """초기화 후 실행되는 메서드"""
        super().__post_init__()
    
    def get_config_type(self) -> str:
        """
        Config 타입을 반환
        
        Returns:
            Config 타입 (default_runtime)
        """
        return ConfigTypes.DEFAULT_RUNTIME 
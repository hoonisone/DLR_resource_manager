"""
Config 타입 상수 정의
타입 안전성과 유지보수성을 위한 중앙 집중식 상수 관리
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigTypes:
    """
    Config 타입 상수 클래스
    frozen=True로 불변성 보장
    """
    
    # Config 타입 상수
    DATASET: str = 'dataset'
    WORK: str = 'work'
 

@dataclass(frozen=True)
class ConfigDirNames:
    """
    Config 디렉터리 이름 상수 클래스
    """
    
    # 디렉터리 이름 상수
    DATASET: str = 'dataset_config_db'
    SCHEDULER: str = 'scheduler_config_db'
    DEFAULT_RUNTIME: str = 'default_runtime_config_db'
    MODEL: str = 'model_config_db'
    OPTIMIZER: str = 'optimizer_config_db'
    WORK: str = 'work_config_db'
    
    @classmethod
    def get_dir_name(cls, config_type: str) -> str:
        """
        config 타입에 해당하는 디렉터리 이름을 반환
        
        Args:
            config_type: config 타입
            
        Returns:
            해당하는 디렉터리 이름
            
        Raises:
            ValueError: 지원하지 않는 config 타입인 경우
        """
        mapping = {
            ConfigTypes.DATASET: cls.DATASET,
            ConfigTypes.SCHEDULER: cls.SCHEDULER,
            ConfigTypes.DEFAULT_RUNTIME: cls.DEFAULT_RUNTIME,
            ConfigTypes.MODEL: cls.MODEL,
            ConfigTypes.OPTIMIZER: cls.OPTIMIZER,
            ConfigTypes.WORK: cls.WORK,
        }
        
        if config_type not in mapping:
            raise ValueError(f"지원하지 않는 config 타입: {config_type}")
        
        return mapping[config_type]


@dataclass(frozen=True)
class ConfigFileNames:
    """
    Config 파일 이름 상수 클래스
    """
    
    # 파일 이름 상수
    DATASET: str = 'dataset_config.py'
    SCHEDULER: str = 'scheduler_config.py'
    DEFAULT_RUNTIME: str = 'default_runtime_config.py'
    MODEL: str = 'model_config.py'
    OPTIMIZER: str = 'optimizer_config.py'
    WORK: str = 'work_config.py'
    
    @classmethod
    def get_file_name(cls, config_type: str) -> str:
        """
        config 타입에 해당하는 파일 이름을 반환
        
        Args:
            config_type: config 타입
            
        Returns:
            해당하는 파일 이름
            
        Raises:
            ValueError: 지원하지 않는 config 타입인 경우
        """
        mapping = {
            ConfigTypes.DATASET: cls.DATASET,
            ConfigTypes.SCHEDULER: cls.SCHEDULER,
            ConfigTypes.DEFAULT_RUNTIME: cls.DEFAULT_RUNTIME,
            ConfigTypes.MODEL: cls.MODEL,
            ConfigTypes.OPTIMIZER: cls.OPTIMIZER,
            ConfigTypes.WORK: cls.WORK,
        }
        
        if config_type not in mapping:
            raise ValueError(f"지원하지 않는 config 타입: {config_type}")
        
        return mapping[config_type] 
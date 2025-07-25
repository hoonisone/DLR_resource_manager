import os
from pathlib import Path
from typing import List, Optional, Dict
from dataclasses import dataclass, field

from ..dirdb.dirdb import DirDB


@dataclass
class ConfigDB:
    """
    Config 관리 시스템 기본 클래스
    DirDB를 기반으로 config 파일들을 관리합니다.
    """
    
    dir_db: DirDB
    # Config 파일명을 클래스 속성으로 설정
    CONFIG_NAME: str = field(default='config.py', init=False)
    

    
    def get_config_path_by_id(self, id: int, absolute: bool = False) -> Optional[Path]:
        """
        특정 ID에 해당하는 config 파일 경로를 반환
        
        Args:
            id: 찾을 ID
            absolute: True면 절대 경로, False면 상대 경로 반환
            
        Returns:
            찾은 config 파일 경로 또는 None (해당 ID가 없거나 config 파일이 없는 경우)
        """
        folder_path = self.dir_db.get_path_by_id(id, absolute=absolute)
        if folder_path is None:
            return None
        
        config_path = folder_path / self.CONFIG_NAME
        
        # 상대 경로인 경우 상대 경로로 반환
        if not absolute and isinstance(folder_path, Path):
            return config_path
        
        return config_path
    
    def get_all_config_paths(self, absolute: bool = False) -> Dict[int, Path]:
        """
        모든 ID에 대한 config 파일 경로를 반환
        
        Args:
            absolute: True면 절대 경로, False면 상대 경로 반환
            
        Returns:
            ID를 키로 하고 config 경로를 값으로 하는 딕셔너리
        """
        all_ids = self.dir_db.get_all_ids()
        config_paths = {}
        
        for id in all_ids:
            config_path = self.get_config_path_by_id(id, absolute=absolute)
            if config_path is not None:
                config_paths[id] = config_path
        
        return config_paths
    
    def exists_config(self, id: int) -> bool:
        """
        특정 ID에 해당하는 config 파일이 존재하는지 확인
        
        Args:
            id: 확인할 ID
            
        Returns:
            config 파일이 존재하면 True, 아니면 False
        """
        config_path = self.get_config_path_by_id(id, absolute=True)
        return config_path is not None and config_path.exists()
    
    def get_configs_with_missing_files(self) -> List[int]:
        """
        config 파일이 없는 ID들의 리스트를 반환
        
        Returns:
            config 파일이 없는 ID들의 리스트
        """
        all_ids = self.dir_db.get_all_ids()
        missing_configs = []
        
        for id in all_ids:
            if not self.exists_config(id):
                missing_configs.append(id)
        
        return missing_configs
    
    def create_config_file(self, id: int, config_content: str = "") -> Optional[Path]:
        """
        특정 ID에 대한 config 파일을 생성
        
        Args:
            id: config 파일을 생성할 ID
            config_content: config 파일 내용 (기본값: 빈 문자열)
            
        Returns:
            생성된 config 파일 경로 또는 None (해당 ID가 없는 경우)
        """
        folder_path = self.dir_db.get_path_by_id(id, absolute=True)
        if folder_path is None:
            return None
        
        config_path = folder_path / self.CONFIG_NAME
        
        # config 파일 생성
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        return config_path
    
    def get_dir_db(self) -> DirDB:
        """
        내부 DirDB 객체를 반환
        
        Returns:
            DirDB 객체
        """
        return self.dir_db
    
    def get_config_name(self) -> str:
        """
        Config 파일명을 반환
        
        Returns:
            Config 파일명
        """
        return self.CONFIG_NAME
    
    def create_new(self, name: Optional[str] = None) -> int:
        """
        새로운 ID를 가진 폴더를 생성하고 빈 config 파일을 만듭니다.
        
        Args:
            name: 폴더 이름 (기본값: None, 이 경우 "no_name" 사용)
            
        Returns:
            생성된 폴더의 ID
        """
        # DirDB를 사용하여 새 폴더 생성
        new_id = self.dir_db.create_folder(name=name)
        
        # 빈 config 파일 생성
        self.create_config_file(new_id, "")
        
        return new_id 
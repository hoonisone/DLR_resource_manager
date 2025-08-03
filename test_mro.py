import os
import sys
sys.path.append('src')

from pathlib import Path
from pydantic import BaseModel

class TestProperty(BaseModel):
    a: int
    b: str

from rm.db.record import PropertyRecord
PropertyRecord(dir_path=Path("test"), db=None, property_class=TestProperty) 
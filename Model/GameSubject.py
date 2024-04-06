
from pydantic import BaseModel
from typing import Optional, List

class GameSubject(BaseModel):
    title : str
    # suggested_subject : list | None = None
    subjects: Optional[List[str]] = None
    before_subjects : Optional[List[str]] = None

from pydantic import BaseModel
from typing import Optional, List

class GameSubject(BaseModel):
    selected_subject : str
    # suggested_subject : list | None = None
    suggested_subject: Optional[List[str]] = None
    before_suject : Optional[List[str]] = None
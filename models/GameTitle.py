from pydantic import BaseModel
from typing import Optional, List

class GameTitle(BaseModel):
    titles: Optional[List[str]] = None
    excluded_titles : Optional[List[str]] = None
    number : Optional[int] = 5
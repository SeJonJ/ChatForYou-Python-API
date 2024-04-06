
from pydantic import BaseModel
from typing import Optional, List

class GameTitle(BaseModel):
    titles: Optional[List[str]] = None
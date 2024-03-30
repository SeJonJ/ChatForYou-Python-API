
from pydantic import BaseModel

class GameSubject(BaseModel):
    selected_subject : str
    suggested_subject : list | None = None
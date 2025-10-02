from pydantic import BaseModel
from typing import Optional

class SurveyModel(BaseModel):
    name: str
    email: str
    age: int
    consent: bool
    rating: int
    comments: Optional[str] = None
    user_agent: Optional[str] = None
    submission_id: Optional[str] = None


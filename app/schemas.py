from pydantic import BaseModel
from typing import List, Dict


class RuleTaskCreate(BaseModel):
    name: str
    rules: List[Dict]
from typing import Any

from pydantic import BaseModel


class GenericResults(BaseModel):
    results: Any


class GenericRequest(BaseModel):
    task_id: str
    task_data: Any

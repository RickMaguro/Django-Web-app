from ninja import Schema
from typing import Optional
from datetime import datetime
from pydantic import Field, EmailStr


class TaskIn(Schema):
    email: EmailStr
    task: str
    due_by: datetime = Field(gt=datetime.now())
    priority: int
    is_urgent: Optional[bool] = False


class TaskOut(Schema):
    id: int
    email: str
    task: str
    due_by: datetime
    priority: int
    is_urgent: bool

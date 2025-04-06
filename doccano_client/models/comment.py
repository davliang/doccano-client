from typing import Optional

from pydantic import BaseModel


class Comment(BaseModel):
    id: Optional[int] = None
    text: str = ""
    example: int
    user: Optional[int] = None
    username: Optional[str] = None
    created_at: Optional[str] = None

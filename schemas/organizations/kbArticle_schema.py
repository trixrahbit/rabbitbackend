from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class KbArticleSchema(BaseModel):
    title: str
    content: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    author_id: Optional[int] = None
    tags: Optional[str] = None

    class Config:
        from_attributes = True
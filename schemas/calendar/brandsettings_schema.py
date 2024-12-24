from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BrandingSettingsBase(BaseModel):
    logo_url: Optional[str] = None
    brand_color: Optional[str] = None

class BrandingSettingsCreate(BrandingSettingsBase):
    user_id: int
    client_id: int

class BrandingSettings(BrandingSettingsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

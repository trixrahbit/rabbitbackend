from datetime import datetime

from pydantic import BaseModel


class NotificationSettingsBase(BaseModel):
    email_notifications: bool
    sms_notifications: bool

class NotificationSettingsCreate(NotificationSettingsBase):
    user_id: int

class NotificationSettings(NotificationSettingsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

class MarketingAnalyticsSchema(BaseModel):
    campaign_id: int
    impressions: int
    clicks: int
    conversions: int
    conversion_rate: float
    cost_per_click: float
    cost_per_conversion: float
    
    class Config:
        from_attributes = True
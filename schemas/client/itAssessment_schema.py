from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class ItAssessmentSchema(BaseModel):
    organization_id: int
    assessment_date: Optional[str] = None
    summary: Optional[str] = None
    detailed_findings: Optional[str] = None
    recommendations: Optional[str] = None

    class Config:
        from_attributes = True
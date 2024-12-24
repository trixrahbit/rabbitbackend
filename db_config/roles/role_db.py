from sqlalchemy.orm import Session

from models import models
from schemas import schemas


def assign_role_to_user(db: Session, assignment: schemas.UserRoleOrgCreate):
    db_assignment = models.UserRoleOrg(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

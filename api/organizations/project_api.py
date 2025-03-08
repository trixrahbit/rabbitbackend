from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.organizationModels.project_model import Project
from root.root_elements import router
from schemas.organizations.project_schema import ProjectSchema


@router.get("/{client_id}/projects", response_model=List[ProjectSchema])
def get_projects(client_id: int, db: Session = Depends(get_db)):
    projects = db.query(Project).filter(Project.client_id == client_id).all()
    return projects

@router.get("/{client_id}/projects/{project_id}", response_model=ProjectSchema)
def get_project(client_id: int, project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.client_id == client_id, Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.projects.projects_model import Project, Phase, Task, Sprint, Story
from schemas.project import project as schemas
from api.user.user_router import get_db
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    logger.info(f"Received project payload: {project.dict()}")
    db_project = Project(
        name=project.name,
        description=project.description,
        client_id=project.client_id,
        methodology=project.methodology
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    if project.methodology == "waterfall":
        for phase in project.phases:
            db_phase = Phase(
                name=phase.name,
                start_date=phase.start_date,
                end_date=phase.end_date,
                budget_hours=phase.budget_hours,
                project_id=db_project.id
            )
            db.add(db_phase)
            db.commit()
            db.refresh(db_phase)
            for task in phase.tasks:
                db_task = Task(
                    name=task.name,
                    description=task.description,
                    start_date=task.start_date,
                    end_date=task.end_date,
                    budget_hours=task.budget_hours,
                    phase_id=db_phase.id,
                    project_id=db_project.id
                )
                db.add(db_task)
            db.commit()
        for task in project.tasks:
            db_task = Task(
                name=task.name,
                description=task.description,
                start_date=task.start_date,
                end_date=task.end_date,
                budget_hours=task.budget_hours,
                project_id=db_project.id
            )
            db.add(db_task)
        db.commit()
    elif project.methodology == "agile":
        for sprint in project.sprints:
            db_sprint = Sprint(
                name=sprint.name,
                start_date=sprint.start_date,
                end_date=sprint.end_date,
                budget_hours=sprint.budget_hours,
                project_id=db_project.id
            )
            db.add(db_sprint)
            db.commit()
            db.refresh(db_sprint)
            for story in sprint.stories:
                db_story = Story(
                    name=story.name,
                    description=story.description,
                    start_date=story.start_date,
                    end_date=story.end_date,
                    budget_hours=story.budget_hours,
                    sprint_id=db_sprint.id,
                    project_id=db_project.id
                )
                db.add(db_story)
            db.commit()
        for story in project.stories:
            db_story = Story(
                name=story.name,
                description=story.description,
                start_date=story.start_date,
                end_date=story.end_date,
                budget_hours=story.budget_hours,
                project_id=db_project.id
            )
            db.add(db_story)
        db.commit()

    db.refresh(db_project)
    return db_project


@router.get("/projects/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects

@router.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    return project


@router.get("/phases/", response_model=List[schemas.Phase])
def read_phases(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    phases = db.query(Phase).offset(skip).limit(limit).all()
    return phases

@router.get("/phases/{phase_id}", response_model=schemas.Phase)
def read_phase(phase_id: int, db: Session = Depends(get_db)):
    phase = db.query(Phase).filter(Phase.id == phase_id).first()
    return phase

@router.post("/phases/", response_model=schemas.Phase)
def create_phase(phase: schemas.PhaseCreate, db: Session = Depends(get_db)):
    db_phase = Phase(**phase.dict())
    db.add(db_phase)
    db.commit()
    db.refresh(db_phase)
    return db_phase

@router.put("/phases/{phase_id}", response_model=schemas.Phase)
def update_phase(phase_id: int, phase: schemas.PhaseUpdate, db: Session = Depends(get_db)):
    db_phase = db.query(Phase).filter(Phase.id == phase_id).first()
    db_phase.name = phase.name
    db_phase.start_date = phase.start_date
    db_phase.end_date = phase.end_date
    db_phase.budget_hours = phase.budget_hours
    db.commit()
    db.refresh(db_phase)
    return db_phase


@router.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    return task


@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    db_task.name = task.name
    db_task.description = task.description
    db_task.start_date = task.start_date
    db_task.end_date = task.end_date
    db_task.budget_hours = task.budget_hours
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/sprints/", response_model=List[schemas.Sprint])
def read_sprints(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    sprints = db.query(Sprint).offset(skip).limit(limit).all()
    return sprints

@router.get("/sprints/{sprint_id}", response_model=schemas.Sprint)
def read_sprint(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    return sprint


@router.post("/sprints/", response_model=schemas.Sprint)
def create_sprint(sprint: schemas.SprintCreate, db: Session = Depends(get_db)):
    db_sprint = Sprint(**sprint.dict())
    db.add(db_sprint)
    db.commit()
    db.refresh(db_sprint)
    return db_sprint

@router.put("/sprints/{sprint_id}", response_model=schemas.Sprint)
def update_sprint(sprint_id: int, sprint: schemas.SprintUpdate, db: Session = Depends(get_db)):
    db_sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    db_sprint.name = sprint.name
    db_sprint.start_date = sprint.start_date
    db_sprint.end_date = sprint.end_date
    db_sprint.budget_hours = sprint.budget_hours
    db.commit()
    db.refresh(db_sprint)
    return db_sprint


@router.get("/stories/", response_model=List[schemas.Story])
def read_stories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    stories = db.query(Story).offset(skip).limit(limit).all()
    return stories

@router.get("/stories/{story_id}", response_model=schemas.Story)
def read_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    return story

@router.post("/stories/", response_model=schemas.Story)
def create_story(story: schemas.StoryCreate, db: Session = Depends(get_db)):
    db_story = Story(**story.dict())
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story


@router.put("/stories/{story_id}", response_model=schemas.Story)
def update_story(story_id: int, story: schemas.StoryUpdate, db: Session = Depends(get_db)):
    db_story = db.query(Story).filter(Story.id == story_id).first()

    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Update only the fields that are provided
    update_data = story.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_story, key, value)

    db.commit()
    db.refresh(db_story)
    return db_story

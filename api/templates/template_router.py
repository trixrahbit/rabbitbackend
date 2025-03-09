import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.templates.templateModel import Template, TemplatePhase, TemplateTask, TemplateSprint, TemplateStory
from root.root_elements import router
from schemas.template import template_schema as schemas
from api.user.user_router import get_db
from schemas.template.template_schema import PhaseCreate, TaskCreate, StoryCreate, SprintCreate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@router.get("/templates", response_model=List[schemas.Template])
def read_templates(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    templates = db.query(Template).order_by(Template.id).offset(skip).limit(limit).all()
    return templates



@router.post("/templates", response_model=schemas.Template)
def create_template(template: schemas.TemplateCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating template with name: {template.name}")
    db_template = Template(name=template.name, description=template.description, methodology=template.methodology)
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    logger.info(f"Created template with ID: {db_template.id}")
    return db_template


@router.get("/templates/{template_id}", response_model=schemas.Template)
def read_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(Template).filter(Template.id == template_id).first()
    if template is None:
        logger.error(f"Template with ID {template_id} not found")
        raise HTTPException(status_code=404, detail="Template not found")
    logger.info(f"Retrieved template with ID: {template_id}")
    return template


@router.put("/templates/{template_id}", response_model=schemas.Template)
def update_template(template_id: int, updated_template: schemas.TemplateCreate, db: Session = Depends(get_db)):
    template = db.query(Template).filter(Template.id == template_id).first()
    if template is None:
        logger.error(f"Template with ID {template_id} not found")
        raise HTTPException(status_code=404, detail="Template not found")

    logger.info(f"Updating template with ID: {template_id}")
    template.name = updated_template.name
    template.description = updated_template.description
    template.methodology = updated_template.methodology

    db.commit()
    db.refresh(template)

    # Update or add phases
    for phase in updated_template.phases:
        if hasattr(phase, 'id') and phase.id:
            db_phase = db.query(TemplatePhase).filter(TemplatePhase.id == phase.id).first()
            if db_phase:
                db_phase.name = phase.name
                db_phase.start_date = phase.start_date
                db_phase.end_date = phase.end_date
                db_phase.budget_hours = phase.budget_hours
                db.commit()
                db.refresh(db_phase)
                logger.info(f"Updated phase with ID: {phase.id}")
            else:
                db_phase = TemplatePhase(
                    name=phase.name,
                    start_date=phase.start_date,
                    end_date=phase.end_date,
                    budget_hours=phase.budget_hours,
                    template_id=template.id
                )
                db.add(db_phase)
                db.commit()
                db.refresh(db_phase)
                logger.info(f"Added new phase with ID: {db_phase.id}")
        else:
            db_phase = TemplatePhase(
                name=phase.name,
                start_date=phase.start_date,
                end_date=phase.end_date,
                budget_hours=phase.budget_hours,
                template_id=template.id
            )
            db.add(db_phase)
            db.commit()
            db.refresh(db_phase)
            logger.info(f"Added new phase with ID: {db_phase.id}")

        for task in phase.tasks:
            if hasattr(task, 'id') and task.id:
                db_task = db.query(TemplateTask).filter(TemplateTask.id == task.id).first()
                if db_task:
                    db_task.name = task.name
                    db_task.description = task.description
                    db_task.start_date = task.start_date
                    db_task.end_date = task.end_date
                    db_task.budget_hours = task.budget_hours
                    db_task.phase_id = db_phase.id
                    db.commit()
                    db.refresh(db_task)
                    logger.info(f"Updated task with ID: {task.id}")
                else:
                    db_task = TemplateTask(
                        name=task.name,
                        description=task.description,
                        start_date=task.start_date,
                        end_date=task.end_date,
                        budget_hours=task.budget_hours,
                        phase_id=db_phase.id,
                        template_id=template.id
                    )
                    db.add(db_task)
                    db.commit()
                    db.refresh(db_task)
                    logger.info(f"Added new task with ID: {db_task.id}")
            else:
                db_task = TemplateTask(
                    name=task.name,
                    description=task.description,
                    start_date=task.start_date,
                    end_date=task.end_date,
                    budget_hours=task.budget_hours,
                    phase_id=db_phase.id,
                    template_id=template.id
                )
                db.add(db_task)
                db.commit()
                db.refresh(db_task)
                logger.info(f"Added new task with ID: {db_task.id}")

    for task in updated_template.tasks:
        if hasattr(task, 'id') and task.id:
            db_task = db.query(TemplateTask).filter(TemplateTask.id == task.id).first()
            if db_task:
                db_task.name = task.name
                db_task.description = task.description
                db_task.start_date = task.start_date
                db_task.end_date = task.end_date
                db_task.budget_hours = task.budget_hours
                db_task.phase_id = task.phase_id
                db_task.template_id = template.id
                db.commit()
                db.refresh(db_task)
                logger.info(f"Updated task with ID: {task.id}")
            else:
                db_task = TemplateTask(
                    name=task.name,
                    description=task.description,
                    start_date=task.start_date,
                    end_date=task.end_date,
                    budget_hours=task.budget_hours,
                    phase_id=task.phase_id,
                    template_id=template.id
                )
                db.add(db_task)
                db.commit()
                db.refresh(db_task)
                logger.info(f"Added new task with ID: {db_task.id}")
        else:
            db_task = TemplateTask(
                name=task.name,
                description=task.description,
                start_date=task.start_date,
                end_date=task.end_date,
                budget_hours=task.budget_hours,
                phase_id=task.phase_id,
                template_id=template.id
            )
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            logger.info(f"Added new task with ID: {db_task.id}")

    for sprint in updated_template.sprints:
        if hasattr(sprint, 'id') and sprint.id:
            db_sprint = db.query(TemplateSprint).filter(TemplateSprint.id == sprint.id).first()
            if db_sprint:
                db_sprint.name = sprint.name
                db_sprint.start_date = sprint.start_date
                db_sprint.end_date = sprint.end_date
                db_sprint.budget_hours = sprint.budget_hours
                db_sprint.template_id = template.id
                db.commit()
                db.refresh(db_sprint)
                logger.info(f"Updated sprint with ID: {sprint.id}")
            else:
                db_sprint = TemplateSprint(
                    name=sprint.name,
                    start_date=sprint.start_date,
                    end_date=sprint.end_date,
                    budget_hours=sprint.budget_hours,
                    template_id=template.id
                )
                db.add(db_sprint)
                db.commit()
                db.refresh(db_sprint)
                logger.info(f"Added new sprint with ID: {db_sprint.id}")
        else:
            db_sprint = TemplateSprint(
                name=sprint.name,
                start_date=sprint.start_date,
                end_date=sprint.end_date,
                budget_hours=sprint.budget_hours,
                template_id=template.id
            )
            db.add(db_sprint)
            db.commit()
            db.refresh(db_sprint)
            logger.info(f"Added new sprint with ID: {db_sprint.id}")

        for story in sprint.stories:
            if hasattr(story, 'id') and story.id:
                db_story = db.query(TemplateStory).filter(TemplateStory.id == story.id).first()
                if db_story:
                    db_story.name = story.name
                    db_story.description = story.description
                    db_story.start_date = story.start_date
                    db_story.end_date = story.end_date
                    db_story.budget_hours = story.budget_hours
                    db_story.sprint_id = db_sprint.id
                    db_story.template_id = template.id
                    db.commit()
                    db.refresh(db_story)
                    logger.info(f"Updated story with ID: {story.id}")
                else:
                    db_story = TemplateStory(
                        name=story.name,
                        description=story.description,
                        start_date=story.start_date,
                        end_date=story.end_date,
                        budget_hours=story.budget_hours,
                        sprint_id=db_sprint.id,
                        template_id=template.id
                    )
                    db.add(db_story)
                    db.commit()
                    db.refresh(db_story)
                    logger.info(f"Added new story with ID: {db_story.id}")
            else:
                db_story = TemplateStory(
                    name=story.name,
                    description=story.description,
                    start_date=story.start_date,
                    end_date=story.end_date,
                    budget_hours=story.budget_hours,
                    sprint_id=db_sprint.id,
                    template_id=template.id
                )
                db.add(db_story)
                db.commit()
                db.refresh(db_story)
                logger.info(f"Added new story with ID: {db_story.id}")

    for story in updated_template.stories:
        if hasattr(story, 'id') and story.id:
            db_story = db.query(TemplateStory).filter(TemplateStory.id == story.id).first()
            if db_story:
                db_story.name = story.name
                db_story.description = story.description
                db_story.start_date = story.start_date
                db_story.end_date = story.end_date
                db_story.budget_hours = story.budget_hours
                db_story.sprint_id = story.sprint_id
                db_story.template_id = template.id
                db.commit()
                db.refresh(db_story)
                logger.info(f"Updated story with ID: {story.id}")
            else:
                db_story = TemplateStory(
                    name=story.name,
                    description=story.description,
                    start_date=story.start_date,
                    end_date=story.end_date,
                    budget_hours=story.budget_hours,
                    sprint_id=story.sprint_id,
                    template_id=template.id
                )
                db.add(db_story)
                db.commit()
                db.refresh(db_story)
                logger.info(f"Added new story with ID: {db_story.id}")
        else:
            db_story = TemplateStory(
                name=story.name,
                description=story.description,
                start_date=story.start_date,
                end_date=story.end_date,
                budget_hours=story.budget_hours,
                sprint_id=story.sprint_id,
                template_id=template.id
            )
            db.add(db_story)
            db.commit()
            db.refresh(db_story)
            logger.info(f"Added new story with ID: {db_story.id}")

    logger.info(f"Updated template with ID: {template.id}")
    return template


@router.delete("/templates/{template_id}", response_model=schemas.Template)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(Template).filter(Template.id == template_id).first()
    if template is None:
        logger.error(f"Template with ID {template_id} not found")
        raise HTTPException(status_code=404, detail="Template not found")

    db.delete(template)
    db.commit()
    logger.info(f"Deleted template with ID: {template_id}")
    return template


@router.get("/template/phases", response_model=List[schemas.Phase])
def read_template_phases(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    phases = db.query(TemplatePhase).order_by(TemplatePhase.id).offset(skip).limit(limit).all()
    return phases



@router.get("/template/phases/{phase_id}", response_model=schemas.Phase)
def read_template_phase(phase_id: int, db: Session = Depends(get_db)):
    phase = db.query(TemplatePhase).filter(TemplatePhase.id == phase_id).first()
    if phase is None:
        logger.error(f"Phase with ID {phase_id} not found")
        raise HTTPException(status_code=404, detail="Phase not found")
    logger.info(f"Retrieved phase with ID: {phase_id}")
    return phase


@router.post("/template/phases", response_model=schemas.Phase)
def create_template_phase(phase: PhaseCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating phase with name: {phase.name}")
    db_phase = TemplatePhase(**phase.dict())
    db.add(db_phase)
    db.commit()
    db.refresh(db_phase)
    logger.info(f"Created phase with ID: {db_phase.id}")
    return db_phase


@router.get("/template/tasks", response_model=List[schemas.Task])
def read_template_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(TemplateTask).order_by(TemplateTask.id).offset(skip).limit(limit).all()
    return tasks



@router.get("/template/tasks/{task_id}", response_model=schemas.Task)
def read_template_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TemplateTask).filter(TemplateTask.id == task_id).first()
    if task is None:
        logger.error(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Retrieved task with ID: {task_id}")
    return task


@router.post("/template/tasks", response_model=schemas.Task)
def create_template_task(task: TaskCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating task with name: {task.name}")
    db_task = TemplateTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info(f"Created task with ID: {db_task.id}")
    return db_task


@router.get("/template/sprints", response_model=List[schemas.Sprint])
def read_template_sprints(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    sprints = db.query(TemplateSprint).order_by(TemplateSprint.id).offset(skip).limit(limit).all()
    return sprints



@router.get("/template/sprints/{sprint_id}", response_model=schemas.Sprint)
def read_template_sprint(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(TemplateSprint).filter(TemplateSprint.id == sprint_id).first()
    if sprint is None:
        logger.error(f"Sprint with ID {sprint_id} not found")
        raise HTTPException(status_code=404, detail="Sprint not found")
    logger.info(f"Retrieved sprint with ID: {sprint_id}")
    return sprint


@router.post("/template/sprints", response_model=schemas.Sprint)
def create_template_sprint(sprint: SprintCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating sprint with name: {sprint.name}")
    db_sprint = TemplateSprint(**sprint.dict())
    db.add(db_sprint)
    db.commit()
    db.refresh(db_sprint)
    logger.info(f"Created sprint with ID: {db_sprint.id}")
    return db_sprint


@router.get("/template/stories", response_model=List[schemas.Story])
def read_template_stories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    stories = db.query(TemplateStory).order_by(TemplateStory.id).offset(skip).limit(limit).all()
    return stories



@router.get("/template/stories/{story_id}", response_model=schemas.Story)
def read_template_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(TemplateStory).filter(TemplateStory.id == story_id).first()
    if story is None:
        logger.error(f"Story with ID {story_id} not found")
        raise HTTPException(status_code=404, detail="Story not found")
    logger.info(f"Retrieved story with ID: {story_id}")
    return story


@router.post("/template/stories", response_model=schemas.Story)
def create_template_story(story: StoryCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating story with name: {story.name}")
    db_story = TemplateStory(**story.dict())
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    logger.info(f"Created story with ID: {db_story.id}")
    return db_story


@router.put("/template/phases/{phase_id}", response_model=schemas.Phase)
def update_template_phase(phase_id: int, phase: schemas.PhaseCreate, db: Session = Depends(get_db)):
    db_phase = db.query(TemplatePhase).filter(TemplatePhase.id == phase_id).first()
    if db_phase is None:
        logger.error(f"Phase with ID {phase_id} not found")
        raise HTTPException(status_code=404, detail="Phase not found")

    logger.info(f"Updating phase with ID: {phase_id}")
    db_phase.name = phase.name
    db_phase.start_date = phase.start_date
    db_phase.end_date = phase.end_date
    db_phase.budget_hours = phase.budget_hours

    db.commit()
    db.refresh(db_phase)
    logger.info(f"Updated phase with ID: {phase_id}")
    return db_phase


@router.put("/template/tasks/{task_id}", response_model=schemas.Task)
def update_template_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(TemplateTask).filter(TemplateTask.id == task_id).first()
    if db_task is None:
        logger.error(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")

    logger.info(f"Updating task with ID: {task_id}")
    db_task.name = task.name
    db_task.description = task.description
    db_task.start_date = task.start_date
    db_task.end_date = task.end_date
    db_task.budget_hours = task.budget_hours
    db_task.phase_id = task.phase_id

    db.commit()
    db.refresh(db_task)
    logger.info(f"Updated task with ID: {task_id}")
    return db_task


@router.put("/template/sprints/{sprint_id}", response_model=schemas.Sprint)
def update_template_sprint(sprint_id: int, sprint: schemas.SprintCreate, db: Session = Depends(get_db)):
    db_sprint = db.query(TemplateSprint).filter(TemplateSprint.id == sprint_id).first()
    if db_sprint is None:
        logger.error(f"Sprint with ID {sprint_id} not found")
        raise HTTPException(status_code=404, detail="Sprint not found")

    logger.info(f"Updating sprint with ID: {sprint_id}")
    db_sprint.name = sprint.name
    db_sprint.start_date = sprint.start_date
    db_sprint.end_date = sprint.end_date
    db_sprint.budget_hours = sprint.budget_hours

    db.commit()
    db.refresh(db_sprint)
    logger.info(f"Updated sprint with ID: {sprint_id}")
    return db_sprint


@router.put("/template/stories/{story_id}", response_model=schemas.Story)
def update_template_story(story_id: int, story: schemas.StoryCreate, db: Session = Depends(get_db)):
    db_story = db.query(TemplateStory).filter(TemplateStory.id == story_id).first()
    if db_story is None:
        logger.error(f"Story with ID {story_id} not found")
        raise HTTPException(status_code=404, detail="Story not found")

    logger.info(f"Updating story with ID: {story_id}")
    db_story.name = story.name
    db_story.description = story.description
    db_story.start_date = story.start_date
    db_story.end_date = story.end_date
    db_story.budget_hours = story.budget_hours
    db_story.sprint_id = story.sprint_id

    db.commit()
    db.refresh(db_story)
    logger.info(f"Updated story with ID: {story_id}")
    return db_story

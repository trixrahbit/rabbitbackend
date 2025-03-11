from fastapi import Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.clientModel.task_model import Task
from root.root_elements import router
from schemas.client.task_schema import TaskSchema



@router.get("/{client_id}/tasks", response_model=List[TaskSchema])
async def get_tasks(client_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.client_id == client_id).all()
    return tasks

@router.get("/{client_id}/tasks/{task_id}", response_model=TaskSchema)
async def get_task(client_id: int, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.client_id == client_id, Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/{client_id}/tasks", response_model=TaskSchema)
async def create_task(client_id: int, task: TaskSchema, db: Session = Depends(get_db)):
    db_task = Task(client_id=client_id, **task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/{client_id}/tasks/{task_id}", response_model=TaskSchema)
async def update_task(client_id: int, task_id: int, task: TaskSchema, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.client_id == client_id, Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{client_id}/tasks/{task_id}", response_model=TaskSchema)
async def delete_task(client_id: int, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.client_id == client_id, Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return task
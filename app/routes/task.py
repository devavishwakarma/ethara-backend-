from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate
from fastapi import HTTPException

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        title=data.title,
        project_id=data.project_id,
        assigned_to=data.assigned_to
    )
    db.add(task)
    db.commit()

    return {"message": "Task created"}

@router.put("/update/{task_id}")
def update_task(task_id: int, status: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status
    db.commit()

    return {"message": "Task updated"}

@router.get("/dashboard/{user_id}")
def dashboard(user_id: int, db: Session = Depends(get_db)):
    total = db.query(Task).filter(Task.assigned_to == user_id).count()

    completed = db.query(Task).filter(
        Task.assigned_to == user_id,
        Task.status == "completed"
    ).count()

    pending = total - completed

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending
    }
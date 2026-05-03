from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.project import Project
from app.schemas.project import ProjectCreate
from fastapi import HTTPException
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create project")

    project = Project(
        name=data.name,
        created_by=data.user_id
    )

    db.add(project)
    db.commit()

    return {"message": "Project created"}
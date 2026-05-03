from dotenv import load_dotenv
load_dotenv()  

from fastapi import FastAPI
from app.routes import auth
from app.database import Base, engine
from app.routes import project
from app.routes import task
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth")

app.include_router(project.router, prefix="/project")
app.include_router(task.router, prefix="/task")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API Running"}

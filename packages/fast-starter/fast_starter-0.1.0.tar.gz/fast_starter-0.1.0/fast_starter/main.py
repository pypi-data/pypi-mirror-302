import os
import subprocess
import sys
import argparse

def create_virtual_env(project_name):
    """Create a virtual environment and install necessary packages."""
    # Create a virtual environment
    subprocess.check_call([sys.executable, "-m", "venv", f"{project_name}/venv"])

    # Path to the pip executable
    if os.name == 'nt':  # For Windows
        pip_path = f"{project_name}/venv/Scripts/pip"
    else:  # For macOS/Linux
        pip_path = f"{project_name}/venv/bin/pip"

    # Install packages
    try:
        # Call pip to install the requirements
        subprocess.check_call([pip_path, "install", "-r", f"{project_name}/requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Error during package installation: {e}")
        sys.exit(1)

def create_fastapi_structure(project_name):
    """Create the directory structure and necessary files for a FastAPI project."""
    # Create project directories
    os.makedirs(f"{project_name}/app/models", exist_ok=True)
    os.makedirs(f"{project_name}/app/schemas", exist_ok=True)
    os.makedirs(f"{project_name}/app/crud", exist_ok=True)
    os.makedirs(f"{project_name}/alembic/versions", exist_ok=True)

    # Create app/main.py
    with open(f"{project_name}/app/main.py", "w") as f:
        f.write("""from fastapi import FastAPI
from .routes import router
from .database import engine
from .models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)
""")

    # Create app/models/user.py
    with open(f"{project_name}/app/models/user.py", "w") as f:
        f.write("""from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
""")

    # Create app/schemas/user.py
    with open(f"{project_name}/app/schemas/user.py", "w") as f:
        f.write("""from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
""")

    # Create app/crud/user.py
    with open(f"{project_name}/app/crud/user.py", "w") as f:
        f.write("""from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, email=user.email, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
""")

    # Create app/database.py
    with open(f"{project_name}/app/database.py", "w") as f:
        f.write("""from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

    # Create app/routes.py
    with open(f"{project_name}/app/routes.py", "w") as f:
        f.write("""from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import get_db

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)
""")

    # Create Alembic configuration files
    with open(f"{project_name}/alembic.ini", "w") as f:
        f.write("[alembic]\n")
        f.write("script_location = alembic\n")
        f.write("sqlalchemy.url = sqlite:///./test.db\n")

    # Create README.md
    with open(f"{project_name}/README.md", "w") as f:
        f.write(f"# {project_name}\nThis is a simple FastAPI project structure.\n")

    # Create requirements.txt
    with open(f"{project_name}/requirements.txt", "w") as f:
        f.write("fastapi\nsqlalchemy\npydantic\nalembic\n")

    # Create .env file
    with open(f"{project_name}/.env", "w") as f:
        f.write('DATABASE_URL="sqlite:///./test.db"\n')

    print(f"Project structure for '{project_name}' has been created successfully!")

def main():
    """Main function to parse arguments and create project structure."""
    parser = argparse.ArgumentParser(description="Generate FastAPI project structure")
    parser.add_argument('project_name', type=str, help="Name of the FastAPI project")
    args = parser.parse_args()

    project_name = args.project_name
    create_fastapi_structure(project_name)
    create_virtual_env(project_name)

if __name__ == "__main__":
    main()

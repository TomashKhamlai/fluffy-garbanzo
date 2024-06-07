from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config import environment

DATABASE_URL = f'sqlite:///{environment.db_name}'

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

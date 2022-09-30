from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from schemas import envs

# SQLALCHEMY_DATABASE_URL = 'postgresql://abhay4122:aaaaaaaa@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f'mysql://{envs.db_user}:{envs.db_pass}@{envs.db_host}/{envs.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
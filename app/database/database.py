from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'sqlite:///./banco_digital.db'

engine = create_engine(DATABASE_URL)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()
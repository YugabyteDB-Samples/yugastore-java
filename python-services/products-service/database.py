from sqlmodel import create_engine, SQLModel, Session
import os

# Assuming YugabyteDB (PostgreSQL compatible)
# This connection string should be updated with actual credentials/env vars
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://yugabyte:yugabyte@localhost:5433/yugabyte")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

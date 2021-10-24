from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# some configs - would be in .env or conf file
DB_URL = "sqlite:///./example_app.db"
# DB_URL = "postgresql://user:pass@server/db"

db_engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base = declarative_base()

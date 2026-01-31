from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. The URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. The Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 3. The Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Base
Base = declarative_base()
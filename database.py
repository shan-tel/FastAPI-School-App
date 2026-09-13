from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_lGzOIi76rXaP@ep-proud-sun-aezm5dkz-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit= False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
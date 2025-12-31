import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
print(f"DEBUG: Connecting to {settings.DATABASE_URL}")

engine = create_engine(settings.DATABASE_URL)


try:
    with engine.connect() as connection:
     
        connection.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful!")
except Exception as e:
    logger.error(f"❌ Database connection failed: {e}")


SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    logger.info("Creating new DB session")
    try:
        yield db
    finally:
        logger.info("Closing DB session")
        db.close()
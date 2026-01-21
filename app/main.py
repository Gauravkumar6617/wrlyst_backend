import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

# Import your local modules
from app.core.database import get_db, Base, engine
from app.model.users import Users  
from app.model.subscriber import SubscriberList
from app.api.v1.endpoint.auth import router as auth_router
from app.api.v1.endpoint.subscribers import router as subs_router
from app.api.v1.endpoint.admin import router as admin_router
from app.api.v1.endpoint.contact import router as contact_router

# Setup logging to see database errors in Render logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Lifespan event to handle database table creation
# This prevents the app from hanging on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting up: Creating database tables...")
    try:
        # This creates tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables verified/created.")
    except Exception as e:
        logger.error(f"❌ Error during startup table creation: {e}")
    
    yield  # App is now running and "Live"
    
    logger.info("Shutting down...")

# 2. Initialize FastAPI with Lifespan
app = FastAPI(
    title="Wrklyst API",
    version="1.0.0",
    lifespan=lifespan
)

# 3. Configure CORS
# Added "*" to allow_origins so your frontend can connect easily from any URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Include Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(subs_router, prefix="/api/v1")
app.include_router(contact_router, prefix="/api/v1")

# 5. Root Route (Health Check)
@app.get("/")
def root():
    return {"message": "Wrklyst API is running successfully!", "status": "online"}

# 6. Database Test Route
@app.get("/db-test")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT current_database();")).fetchone()
        return {
            "database_name": result[0],
            "status": "connected"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

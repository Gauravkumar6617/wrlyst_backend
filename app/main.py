from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import get_db, Base, engine
from app.model.users import Users  # IMPORTANT: import model
from app.api.v1.endpoint.auth import router as auth_router
from app.model.subscriber import SubscriberList
from app.api.v1.endpoint.subscribers import router as subs_router
from app.api.v1.endpoint.admin import router as admin_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wrklyst API",
    version="1.0.0"
)
origins = [
    "http://localhost:3000",
    # Add your production URL here later
]

# 2. Add the middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows Next.js to connect
    allow_credentials=True,           # Allows cookies/headers
    allow_methods=["*"],              # Allows OPTIONS, POST, GET, etc.
    allow_headers=["*"],              # Allows Content-Type, Authorization, etc.
)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(admin_router,prefix="/api/v1")
app.include_router(subs_router ,prefix="/api/v1")
@app.get("/db-test")
def test_db_connection(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT current_database();")).fetchone()
    return {
        "database_name": result[0],
        "status": "connected"
    }

# test_db.py
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:%40Gaurav6617@localhost:5432/wrklyst"
)

with engine.connect() as conn:
    print("✅ Database connected successfully")

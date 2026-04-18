# backend/test_db.py
import os
os.environ["DATABASE_URL"] = "mysql+pymysql://root:Preet%40123@localhost:3306/revai"

from analytics.models import create_tables, engine
from sqlalchemy import inspect

create_tables()
print("✅ Tables created!")

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in DB:", tables)
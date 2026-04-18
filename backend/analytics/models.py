# analytics/models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # ← ye tha hi nahi!

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:PASSWORD@localhost:3306/revai")
print(f"Connecting to: {DATABASE_URL}")  # confirm karne ke liye

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ReviewLog(Base):
    __tablename__ = "review_logs"
    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String(100), index=True)      # ← length add ki
    repo = Column(String(100), index=True)        # ← length add ki
    pr_number = Column(Integer)
    files_reviewed = Column(Integer, default=0)
    rule_violations = Column(Integer, default=0)
    secret_findings = Column(Integer, default=0)
    owasp_findings = Column(Integer, default=0)
    has_critical = Column(Integer, default=0)
    review_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ViolationLog(Base):
    __tablename__ = "violation_logs"
    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String(100))                  # ← length add ki
    repo = Column(String(100))                   # ← length add ki
    pr_number = Column(Integer)
    violation_type = Column(String(50))          # ← length add ki
    severity = Column(String(50))                # ← length add ki
    name = Column(String(200))                   # ← length add ki
    file = Column(String(200))                   # ← length add ki
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def create_tables():
    Base.metadata.create_all(bind=engine)
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None
Base = declarative_base()

class AuditTrail(Base):
    __tablename__ = 'audit_trail'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String(50))
    staff_number = Column(String(50))
    member_number = Column(String(50))
    field = Column(String(100))
    old_value = Column(Text)
    new_value = Column(Text)
    user_type = Column(String(20), default='employee')

class ChangeRequest(Base):
    __tablename__ = 'change_requests'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_number = Column(String(50))
    member_number = Column(String(50))
    member_name = Column(String(200))
    field = Column(String(100))
    old_value = Column(Text)
    new_value = Column(Text)
    remarks = Column(Text)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(30), default='pending_approval')
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    review_notes = Column(Text, nullable=True)

class ReminderQueue(Base):
    __tablename__ = 'reminder_queue'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_number = Column(String(50))
    email = Column(String(200))
    employee_name = Column(String(200))
    scheduled_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    status = Column(String(30), default='pending')

def init_db():
    if engine:
        Base.metadata.create_all(bind=engine)

def get_db():
    if SessionLocal:
        db = SessionLocal()
        try:
            return db
        except:
            db.close()
            raise
    return None

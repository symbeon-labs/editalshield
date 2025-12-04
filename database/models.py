"""
EditalShield: Database Models (SQLAlchemy ORM)
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()

# Database URL from environment or default
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "editalshield_dev")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Edital(Base):
    __tablename__ = "editals"
    
    edital_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    agency = Column(String(100))
    min_value = Column(Float)
    max_value = Column(Float)
    execution_months = Column(Integer)
    approval_rate_historical = Column(Float)
    eligible_sectors = Column(ARRAY(String))
    eligible_stages = Column(ARRAY(String))
    technical_detail_level = Column(String(20))
    evaluation_type = Column(String(50))
    full_text = Column(Text)
    criteria_json = Column(JSONB)
    is_real = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Memorial(Base):
    __tablename__ = "memorials"
    
    memorial_id = Column(Integer, primary_key=True)
    edital_id = Column(Integer)
    sector = Column(String(100))
    technology_type = Column(String(100))
    stage = Column(String(50))
    result = Column(String(50))
    original_text = Column(Text, nullable=False)
    num_words = Column(Integer)
    num_paragraphs = Column(Integer)
    is_synthetic = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ParagraphAnnotated(Base):
    __tablename__ = "paragraphs_annotated"
    
    paragraph_id = Column(Integer, primary_key=True)
    memorial_id = Column(Integer)
    paragraph_index = Column(Integer)
    original_text = Column(Text, nullable=False)
    section_type = Column(String(50))
    has_exposure = Column(Boolean, nullable=False)
    exposure_types = Column(ARRAY(String))
    entropy_value = Column(Float)
    entropy_normalized = Column(Float)
    num_sensitive_patterns = Column(Integer)
    edital_type = Column(String(20))
    rater_1_label = Column(Boolean)
    rater_2_label = Column(Boolean)
    rater_3_label = Column(Boolean)
    inter_rater_agreement = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class SensitivePattern(Base):
    __tablename__ = "sensitive_patterns"
    
    pattern_id = Column(Integer, primary_key=True)
    category = Column(String(50), nullable=False)
    pattern_text = Column(String(255), nullable=False)
    is_regex = Column(Boolean, default=False)
    weight = Column(Float)
    examples = Column(ARRAY(String))
    protection_suggestions = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.utcnow)


class MemorialProtected(Base):
    __tablename__ = "memorials_protected"
    
    protected_id = Column(Integer, primary_key=True)
    memorial_id = Column(Integer)
    protected_text = Column(Text, nullable=False)
    sensitivity_level = Column(String(20))
    risk_score_original = Column(Float)
    risk_score_protected = Column(Float)
    clarity_original = Column(Float)
    clarity_protected = Column(Float)
    num_paragraphs_modified = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class ValidationMetric(Base):
    __tablename__ = "validation_metrics"
    
    metric_id = Column(Integer, primary_key=True)
    corpus_size_memoriais = Column(Integer)
    corpus_size_paragraphs = Column(Integer)
    model_auc = Column(Float)
    model_precision = Column(Float)
    model_recall = Column(Float)
    model_f1 = Column(Float)
    inter_rater_kappa = Column(Float)
    evaluated_at = Column(DateTime, default=datetime.utcnow)


# Utility functions
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_training_data():
    """Load paragraphs for training"""
    db = SessionLocal()
    try:
        paragraphs = db.query(ParagraphAnnotated).all()
        return paragraphs
    finally:
        db.close()


def get_paragraphs_with_labels():
    """Get paragraphs with exposure labels for training"""
    db = SessionLocal()
    try:
        paragraphs = db.query(ParagraphAnnotated).all()
        data = []
        for p in paragraphs:
            data.append({
                'id': p.paragraph_id,
                'text': p.original_text,
                'entropy': p.entropy_value or 0,
                'entropy_norm': p.entropy_normalized or 0,
                'section': p.section_type,
                'patterns': p.num_sensitive_patterns or 0,
                'has_exposure': p.has_exposure
            })
        return data
    finally:
        db.close()


if __name__ == "__main__":
    print(f"Database URL: {DATABASE_URL}")
    print("Testing connection...")
    try:
        db = SessionLocal()
        count = db.query(Memorial).count()
        print(f"✓ Connected! Memorials in DB: {count}")
        db.close()
    except Exception as e:
        print(f"✗ Connection failed: {e}")

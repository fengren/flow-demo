from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RuleTask(Base):
    __tablename__ = "rule_tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rules = Column(JSON)

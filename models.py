from sqlalchemy import Column, String, Integer, Boolean, JSON, ForeignKey
from database import Base

class Suspect(Base):
    __tablename__ = "suspects"
    
    key = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    occupation = Column(String, nullable=False)
    personality = Column(String, nullable=False)
    background = Column(String, nullable=False)

class CaseTemplate(Base):
    __tablename__ = "case_templates"
    
    id = Column(String, primary_key=True, index=True)
    victim = Column(String, nullable=False)
    location = Column(String, nullable=False)
    method = Column(String, nullable=False)
    window = Column(String, nullable=False)
    motive = Column(String, nullable=False)
    murderer_key = Column(String, nullable=False)
    # JSON structure: { "chef": { "alibi": {"truth": "...", "evasive": False, "reason": None}, ...}, ... }
    suspect_facts = Column(JSON, nullable=False)

class GameSession(Base):
    __tablename__ = "game_sessions"
    
    id = Column(String, primary_key=True, index=True)
    template_id = Column(String, ForeignKey("case_templates.id"))
    questions_remaining = Column(Integer, default=5)
    solved = Column(Boolean, default=False)
    # List of {suspect, suspect_name, topic, reply}
    transcript = Column(JSON, default=list)
    # Map of suspect keys to questions asked, e.g., {"chef": 1, "librarian": 0}
    suspect_questions = Column(JSON, default=dict)

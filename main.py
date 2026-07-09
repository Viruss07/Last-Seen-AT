from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uuid
import random

from database import get_db
from models import Suspect, CaseTemplate, GameSession
from AI import interrogate

app = FastAPI(title="Last Seen At")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

MAX_QUESTIONS_PER_SUSPECT = 3
TOTAL_QUESTION_BUDGET = 15
TOPICS = ["alibi", "relationship", "saw", "rumor"]

class AskRequest(BaseModel):
    topic: str

class AccusationRequest(BaseModel):
    suspect: str
    motive_keyword: str

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

def briefing_view(session: GameSession, template: CaseTemplate, db: Session):
    suspects = db.query(Suspect).all()
    suspect_list = []
    for s in suspects:
        questions_asked = session.suspect_questions.get(s.key, 0)
        suspect_list.append({
            "key": s.key,
            "name": s.name,
            "occupation": s.occupation,
            "questions_asked": questions_asked,
            "can_ask": questions_asked < MAX_QUESTIONS_PER_SUSPECT
        })
    
    return {
        "id": session.id,
        "victim": template.victim,
        "location": template.location,
        "window": template.window,
        "questions_remaining": session.questions_remaining,
        "transcript": session.transcript,
        "solved": session.solved,
        "suspects": suspect_list
    }

def reveal_view(template: CaseTemplate):
    return {
        "murderer": template.murderer_key,
        "motive": template.motive,
        "method": template.method,
        "truth": template.suspect_facts
    }

@app.post("/cases")
def create_case(db: Session = Depends(get_db)):
    templates = db.query(CaseTemplate).all()
    if not templates:
        raise HTTPException(status_code=500, detail="No cases available in database. Run seed_data.py")
    
    template = random.choice(templates)
    
    session_id = str(uuid.uuid4())
    game_session = GameSession(
        id=session_id,
        template_id=template.id,
        questions_remaining=TOTAL_QUESTION_BUDGET,
        solved=False,
        transcript=[],
        suspect_questions={}
    )
    db.add(game_session)
    db.commit()
    db.refresh(game_session)
    
    return briefing_view(game_session, template, db)

@app.get("/cases/{case_id}")
def get_case(case_id: str, db: Session = Depends(get_db)):
    game_session, template = _get_case_or_404(case_id, db)
    return briefing_view(game_session, template, db)

@app.get("/topics")
def get_topics():
    return {
        "topics": [
            {"key": "alibi", "label": "Where were you during the murder?"},
            {"key": "relationship", "label": "What was your relationship with the victim?"},
            {"key": "saw", "label": "Did you see or hear anything unusual?"},
            {"key": "rumor", "label": "Know anything about what the others were doing?"},
        ]
    }

@app.post("/cases/{case_id}/suspects/{suspect_key}/ask")
def ask(case_id: str, suspect_key: str, data: AskRequest, db: Session = Depends(get_db)):
    game_session, template = _get_case_or_404(case_id, db)
    suspect = db.query(Suspect).filter(Suspect.key == suspect_key).first()

    if not suspect:
        raise HTTPException(status_code=404, detail="No such suspect")
    if data.topic not in TOPICS:
        raise HTTPException(status_code=400, detail=f"Topic must be one of {TOPICS}")
    if game_session.solved:
        raise HTTPException(status_code=400, detail="This case is already closed")

    # In PostgreSQL JSON columns, modifying inner dict requires a copy to detect change or assigning new dict
    suspect_questions = dict(game_session.suspect_questions)
    questions_asked = suspect_questions.get(suspect_key, 0)

    if game_session.questions_remaining <= 0:
        raise HTTPException(status_code=400, detail="No questions remaining this case")
    if questions_asked >= MAX_QUESTIONS_PER_SUSPECT:
        raise HTTPException(status_code=400, detail="Already asked this suspect the maximum questions")

    reply = interrogate(template, suspect, data.topic)

    suspect_questions[suspect_key] = questions_asked + 1
    game_session.suspect_questions = suspect_questions
    game_session.questions_remaining -= 1
    
    transcript = list(game_session.transcript)
    transcript.append(
        {"suspect": suspect_key, "suspect_name": suspect.name, "topic": data.topic, "reply": reply}
    )
    game_session.transcript = transcript
    
    db.commit()

    return {
        "suspect": suspect.name,
        "topic": data.topic,
        "reply": reply,
        "questions_remaining": game_session.questions_remaining,
        "suspect_questions_remaining": MAX_QUESTIONS_PER_SUSPECT - (questions_asked + 1),
    }

@app.post("/cases/{case_id}/accuse")
def accuse(case_id: str, data: AccusationRequest, db: Session = Depends(get_db)):
    game_session, template = _get_case_or_404(case_id, db)
    suspect = db.query(Suspect).filter(Suspect.key == data.suspect).first()

    if not suspect:
        raise HTTPException(status_code=404, detail="No such suspect")

    correct_suspect = data.suspect == template.murderer_key
    correct_motive = data.motive_keyword.strip().lower() in template.motive.lower()
    game_session.solved = True
    db.commit()

    return {
        "correct_suspect": correct_suspect,
        "correct_motive": correct_motive,
        "questions_used": TOTAL_QUESTION_BUDGET - game_session.questions_remaining,
        "reveal": reveal_view(template),
    }

def _get_case_or_404(case_id: str, db: Session):
    game_session = db.query(GameSession).filter(GameSession.id == case_id).first()
    if not game_session:
        raise HTTPException(status_code=404, detail="No such case")
    template = db.query(CaseTemplate).filter(CaseTemplate.id == game_session.template_id).first()
    return game_session, template

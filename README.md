# Last Seen At

**Last Seen At** is an AI-powered murder mystery and deduction game. Step into the shoes of a detective to interrogate suspects, gather evidence, cross-reference alibis, and make a final accusation to solve the case.

The game is designed with a noir aesthetic and a focus on narrative-driven gameplay, ensuring players experience a satisfying "aha!" moment when piecing together the clues.

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL
- **AI Integration:** LLM-powered suspect interrogation and dynamic responses
- **Frontend:** HTML/CSS/JS (Vanilla)

## Setup & Running Locally

1. **Prerequisites:**
   - Python 3.10+
   - PostgreSQL
   - An API key for the language model (configured via environment variables or `config.py`)

2. **Installation:**
   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Running the Server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Play the Game:**
   Open your browser and navigate to `http://localhost:8000/`.

## Gameplay

1. **Archive:** Review past cases or start a new investigation.
2. **Briefing:** Read the case file, victim details, and crime scene information.
3. **Investigation:** Interrogate suspects using a limited question budget. Take notes and review the evidence board.
4. **Accusation:** Once you have gathered enough clues, make your final accusation and see if your deduction holds up!

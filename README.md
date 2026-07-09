# Last Seen At

**Last Seen At** is an AI-powered murder mystery and deduction game. Step into the shoes of a detective to interrogate suspects, gather evidence, cross-reference alibis, and make a final accusation to solve the case.

The game is designed with a noir aesthetic and a focus on narrative-driven gameplay, ensuring players experience a satisfying "aha!" moment when piecing together the clues.

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL
- **AI Integration:** LLM-powered suspect interrogation and dynamic responses
- **Frontend:** HTML/CSS/JS (Vanilla)

## Detailed Setup & Installation Guide

Follow these steps to download the repository, configure the necessary services, and run the game on your local machine.

### 1. Clone the Repository

First, download the source code to your machine using Git:

```bash
git clone https://github.com/Viruss07/Last-Seen-AT.git
cd Last-Seen-AT
```

### 2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage Python dependencies and avoid conflicting with system-wide packages.

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

With the virtual environment activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Database Configuration (PostgreSQL)

The game requires PostgreSQL to store session histories, suspects, and transcripts.

1. Ensure PostgreSQL is installed and running on your system.
2. The game expects a database named `last_seen_at` running locally on port `5432` by default. You can create it using the `psql` command-line tool:

```bash
# Example using psql
psql -U postgres -c "CREATE DATABASE last_seen_at;"
```

*Note: If you have a different PostgreSQL setup (e.g., specific username/password), update the `DATABASE_URL` string inside `database.py`.*

### 5. API Key Configuration

Since this game relies on an LLM for character interrogation, you must provide a valid API key.

Open `config.py` in the root directory and ensure your key is configured, or export it in your terminal before running the server:

```bash
export API_KEY="your-actual-api-key"
```

### 6. Start the Server

Run the FastAPI backend using `uvicorn`:

```bash
uvicorn main:app --reload --port 8000
```
*(The `--reload` flag automatically restarts the server if you make changes to the code).*

### 7. Play the Game

Open your favorite web browser and navigate to:

👉 **[http://localhost:8000/](http://localhost:8000/)**

## Gameplay

1. **Archive:** Review past cases or start a new investigation.
2. **Briefing:** Read the case file, victim details, and crime scene information.
3. **Investigation:** Interrogate suspects using a limited question budget. Take notes and review the evidence board.
4. **Accusation:** Once you have gathered enough clues, make your final accusation and see if your deduction holds up!

# Doremon.ai — Python-powered learning gadgets

Children use an interactive website with a robot teacher, Fraction Pizza, Planet Explorer, Story Spark, Brain Boost, and a Python-powered quiz service. Python is used **behind the scenes**, not taught to children.

## Architecture
- Frontend: HTML, CSS, JavaScript on GitHub Pages.
- Backend: FastAPI in `backend/main.py`.
- `POST /api/ask`: topic classification, curated explanations, and gadget recommendations.
- `POST /api/quiz`: randomized questions with answers and explanations.
- `GET /health`: health check.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8001
```

In a second terminal, run `python3 -m http.server 8000` from the repository root. Visit http://localhost:8000. The browser will call the Python API at localhost:8001.

## Deploy
GitHub Pages serves the frontend only. Deploy the backend separately to a Python host using `pip install -r backend/requirements.txt` and `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`. Set the backend environment variable `ALLOWED_ORIGINS` to `https://aashish-siingh.github.io`. Edit `config.js` to specify the backend's public HTTPS URL. Without a deployed backend, the existing browser-based gadgets still work, while API features show an offline message.

## Test
Install `pytest` and `httpx`, then run `pytest backend/test_main.py`.

## Scope
The backend is functional rule-based Python, **not a generative AI model**. The prototype stores no child accounts or personal information. Production deployment for children needs safety, privacy, and security review. The mascot is original, not an official Doraemon character.

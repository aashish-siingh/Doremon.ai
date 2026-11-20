"""Doremon.ai educational API. Run: uvicorn backend.main:app --reload"""
import os
import re
from random import choice
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Doremon.ai Learning API", version="1.0.0")
origins = [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000,https://aashish-siingh.github.io").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=500)

class QuizRequest(BaseModel):
    topic: str = Field(default="general", max_length=40)
    count: int = Field(default=5, ge=1, le=10)

TOPICS = {
    "math": {"terms": ("math", "fraction", "divide", "multiply", "number", "addition", "subtract", "percent"), "gadget": "math", "intro": "Let's solve it one step at a time! Fractions are equal parts of a whole. Imagine sharing a pizza with friends.", "hint": "Try the Fraction Pizza gadget. Start with four equal slices and select one."},
    "science": {"terms": ("planet", "space", "solar", "earth", "sun", "science", "gravity", "moon"), "gadget": "science", "intro": "Science starts with curiosity! The Sun's gravity helps keep planets in orbit.", "hint": "Visit Planet Explorer and compare the eight planets."},
    "writing": {"terms": ("story", "write", "creative", "imagine", "character", "essay"), "gadget": "story", "intro": "Every story needs a character, a setting, and a challenge. Let's invent an adventure!", "hint": "Open Story Spark, choose a hero and a place, and write your own ending."},
    "study": {"terms": ("study", "quiz", "remember", "exam", "test", "learn"), "gadget": "quiz", "intro": "Learning is easier in small steps. Try answering a question, then explain why your answer makes sense.", "hint": "Use Brain Boost for practice and try again if you miss a question."},
}
QUESTION_BANK = [
    {"topic": "math", "question": "What is 6 × 3?", "options": ["9", "18", "63"], "answer": 1, "explanation": "Six groups of three make eighteen."},
    {"topic": "math", "question": "What is half of 14?", "options": ["7", "6", "28"], "answer": 0, "explanation": "Fourteen split into two equal groups gives seven."},
    {"topic": "math", "question": "What is 25% of 20?", "options": ["10", "5", "4"], "answer": 1, "explanation": "25% means one quarter, and one quarter of 20 is 5."},
    {"topic": "math", "question": "What is 9 + 8?", "options": ["17", "18", "16"], "answer": 0, "explanation": "Nine plus eight equals seventeen."},
    {"topic": "science", "question": "Which planet is closest to the Sun?", "options": ["Earth", "Mercury", "Mars"], "answer": 1, "explanation": "Mercury is closest to the Sun."},
    {"topic": "science", "question": "What do plants need for photosynthesis?", "options": ["Sunlight", "Moonlight", "Sand only"], "answer": 0, "explanation": "Plants use sunlight, water, and carbon dioxide."},
    {"topic": "science", "question": "What force pulls things toward Earth?", "options": ["Magnetism", "Gravity", "Sound"], "answer": 1, "explanation": "Gravity pulls objects toward Earth's center."},
    {"topic": "science", "question": "What is the largest planet?", "options": ["Saturn", "Jupiter", "Neptune"], "answer": 1, "explanation": "Jupiter is the largest planet in our solar system."},
    {"topic": "writing", "question": "What is the setting of a story?", "options": ["Where and when it happens", "The author's name", "The last sentence"], "answer": 0, "explanation": "A setting describes a story's time and place."},
    {"topic": "writing", "question": "Which word is an adjective?", "options": ["Run", "Bright", "Quickly"], "answer": 1, "explanation": "Bright describes a noun."},
    {"topic": "general", "question": "How many days are in a week?", "options": ["5", "7", "10"], "answer": 1, "explanation": "A week has seven days."},
    {"topic": "general", "question": "Which animal is a mammal?", "options": ["Dolphin", "Shark", "Salmon"], "answer": 0, "explanation": "Dolphins are mammals that breathe air."},
]

@app.get("/health")
def health():
    return {"status": "ok", "service": "doremon-ai"}

@app.post("/api/ask")
def ask(request: AskRequest):
    text = request.question.lower()
    selected = next((key for key, data in TOPICS.items() if any(re.search(r"\b" + re.escape(term) + r"\b", text) for term in data["terms"])), None)
    if not selected:
        return {"topic": "general", "gadget": "quiz", "reply": "That's an interesting question! I don't have a reliable explanation for that topic yet. Let's practice with a learning game, or ask a teacher or trusted adult.", "hint": "Try Brain Boost for a new challenge.", "source": "curated"}
    data = TOPICS[selected]
    return {"topic": selected, "gadget": data["gadget"], "reply": data["intro"], "hint": data["hint"], "source": "curated"}

@app.post("/api/quiz")
def quiz(request: QuizRequest):
    topic = request.topic.lower()
    questions = [q for q in QUESTION_BANK if q["topic"] == topic] if topic != "general" else QUESTION_BANK
    if not questions:
        questions = QUESTION_BANK
    from random import sample
    return {"questions": sample(questions, min(request.count, len(questions)))}

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from fastapi import HTTPException

connection = sqlite3.connect("database.db", check_same_thread=False)
cursor = connection.cursor()

app = FastAPI()

ALLOWED_COUNTRIES = [
    "Slovakia",
    "Czech Republic",
    "Germany",
    "Austria",
    "Poland",
    "Hungary"
]

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    country TEXT,
    score INTEGER
)
""")
connection.commit()

class Score(BaseModel):
    name: str
    country: str
    score: int


@app.post("/score")
def add_score(data: Score):
    if data.country not in ALLOWED_COUNTRIES:
        raise HTTPException(status_code=400, detail="Invalid country")

    cursor.execute(
        "INSERT INTO scores (name, country, score) VALUES (?, ?, ?)",
        (data.name, data.country, data.score)
    )
    connection.commit()

    return {"status": "ok"}


@app.get("/leaderboard")
def get_leaderboard():
    cursor.execute(
        "SELECT name, country, score FROM scores ORDER BY score DESC LIMIT 10"
    )
    rows = cursor.fetchall()

    return [
        {"name": r[0], "country": r[1], "score": r[2]}
        for r in rows
    ]

@app.get("/countries")
def get_countries():
    return ALLOWED_COUNTRIES

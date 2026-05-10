from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
import os
from sqlalchemy import create_engine, text
from sqlalchemy import text


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

app = FastAPI()

ALLOWED_COUNTRIES = [
    "Slovakia",
    "Czech Republic",
    "Germany",
    "Austria",
    "Poland",
    "Hungary"
]

class Score(BaseModel):
    name: str
    country: str
    score: int


@app.post("/score")
def add_score(data: Score):
    if data.country not in ALLOWED_COUNTRIES:
        raise HTTPException(status_code=400, detail="Invalid country")

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO scores (name, country, score)
                VALUES (:name, :country, :score)
            """),
            {
                "name": data.name,
                "country": data.country,
                "score": data.score
            }
        )
        conn.commit()
    return {"status": "ok"}


from sqlalchemy import text

@app.get("/leaderboard")
def get_leaderboard():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT name, country, score
                FROM scores
                ORDER BY score DESC
                LIMIT 10
            """)
        )
        rows = result.fetchall()

    return [
        {"name": r[0], "country": r[1], "score": r[2]}
        for r in rows
    ]

@app.get("/countries")
def get_countries():
    return ALLOWED_COUNTRIES

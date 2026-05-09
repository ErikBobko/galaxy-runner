import requests
BASE_URL = "http://127.0.0.1:8000"

def send_score(name, country, score):
    try:
        res = requests.post(
            "http://127.0.0.1:8000/score",
            json={
                "name": name,
                "country": country,
                "score": score
            }
        )
        print("STATUS:", res.status_code)
    except Exception as e:
        print("ERROR:", e)


def get_leaderboard():
    try:
        res = requests.get(f"{BASE_URL}/leaderboard")
        return res.json()
    except Exception as e:
        print("GET LEADERBOARD ERROR:", e)
        return []

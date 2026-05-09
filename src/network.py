import requests
BASE_URL = "https://galaxy-runner.onrender.com"

def send_score(name, country, score):
    try:
        res = requests.post(
            f"{BASE_URL}/score",
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

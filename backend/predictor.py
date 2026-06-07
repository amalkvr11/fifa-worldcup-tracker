import math
import random

TEAM_STRENGTH = {
    "ARG": 98, "BRA": 97, "FRA": 96, "ENG": 95, "ESP": 94,
    "GER": 93, "NED": 92, "POR": 91, "BEL": 90, "ITA": 89,
    "CRO": 87, "URU": 86, "USA": 84, "MEX": 83, "JPN": 82,
    "MAR": 81, "SEN": 80, "SUI": 79, "COL": 78, "DEN": 77,
    "KOR": 76, "AUS": 75, "ECU": 74, "NGA": 73, "CMR": 72,
    "GHA": 71, "EGY": 70, "TUN": 69, "CIV": 68, "ALG": 67,
    "CRC": 66, "PAN": 65, "KSA": 64, "IRN": 63, "NZL": 62,
    "CAN": 61, "JAM": 60, "MLI": 59, "BFA": 58, "RSA": 57,
    "CHI": 56, "SRB": 55, "IRQ": 54, "IND": 53, "CHN": 52,
    "UZB": 51, "TAH": 40, "FIJ": 38,
}

def expected_score(rating_a, rating_b):
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))

def predict_match(team1_code, team2_code, team1_goals=None, team2_goals=None):
    s1 = TEAM_STRENGTH.get(team1_code, 50)
    s2 = TEAM_STRENGTH.get(team2_code, 50)

    s1 += random.uniform(-3, 3)
    s2 += random.uniform(-3, 3)

    exp1 = expected_score(s1, s2)
    exp2 = 1.0 - exp1

    win_prob = round(exp1 * 100, 1)
    draw_prob = round((1 - abs(exp1 - exp2)) * 30, 1)
    lose_prob = round(100 - win_prob - draw_prob, 1)

    if team1_goals is not None and team2_goals is not None:
        if team1_goals > team2_goals:
            actual = team1_code
        elif team2_goals > team1_goals:
            actual = team2_code
        else:
            actual = "draw"
    else:
        actual = None

    return {
        "team1": team1_code,
        "team2": team2_code,
        "strength1": round(s1, 1),
        "strength2": round(s2, 1),
        "win_probability": f"{win_prob}%",
        "draw_probability": f"{draw_prob}%",
        "lose_probability": f"{lose_prob}%",
        "predicted_winner": team1_code if win_prob > 50 else team2_code if win_prob < 50 else "draw",
        "confidence": "high" if abs(win_prob - lose_prob) > 30 else "medium",
    }

def predict_tournament_winner():
    top_teams = ["ARG", "BRA", "FRA", "ENG", "ESP", "GER", "NED", "POR"]
    weights = [TEAM_STRENGTH.get(t, 50) ** 2 for t in top_teams]
    total = sum(weights)
    probs = {t: round(w / total * 100, 1) for t, w in zip(top_teams, weights)}
    winner = max(probs, key=probs.get)
    return {
        "predictions": dict(sorted(probs.items(), key=lambda x: -x[1])),
        "favorite": winner,
        "favorite_name": {"ARG": "Argentina", "BRA": "Brazil", "FRA": "France",
                         "ENG": "England", "ESP": "Spain", "GER": "Germany",
                         "NED": "Netherlands", "POR": "Portugal"}.get(winner, winner),
    }

GROUP_PREDICTIONS = {}

def predict_group(group_code, teams):
    rated = [(t, TEAM_STRENGTH.get(t["code"], 50)) for t in teams]
    rated.sort(key=lambda x: -x[1])
    return [
        {"code": t["code"], "name": t["name"], "flag": t["flag"],
         "strength": s, "predicted_position": i + 1,
         "qualify": i < 2}
        for i, (t, s) in enumerate(rated)
    ]

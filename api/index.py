import os, sys, threading, time, random
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

app = FastAPI(title="FIFA World Cup 2026 API")

app.add_middleware(
    __import__("starlette.middleware.cors", fromlist=["CORSMiddleware"]).CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/matches")
def get_matches():
    from data import ALL_MATCHES
    return {"matches": ALL_MATCHES, "total": len(ALL_MATCHES)}

@app.get("/api/matches/{mid}")
def get_match(mid: int):
    from data import ALL_MATCHES
    m = next((x for x in ALL_MATCHES if x["id"] == mid), None)
    if not m:
        return JSONResponse({"error": "Not found"}, status_code=404)
    return m

@app.get("/api/teams")
def get_teams():
    from data import ALL_TEAMS
    return list(ALL_TEAMS.values())

@app.get("/api/teams/{code}")
def get_team(code: str):
    from data import ALL_TEAMS
    t = ALL_TEAMS.get(code.upper())
    if not t:
        return JSONResponse({"error": "Not found"}, status_code=404)
    return t

@app.get("/api/teams/{code}/players")
def get_players(code: str):
    from data import SQUAD_DATA
    return {"team_code": code.upper(), "players": SQUAD_DATA.get(code.upper(), [])}

@app.get("/api/groups")
def get_groups():
    from data import ALL_TEAMS
    groups = {}
    for t in ALL_TEAMS.values():
        g = t["group"]
        groups.setdefault(g, []).append({"code": t["code"], "name": t["name"], "flag": t["flag"]})
    return groups

@app.get("/api/standings/{group}")
def get_standings(group: str):
    from data import TEAMS, ALL_MATCHES
    grp = group.upper()
    gt = [t for t in TEAMS if t["group"] == grp]
    if not gt:
        return JSONResponse({"error": "Not found"}, status_code=404)
    res = []
    for t in gt:
        ms = [m for m in ALL_MATCHES if m["stage"] == "Group Stage" and m["group"] == grp
              and (m["team1_code"] == t["code"] or m["team2_code"] == t["code"])]
        p = w = d = l = gf = ga = 0
        for m in ms:
            s1 = m.get("score_team1") or 0
            s2 = m.get("score_team2") or 0
            if m["team1_code"] == t["code"]:
                gf += s1; ga += s2
                if s1 > s2: w += 1
                elif s1 == s2: d += 1
                else: l += 1
            else:
                gf += s2; ga += s1
                if s2 > s1: w += 1
                elif s2 == s1: d += 1
                else: l += 1
        res.append({
            "code": t["code"], "name": t["name"], "flag": t["flag"],
            "played": p, "won": w, "drawn": d, "lost": l,
            "gf": gf, "ga": ga, "gd": gf - ga, "points": w * 3 + d,
        })
    res.sort(key=lambda x: (-x["points"], -x["gd"], -x["gf"]))
    return {"group": grp, "standings": res}

@app.get("/api/predict/match/{mid}")
def predict_match(mid: int):
    from data import ALL_MATCHES
    from predictor import predict_match as pm
    m = next((x for x in ALL_MATCHES if x["id"] == mid), None)
    if not m:
        return JSONResponse({"error": "Not found"}, status_code=404)
    return pm(m["team1_code"], m["team2_code"])

@app.get("/api/predict/tournament")
def predict_tournament():
    from predictor import predict_tournament_winner
    return predict_tournament_winner()

@app.get("/api/predict/strengths")
def get_strengths():
    from data import TEAMS
    from predictor import TEAM_STRENGTH
    return {
        t["code"]: {"name": t["name"], "flag": t["flag"],
                    "strength": TEAM_STRENGTH.get(t["code"], 50), "group": t["group"]}
        for t in sorted(TEAMS, key=lambda x: -TEAM_STRENGTH.get(x["code"], 50))
    }

@app.get("/api/predict/group/{group}")
def predict_group(group: str):
    from data import TEAMS
    from predictor import predict_group as pg
    grp = group.upper()
    gt = [t for t in TEAMS if t["group"] == grp]
    if not gt:
        return JSONResponse({"error": "Not found"}, status_code=404)
    return {"group": grp, "predictions": pg(grp, gt)}

@app.post("/api/chat")
def chat(body: dict):
    from chatbot import get_response
    return {"reply": get_response(body.get("message", ""))}

scores = {}
events = {}

@app.post("/api/live/start/{mid}")
def start_live(mid: int):
    from data import ALL_MATCHES
    from predictor import TEAM_STRENGTH
    m = next((x for x in ALL_MATCHES if x["id"] == mid), None)
    if not m:
        return JSONResponse({"error": "Not found"}, status_code=404)
    scores[mid] = {"score_team1": 0, "score_team2": 0, "status": "live"}
    events[mid] = []
    s1 = TEAM_STRENGTH.get(m["team1_code"], 50)
    s2 = TEAM_STRENGTH.get(m["team2_code"], 50)
    GOAL = ["Goal!", "What a strike!", "Finds the net!", "Powerful shot!"]

    def sim():
        minute = 0
        while minute < 90:
            time.sleep(random.uniform(1.5, 4.0))
            minute += random.randint(1, 3)
            if minute > 90:
                minute = 90
            total = s1 + s2
            ev = random.random()
            if ev < 0.10 * (s1 / total * 2):
                scores[mid]["score_team1"] += 1
                events[mid].append({"minute": minute, "text": random.choice(GOAL), "type": "goal"})
            elif ev < 0.10 * (s1 / total * 2) + 0.10 * (s2 / total * 2):
                scores[mid]["score_team2"] += 1
                events[mid].append({"minute": minute, "text": random.choice(GOAL), "type": "goal"})
            elif ev < 0.16:
                events[mid].append({"minute": minute, "text": "Yellow card", "type": "card"})
        scores[mid]["status"] = "finished"
        events[mid].append({"minute": 90, "text": "Full time!", "type": "info"})

    t = threading.Thread(target=sim, daemon=True)
    t.start()
    return {"status": "started", "match_id": mid}

@app.get("/api/live/status/{mid}")
def live_status(mid: int):
    ls = scores.get(mid, {})
    return {
        "match_id": mid,
        "score_team1": ls.get("score_team1"),
        "score_team2": ls.get("score_team2"),
        "status": ls.get("status", "upcoming"),
        "events": events.get(mid, [])[-10:],
    }

@app.get("/api/live/active")
def active_live():
    out = []
    for mid, ls in scores.items():
        if ls.get("status") == "live":
            from data import ALL_MATCHES
            m = next((x for x in ALL_MATCHES if x["id"] == mid), None)
            if m:
                out.append({
                    "match_id": mid, "team1": m["team1"], "team2": m["team2"],
                    "score_team1": ls["score_team1"], "score_team2": ls["score_team2"],
                })
    return {"active": out}

fd = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(fd):
    app.mount("/", StaticFiles(directory=fd, html=True), name="frontend")

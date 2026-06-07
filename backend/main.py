import asyncio
import json
import random
from datetime import datetime, timezone
from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from data import ALL_MATCHES, ALL_TEAMS, TEAMS, SQUAD_DATA
from models import Match, Team, MatchResponse, ChatRequest, ChatResponse, PredictionRequest, FavoriteRequest, Player
from predictor import predict_match, predict_tournament_winner, predict_group, TEAM_STRENGTH
from chatbot import get_response

app = FastAPI(title="FIFA World Cup 2026 API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

favorites: dict[str, int] = {}
match_favorites: dict[int, int] = {}

live_scores: dict[int, dict] = {}
live_events: dict[int, list] = {}
score_simulations: dict[int, asyncio.Task] = {}

connected_clients: list[WebSocket] = []


def get_ist_offset():
    return 5 * 60 + 30


def match_to_dict(m):
    d = dict(m)
    d["favorite_count"] = match_favorites.get(m["id"], 0)
    ls = live_scores.get(m["id"])
    if ls:
        d["score_team1"] = ls["score_team1"]
        d["score_team2"] = ls["score_team2"]
        d["status"] = ls.get("status", m["status"])
    return d


def get_match_by_id(match_id: int):
    for m in ALL_MATCHES:
        if m["id"] == match_id:
            return m
    return None


# ── REST Endpoints ──────────────────────────────────────────

@app.get("/api/matches", response_model=MatchResponse)
def get_matches(
    date: str | None = Query(None),
    team: str | None = Query(None),
    stage: str | None = Query(None),
    group: str | None = Query(None),
):
    result = [match_to_dict(m) for m in ALL_MATCHES]
    if date:
        result = [m for m in result if m["date_utc"][:10] == date]
    if team:
        result = [m for m in result if m["team1_code"] == team or m["team2_code"] == team]
    if stage:
        result = [m for m in result if m["stage"] == stage]
    if group:
        result = [m for m in result if m["group"] == group]
    return MatchResponse(matches=result, total=len(result))


@app.get("/api/matches/{match_id}")
def get_match(match_id: int):
    m = get_match_by_id(match_id)
    if not m:
        return {"error": "Match not found"}, 404
    return match_to_dict(m)


@app.get("/api/teams", response_model=list[Team])
def get_teams(limit: int | None = Query(None)):
    result = [Team(**t) for t in ALL_TEAMS.values()]
    if limit:
        result = result[:limit]
    return result


@app.get("/api/teams/{code}")
def get_team(code: str):
    t = ALL_TEAMS.get(code)
    if not t:
        return {"error": "Team not found"}, 404
    return Team(**t)


@app.get("/api/teams/{code}/players")
def get_team_players(code: str):
    players = SQUAD_DATA.get(code.upper(), [])
    if not players and code.upper() not in ALL_TEAMS:
        return {"error": "Team not found"}, 404
    return {"team_code": code.upper(), "players": players}


@app.post("/api/favorites")
def add_favorite(req: FavoriteRequest):
    favorites[req.team_code] = favorites.get(req.team_code, 0) + 1
    return {"team_code": req.team_code, "count": favorites[req.team_code]}


@app.get("/api/favorites")
def get_favorites():
    return dict(sorted(favorites.items(), key=lambda x: -x[1]))


@app.get("/api/today")
def get_today_matches():
    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")
    result = [match_to_dict(m) for m in ALL_MATCHES if m["date_utc"][:10] == today_str]
    return MatchResponse(matches=result, total=len(result))


@app.get("/api/dates")
def get_match_dates():
    dates = sorted(set(m["date_utc"][:10] for m in ALL_MATCHES))
    return {"dates": dates}


@app.get("/api/groups")
def get_groups():
    groups: dict[str, list[dict]] = {}
    for t in ALL_TEAMS.values():
        g = t["group"]
        if g not in groups:
            groups[g] = []
        groups[g].append({"code": t["code"], "name": t["name"], "flag": t["flag"]})
    return groups


@app.get("/api/standings/{group}")
def get_group_standings(group: str):
    if group not in {t["group"] for t in ALL_TEAMS.values()}:
        return {"error": "Group not found"}, 404
    group_teams = [t for t in TEAMS if t["group"] == group]
    standings = []
    for t in group_teams:
        team_matches = [
            m for m in ALL_MATCHES
            if m["stage"] == "Group Stage" and m["group"] == group
            and (m["team1_code"] == t["code"] or m["team2_code"] == t["code"])
        ]
        played = won = drawn = lost = gf = ga = 0
        for m in team_matches:
            s1 = live_scores.get(m["id"], {}).get("score_team1", m["score_team1"])
            s2 = live_scores.get(m["id"], {}).get("score_team2", m["score_team2"])
            if s1 is not None and s2 is not None:
                played += 1
                if m["team1_code"] == t["code"]:
                    gf += s1; ga += s2
                    if s1 > s2: won += 1
                    elif s1 == s2: drawn += 1
                    else: lost += 1
                else:
                    gf += s2; ga += s1
                    if s2 > s1: won += 1
                    elif s2 == s1: drawn += 1
                    else: lost += 1
        points = won * 3 + drawn
        standings.append({
            "code": t["code"], "name": t["name"], "flag": t["flag"],
            "played": played, "won": won, "drawn": drawn, "lost": lost,
            "gf": gf, "ga": ga, "gd": gf - ga, "points": points,
        })
    standings.sort(key=lambda x: (-x["points"], -x["gd"], -x["gf"]))
    return {"group": group, "standings": standings}


# ── AI Prediction Endpoints ─────────────────────────────────

@app.get("/api/predict/match/{match_id}")
def predict_match_api(match_id: int):
    m = get_match_by_id(match_id)
    if not m:
        return {"error": "Match not found"}, 404
    ls = live_scores.get(match_id)
    return predict_match(
        m["team1_code"], m["team2_code"],
        ls["score_team1"] if ls else None,
        ls["score_team2"] if ls else None,
    )


@app.post("/api/predict/match")
def predict_match_custom(req: PredictionRequest):
    return predict_match(req.team1_code, req.team2_code)


@app.get("/api/predict/tournament")
def predict_tournament():
    return predict_tournament_winner()


@app.get("/api/predict/group/{group}")
def predict_group_api(group: str):
    group_teams = [t for t in TEAMS if t["group"] == group.upper()]
    if not group_teams:
        return {"error": "Group not found"}, 404
    return {"group": group.upper(), "predictions": predict_group(group.upper(), group_teams)}


@app.get("/api/predict/strengths")
def get_strengths():
    result = {}
    for t in TEAMS:
        result[t["code"]] = {
            "name": t["name"],
            "flag": t["flag"],
            "strength": TEAM_STRENGTH.get(t["code"], 50),
            "group": t["group"],
        }
    return dict(sorted(result.items(), key=lambda x: -x[1]["strength"]))


# ── AI Chatbot Endpoint ─────────────────────────────────────

@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply = get_response(req.message)
    return ChatResponse(reply=reply)


# ── Live Score Simulation Engine ────────────────────────────

GOAL_EVENTS = [
    "🔥 GOAL! {} scores!",
    "⚡ What a strike from {}!",
    "🎯 {} finds the back of the net!",
    "💥 {} with a powerful shot! GOAL!",
    "✨ Beautiful team play! {} finishes!",
    "🎉 {} scores a spectacular goal!",
    "⚽ {} slots it home!",
    "🚀 {} with a rocket from distance!",
    "🎯 {} heads it in from a corner!",
    "👟 {} with a clinical finish!",
]

YELLOW_CARD_EVENTS = [
    "🟡 {} receives a yellow card.",
    "🟡 Booking for {}.",
    "🟡 {} goes into the referee's book.",
]

SAVE_EVENTS = [
    "🧤 Great save by the goalkeeper!",
    "🧤 Keeper denies the attacker!",
    "🧤 Fantastic reflexes from the goalkeeper!",
]


async def simulate_match(match_id: int):
    m = get_match_by_id(match_id)
    if not m:
        return

    s1 = TEAM_STRENGTH.get(m["team1_code"], 50)
    s2 = TEAM_STRENGTH.get(m["team2_code"], 50)

    live_scores[match_id] = {"score_team1": 0, "score_team2": 0, "status": "live"}
    live_events[match_id] = []
    minute = 0

    try:
        while minute < 90:
            await asyncio.sleep(random.uniform(2.0, 5.0))
            minute += random.randint(1, 3)
            if minute > 90:
                minute = 90

            event_chance = random.random()
            total_strength = s1 + s2

            if event_chance < 0.12 * (s1 / total_strength * 2):
                ls = live_scores[match_id]
                ls["score_team1"] += 1
                event = random.choice(GOAL_EVENTS).format(m["team1"])
                live_events[match_id].append({"minute": minute, "text": event, "type": "goal"})
                await broadcast_live_update(match_id)

            elif event_chance < 0.12 * (s1 / total_strength * 2) + 0.12 * (s2 / total_strength * 2):
                ls = live_scores[match_id]
                ls["score_team2"] += 1
                event = random.choice(GOAL_EVENTS).format(m["team2"])
                live_events[match_id].append({"minute": minute, "text": event, "type": "goal"})
                await broadcast_live_update(match_id)

            elif event_chance < 0.18:
                if random.random() < 0.5:
                    event = random.choice(YELLOW_CARD_EVENTS).format(m["team1"])
                else:
                    event = random.choice(YELLOW_CARD_EVENTS).format(m["team2"])
                live_events[match_id].append({"minute": minute, "text": event, "type": "card"})

            elif event_chance < 0.22:
                event = random.choice(SAVE_EVENTS)
                live_events[match_id].append({"minute": minute, "text": event, "type": "save"})

            await broadcast_live_update(match_id, full=False)

        live_scores[match_id]["status"] = "finished"
        await broadcast_live_update(match_id)
    except asyncio.CancelledError:
        pass
    finally:
        score_simulations.pop(match_id, None)


async def broadcast_live_update(match_id: int, full: bool = True):
    m = get_match_by_id(match_id)
    if not m:
        return
    ls = live_scores.get(match_id, {})
    payload = json.dumps({
        "type": "score_update",
        "match_id": match_id,
        "team1": m["team1"],
        "team2": m["team2"],
        "score_team1": ls.get("score_team1", 0),
        "score_team2": ls.get("score_team2", 0),
        "status": ls.get("status", "upcoming"),
        "events": live_events.get(match_id, [])[-5:] if full else [],
    })
    dead = []
    for ws in connected_clients:
        try:
            await ws.send_text(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        connected_clients.remove(ws)


@app.post("/api/live/start/{match_id}")
async def start_live_simulation(match_id: int):
    if match_id in score_simulations:
        return {"error": "Simulation already running"}, 400
    m = get_match_by_id(match_id)
    if not m:
        return {"error": "Match not found"}, 404
    task = asyncio.create_task(simulate_match(match_id))
    score_simulations[match_id] = task
    return {"status": "started", "match_id": match_id}


@app.post("/api/live/stop/{match_id}")
async def stop_live_simulation(match_id: int):
    task = score_simulations.get(match_id)
    if task:
        task.cancel()
        score_simulations.pop(match_id, None)
        return {"status": "stopped"}
    return {"status": "no_simulation"}


@app.get("/api/live/status/{match_id}")
def get_live_status(match_id: int):
    ls = live_scores.get(match_id)
    events = live_events.get(match_id, [])
    return {
        "match_id": match_id,
        "score_team1": ls["score_team1"] if ls else None,
        "score_team2": ls["score_team2"] if ls else None,
        "status": ls["status"] if ls else "upcoming",
        "events": events[-10:],
    }


@app.get("/api/live/active")
def get_active_live_matches():
    active = []
    for mid, ls in live_scores.items():
        if ls.get("status") == "live":
            m = get_match_by_id(mid)
            if m:
                active.append({
                    "match_id": mid,
                    "team1": m["team1"],
                    "team2": m["team2"],
                    "score_team1": ls["score_team1"],
                    "score_team2": ls["score_team2"],
                })
    return {"active": active}


# ── WebSocket for real-time updates ─────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connected_clients.append(ws)
    try:
        while True:
            data = await ws.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("type") == "start_simulation":
                    match_id = msg.get("match_id")
                    if match_id:
                        await start_live_simulation(match_id)
                        await ws.send_text(json.dumps({
                            "type": "simulation_started", "match_id": match_id
                        }))
                elif msg.get("type") == "ping":
                    await ws.send_text(json.dumps({"type": "pong"}))
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        pass
    finally:
        if ws in connected_clients:
            connected_clients.remove(ws)


# ── Serve built frontend ────────────────────────────────────

import os
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

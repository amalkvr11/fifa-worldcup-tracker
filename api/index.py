import os, sys, threading, time, random
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEAMS = [
    {"code":"MEX","name":"Mexico","group":"A","flag":"🇲🇽"},{"code":"CAN","name":"Canada","group":"A","flag":"🇨🇦"},
    {"code":"JAM","name":"Jamaica","group":"A","flag":"🇯🇲"},{"code":"USA","name":"United States","group":"A","flag":"🇺🇸"},
    {"code":"CRC","name":"Costa Rica","group":"B","flag":"🇨🇷"},{"code":"PAN","name":"Panama","group":"B","flag":"🇵🇦"},
    {"code":"BRA","name":"Brazil","group":"B","flag":"🇧🇷"},{"code":"ARG","name":"Argentina","group":"B","flag":"🇦🇷"},
    {"code":"COL","name":"Colombia","group":"C","flag":"🇨🇴"},{"code":"URU","name":"Uruguay","group":"C","flag":"🇺🇾"},
    {"code":"ECU","name":"Ecuador","group":"C","flag":"🇪🇨"},{"code":"CHI","name":"Chile","group":"C","flag":"🇨🇱"},
    {"code":"ENG","name":"England","group":"D","flag":"🏴󠁧󠁢󠁥󠁮󠁧󠁿"},{"code":"GER","name":"Germany","group":"D","flag":"🇩🇪"},
    {"code":"NED","name":"Netherlands","group":"D","flag":"🇳🇱"},{"code":"FRA","name":"France","group":"D","flag":"🇫🇷"},
    {"code":"ESP","name":"Spain","group":"E","flag":"🇪🇸"},{"code":"POR","name":"Portugal","group":"E","flag":"🇵🇹"},
    {"code":"ITA","name":"Italy","group":"E","flag":"🇮🇹"},{"code":"CRO","name":"Croatia","group":"E","flag":"🇭🇷"},
    {"code":"BEL","name":"Belgium","group":"F","flag":"🇧🇪"},{"code":"DEN","name":"Denmark","group":"F","flag":"🇩🇰"},
    {"code":"SRB","name":"Serbia","group":"F","flag":"🇷🇸"},{"code":"SUI","name":"Switzerland","group":"F","flag":"🇨🇭"},
    {"code":"JPN","name":"Japan","group":"G","flag":"🇯🇵"},{"code":"KOR","name":"South Korea","group":"G","flag":"🇰🇷"},
    {"code":"AUS","name":"Australia","group":"G","flag":"🇦🇺"},{"code":"KSA","name":"Saudi Arabia","group":"G","flag":"🇸🇦"},
    {"code":"IRN","name":"Iran","group":"H","flag":"🇮🇷"},{"code":"IRQ","name":"Iraq","group":"H","flag":"🇮🇶"},
    {"code":"MAR","name":"Morocco","group":"H","flag":"🇲🇦"},{"code":"EGY","name":"Egypt","group":"H","flag":"🇪🇬"},
    {"code":"TUN","name":"Tunisia","group":"I","flag":"🇹🇳"},{"code":"SEN","name":"Senegal","group":"I","flag":"🇸🇳"},
    {"code":"NGA","name":"Nigeria","group":"I","flag":"🇳🇬"},{"code":"GHA","name":"Ghana","group":"I","flag":"🇬🇭"},
    {"code":"CMR","name":"Cameroon","group":"J","flag":"🇨🇲"},{"code":"CIV","name":"Ivory Coast","group":"J","flag":"🇨🇮"},
    {"code":"ALG","name":"Algeria","group":"J","flag":"🇩🇿"},{"code":"NZL","name":"New Zealand","group":"J","flag":"🇳🇿"},
    {"code":"MLI","name":"Mali","group":"K","flag":"🇲🇱"},{"code":"BFA","name":"Burkina Faso","group":"K","flag":"🇧🇫"},
    {"code":"RSA","name":"South Africa","group":"K","flag":"🇿🇦"},{"code":"TAH","name":"Tahiti","group":"K","flag":"🇵🇫"},
    {"code":"IND","name":"India","group":"L","flag":"🇮🇳"},{"code":"CHN","name":"China","group":"L","flag":"🇨🇳"},
    {"code":"FIJ","name":"Fiji","group":"L","flag":"🇫🇯"},{"code":"UZB","name":"Uzbekistan","group":"L","flag":"🇺🇿"},
]

VENUES = [
    "MetLife Stadium New York","SoFi Stadium Los Angeles","AT&T Stadium Dallas",
    "NRG Stadium Houston","Arrowhead Stadium Kansas City","Levi's Stadium San Francisco",
    "Mercedes-Benz Stadium Atlanta","Lincoln Financial Field Philadelphia",
    "Gillette Stadium Boston","Allegiant Stadium Las Vegas",
    "Estadio Azteca Mexico City","Estadio BBVA Monterrey",
    "Estadio Akron Guadalajara","BC Place Vancouver","BMO Field Toronto",
]

STR = {"ARG":98,"BRA":97,"FRA":96,"ENG":95,"ESP":94,"GER":93,"NED":92,"POR":91,"BEL":90,"ITA":89,
       "CRO":87,"URU":86,"USA":84,"MEX":83,"JPN":82,"MAR":81,"SEN":80,"SUI":79,"COL":78,"DEN":77,
       "KOR":76,"AUS":75,"ECU":74,"NGA":73,"CMR":72,"GHA":71,"EGY":70,"TUN":69,"CIV":68,"ALG":67,
       "CRC":66,"PAN":65,"KSA":64,"IRN":63,"NZL":62,"CAN":61,"JAM":60,"MLI":59,"BFA":58,"RSA":57,
       "CHI":56,"SRB":55,"IRQ":54,"IND":53,"CHN":52,"UZB":51,"TAH":40,"FIJ":38}

SQUAD = {
    "ARG":[{"name":"Lionel Messi","number":10,"position":"Forward","rating":93},
           {"name":"Emiliano Martinez","number":23,"position":"Goalkeeper","rating":89}],
    "BRA":[{"name":"Vinícius Jr","number":7,"position":"Forward","rating":91},
           {"name":"Alisson","number":1,"position":"Goalkeeper","rating":89}],
    "FRA":[{"name":"Kylian Mbappé","number":10,"position":"Forward","rating":92}],
    "ESP":[{"name":"Pedri","number":16,"position":"Midfielder","rating":88}],
    "ENG":[{"name":"Harry Kane","number":9,"position":"Forward","rating":89}],
}

def build_matches():
    matches = []
    mid = 1
    base = datetime(2026, 6, 11, tzinfo=timezone.utc)
    KH = [12, 15, 18, 21]
    for g in "ABCDEFGHIJKL":
        ts = [t for t in TEAMS if t["group"] == g]
        pairs = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
        dates = [base + timedelta(days=(ord(g)-65)*3),
                 base + timedelta(days=(ord(g)-65)*3+3),
                 base + timedelta(days=(ord(g)-65)*3+7)]
        for idx,(a,b) in enumerate(pairs):
            t1,t2 = ts[a],ts[b]
            d = dates[min(idx//2,2)].replace(hour=KH[idx%4])
            matches.append({"id":mid,"team1":t1["name"],"team2":t2["name"],
                "team1_code":t1["code"],"team2_code":t2["code"],
                "team1_flag":t1["flag"],"team2_flag":t2["flag"],
                "group":g,"stage":"Group Stage","date_utc":d.isoformat(),
                "venue":VENUES[(mid-1)%len(VENUES)],"status":"upcoming",
                "score_team1":None,"score_team2":None,"favorite_count":0})
            mid += 1
    kb = datetime(2026,7,4,tzinfo=timezone.utc)
    for stage,n,off in [("Round of 16",8,0),("Quarter-finals",4,4),("Semi-finals",2,8),
                        ("Third Place",1,11),("Final",1,12)]:
        for i in range(n):
            dt = kb + timedelta(days=off+(i//2)) + timedelta(hours=(14 if i%2==0 else 19))
            matches.append({"id":mid,"team1":"TBD","team2":"TBD",
                "team1_code":"TBD","team2_code":"TBD",
                "team1_flag":"","team2_flag":"",
                "group":"KO","stage":stage,"date_utc":dt.isoformat(),
                "venue":VENUES[(mid-1)%len(VENUES)],"status":"upcoming",
                "score_team1":None,"score_team2":None,"favorite_count":0})
            mid += 1
    return matches

ALL_MATCHES = build_matches()

_scores = {}
_events = {}

@app.get("/api/health")
def health(): return {"status":"ok"}

@app.get("/api/matches")
def get_matches(): return {"matches":ALL_MATCHES,"total":len(ALL_MATCHES)}

@app.get("/api/matches/{mid}")
def get_match(mid: int):
    m = next((x for x in ALL_MATCHES if x["id"]==mid), None)
    if not m: return JSONResponse({"error":"Not found"}, status_code=404)
    ls = _scores.get(mid)
    if ls:
        m = dict(m)
        m["score_team1"] = ls.get("score_team1", m.get("score_team1"))
        m["score_team2"] = ls.get("score_team2", m.get("score_team2"))
        m["status"] = ls.get("status", m["status"])
    return m

@app.get("/api/teams")
def get_teams(): return [{"code":t["code"],"name":t["name"],"group":t["group"],"flag":t["flag"]} for t in TEAMS]

@app.get("/api/teams/{code}")
def get_team(code: str):
    t = next((t for t in TEAMS if t["code"]==code.upper()), None)
    if not t: return JSONResponse({"error":"Not found"}, status_code=404)
    return t

@app.get("/api/teams/{code}/players")
def get_players(code: str):
    return {"team_code": code.upper(), "players": SQUAD.get(code.upper(), [])}

@app.get("/api/groups")
def get_groups():
    g = {}
    for t in TEAMS:
        g.setdefault(t["group"], []).append({"code":t["code"],"name":t["name"],"flag":t["flag"]})
    return g

@app.get("/api/standings/{grp}")
def standings(grp: str):
    g = grp.upper()
    gt = [t for t in TEAMS if t["group"]==g]
    if not gt: return JSONResponse({"error":"Not found"}, status_code=404)
    res = []
    for t in gt:
        ms = [m for m in ALL_MATCHES if m["stage"]=="Group Stage" and m["group"]==g
              and (m["team1_code"]==t["code"] or m["team2_code"]==t["code"])]
        p=w=d=l=gf=ga=0
        for m in ms:
            s1=m.get("score_team1") or 0; s2=m.get("score_team2") or 0
            if m["team1_code"]==t["code"]: gf+=s1;ga+=s2
            else: gf+=s2;ga+=s1
            if s1>s2: w+=1
            elif s1==s2: d+=1
            else: l+=1
        res.append({"code":t["code"],"name":t["name"],"flag":t["flag"],
                     "played":p,"won":w,"drawn":d,"lost":l,
                     "gf":gf,"ga":ga,"gd":gf-ga,"points":w*3+d})
    res.sort(key=lambda x:(-x["points"],-x["gd"],-x["gf"]))
    return {"group":g,"standings":res}

@app.get("/api/predict/match/{mid}")
def pred_match(mid: int):
    m = next((x for x in ALL_MATCHES if x["id"]==mid), None)
    if not m: return JSONResponse({"error":"Not found"}, status_code=404)
    s1 = STR.get(m["team1_code"],50)+random.uniform(-3,3)
    s2 = STR.get(m["team2_code"],50)+random.uniform(-3,3)
    e1 = 1/(1+10**((s2-s1)/400))
    wp = round(e1*100,1); dp = round((1-abs(e1-0.5)*2)*100,1)
    return {"team1_code":m["team1_code"],"team2_code":m["team2_code"],
            "team1":m["team1"],"team2":m["team2"],
            "win_probability":wp,"draw_probability":dp,"lose_probability":round(100-wp-dp,1),
            "predicted_winner":m["team1_code"]if wp>50 else m["team2_code"]if wp<50 else"draw",
            "confidence":"high"if abs(wp-50)>20 else"medium"}

@app.get("/api/predict/tournament")
def pred_tourn():
    ranked = sorted(STR.items(), key=lambda x:-x[1])[:8]
    res = {}
    for c,_ in ranked:
        t = next((t for t in TEAMS if t["code"]==c), {})
        res[c] = {"name":t.get("name",""),"flag":t.get("flag",""),"probability":round(random.uniform(3,18),1)}
    tot = sum(v["probability"] for v in res.values())
    for v in res.values(): v["probability"] = round(v["probability"]/tot*100,1)
    ranked = dict(sorted(res.items(), key=lambda x:-x[1]["probability"]))
    fc = next(iter(ranked))
    return {"favorite_code":fc,"favorite_name":ranked[fc]["name"],"predictions":ranked}

@app.get("/api/predict/strengths")
def get_str():
    return {t["code"]:{"name":t["name"],"flag":t["flag"],"strength":STR.get(t["code"],50),"group":t["group"]}
            for t in sorted(TEAMS, key=lambda x:-STR.get(x["code"],50))}

@app.get("/api/predict/group/{grp}")
def pred_group(grp: str):
    g = grp.upper()
    gt = [t for t in TEAMS if t["group"]==g]
    if not gt: return JSONResponse({"error":"Not found"}, status_code=404)
    preds = [{"code":t["code"],"name":t["name"],"flag":t["flag"],
              "qualify":STR.get(t["code"],50)>65,"predicted_position":0,
              "strength":STR.get(t["code"],50)} for t in gt]
    preds.sort(key=lambda x:-x["strength"])
    for i,p in enumerate(preds): p["predicted_position"]=i+1
    return {"group":g,"predictions":preds}

@app.post("/api/chat")
def chat(body: dict):
    msg = (body.get("message") or "").lower()
    if "winner" in msg or "champion" in msg:
        return {"reply":"Argentina and Brazil are the top favorites for FIFA World Cup 2026!"}
    if "group" in msg:
        return {"reply":"48 teams in 12 groups of 4. Top 2 advance to Round of 16!"}
    if "match" in msg or "schedule" in msg:
        return {"reply":"Matches run June 11 - July 19 2026. 72 group + 16 knockout = 88 total!"}
    if "player" in msg or "squad" in msg:
        return {"reply":"Stars: Messi (ARG), Mbappé (FRA), Vinícius Jr (BRA), Bellingham (ENG), Pedri (ESP)!"}
    return {"reply":"Welcome to FIFA 2026 AI! Ask about teams, matches, players, predictions!"}

@app.post("/api/live/start/{mid}")
def start_live(mid: int):
    m = next((x for x in ALL_MATCHES if x["id"]==mid), None)
    if not m: return JSONResponse({"error":"Not found"}, status_code=404)
    _scores[mid] = {"score_team1":0,"score_team2":0,"status":"live"}; _events[mid]=[]
    s1 = STR.get(m["team1_code"],50); s2 = STR.get(m["team2_code"],50)
    G = ["Goal!","What a strike!","Finds the net!","Powerful shot!","Clinical finish!"]
    def sim():
        minute = 0
        while minute < 90:
            time.sleep(random.uniform(1.5,4.0)); minute += random.randint(1,3)
            if minute > 90: minute = 90
            total = s1+s2; ev = random.random()
            if ev < 0.10*(s1/total*2):
                _scores[mid]["score_team1"]+=1; _events[mid].append({"minute":minute,"text":random.choice(G),"type":"goal"})
            elif ev < 0.10*(s1/total*2)+0.10*(s2/total*2):
                _scores[mid]["score_team2"]+=1; _events[mid].append({"minute":minute,"text":random.choice(G),"type":"goal"})
            elif ev < 0.16: _events[mid].append({"minute":minute,"text":"Yellow card","type":"card"})
        _scores[mid]["status"]="finished"; _events[mid].append({"minute":90,"text":"Full time!","type":"info"})
    threading.Thread(target=sim, daemon=True).start()
    return {"status":"started","match_id":mid}

@app.get("/api/live/status/{mid}")
def live_status(mid: int):
    ls = _scores.get(mid,{})
    return {"match_id":mid,"score_team1":ls.get("score_team1"),"score_team2":ls.get("score_team2"),
            "status":ls.get("status","upcoming"),"events":_events.get(mid,[])[-10:]}

@app.get("/api/live/active")
def active_live():
    out = []
    for mid,ls in _scores.items():
        if ls.get("status")=="live":
            m = next((x for x in ALL_MATCHES if x["id"]==mid), None)
            if m:
                out.append({"match_id":mid,"team1":m["team1"],"team2":m["team2"],
                            "score_team1":ls["score_team1"],"score_team2":ls["score_team2"]})
    return {"active":out}

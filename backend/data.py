from datetime import datetime, timedelta, timezone

TEAMS = [
    {"code": "MEX", "name": "Mexico",       "group": "A", "flag": "🇲🇽"},
    {"code": "CAN", "name": "Canada",       "group": "A", "flag": "🇨🇦"},
    {"code": "JAM", "name": "Jamaica",      "group": "A", "flag": "🇯🇲"},
    {"code": "USA", "name": "United States","group": "A", "flag": "🇺🇸"},
    {"code": "CRC", "name": "Costa Rica",   "group": "B", "flag": "🇨🇷"},
    {"code": "PAN", "name": "Panama",       "group": "B", "flag": "🇵🇦"},
    {"code": "BRA", "name": "Brazil",       "group": "B", "flag": "🇧🇷"},
    {"code": "ARG", "name": "Argentina",    "group": "B", "flag": "🇦🇷"},
    {"code": "COL", "name": "Colombia",     "group": "C", "flag": "🇨🇴"},
    {"code": "URU", "name": "Uruguay",      "group": "C", "flag": "🇺🇾"},
    {"code": "ECU", "name": "Ecuador",      "group": "C", "flag": "🇪🇨"},
    {"code": "CHI", "name": "Chile",        "group": "C", "flag": "🇨🇱"},
    {"code": "ENG", "name": "England",      "group": "D", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
    {"code": "GER", "name": "Germany",      "group": "D", "flag": "🇩🇪"},
    {"code": "NED", "name": "Netherlands",  "group": "D", "flag": "🇳🇱"},
    {"code": "FRA", "name": "France",       "group": "D", "flag": "🇫🇷"},
    {"code": "ESP", "name": "Spain",        "group": "E", "flag": "🇪🇸"},
    {"code": "POR", "name": "Portugal",     "group": "E", "flag": "🇵🇹"},
    {"code": "ITA", "name": "Italy",        "group": "E", "flag": "🇮🇹"},
    {"code": "CRO", "name": "Croatia",      "group": "E", "flag": "🇭🇷"},
    {"code": "BEL", "name": "Belgium",      "group": "F", "flag": "🇧🇪"},
    {"code": "DEN", "name": "Denmark",      "group": "F", "flag": "🇩🇰"},
    {"code": "SRB", "name": "Serbia",       "group": "F", "flag": "🇷🇸"},
    {"code": "SUI", "name": "Switzerland",  "group": "F", "flag": "🇨🇭"},
    {"code": "JPN", "name": "Japan",        "group": "G", "flag": "🇯🇵"},
    {"code": "KOR", "name": "South Korea",  "group": "G", "flag": "🇰🇷"},
    {"code": "AUS", "name": "Australia",    "group": "G", "flag": "🇦🇺"},
    {"code": "KSA", "name": "Saudi Arabia", "group": "G", "flag": "🇸🇦"},
    {"code": "IRN", "name": "Iran",         "group": "H", "flag": "🇮🇷"},
    {"code": "IRQ", "name": "Iraq",         "group": "H", "flag": "🇮🇶"},
    {"code": "MAR", "name": "Morocco",      "group": "H", "flag": "🇲🇦"},
    {"code": "EGY", "name": "Egypt",        "group": "H", "flag": "🇪🇬"},
    {"code": "TUN", "name": "Tunisia",      "group": "I", "flag": "🇹🇳"},
    {"code": "SEN", "name": "Senegal",      "group": "I", "flag": "🇸🇳"},
    {"code": "NGA", "name": "Nigeria",      "group": "I", "flag": "🇳🇬"},
    {"code": "GHA", "name": "Ghana",        "group": "I", "flag": "🇬🇭"},
    {"code": "CMR", "name": "Cameroon",     "group": "J", "flag": "🇨🇲"},
    {"code": "CIV", "name": "Ivory Coast",  "group": "J", "flag": "🇨🇮"},
    {"code": "ALG", "name": "Algeria",      "group": "J", "flag": "🇩🇿"},
    {"code": "NZL", "name": "New Zealand",  "group": "J", "flag": "🇳🇿"},
    {"code": "MLI", "name": "Mali",         "group": "K", "flag": "🇲🇱"},
    {"code": "BFA", "name": "Burkina Faso", "group": "K", "flag": "🇧🇫"},
    {"code": "RSA", "name": "South Africa", "group": "K", "flag": "🇿🇦"},
    {"code": "UZB", "name": "Uzbekistan",   "group": "K", "flag": "🇺🇿"},
    {"code": "IND", "name": "India",        "group": "L", "flag": "🇮🇳"},
    {"code": "CHN", "name": "China",        "group": "L", "flag": "🇨🇳"},
    {"code": "FIJ", "name": "Fiji",         "group": "L", "flag": "🇫🇯"},
    {"code": "TAH", "name": "Tahiti",       "group": "L", "flag": "🇵🇫"},
]

VENUES = [
    "MetLife Stadium, New York",
    "SoFi Stadium, Los Angeles",
    "AT&T Stadium, Dallas",
    "NRG Stadium, Houston",
    "Arrowhead Stadium, Kansas City",
    "Levi's Stadium, San Francisco",
    "Mercedes-Benz Stadium, Atlanta",
    "Lincoln Financial Field, Philadelphia",
    "Gillette Stadium, Boston",
    "Allegiant Stadium, Las Vegas",
    "Estadio Azteca, Mexico City",
    "Estadio BBVA, Monterrey",
    "Estadio Akron, Guadalajara",
    "BC Place, Vancouver",
    "BMO Field, Toronto",
]


def get_team_code(name):
    for t in TEAMS:
        if t["name"] == name:
            return t["code"]
    return name


def get_group_teams(group):
    return [t for t in TEAMS if t["group"] == group]


def round_robin_pairs(teams):
    pairs = []
    n = len(teams)
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((i, j))
    return pairs


def round_robin_pairs(teams):
    pairs = []
    n = len(teams)
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((i, j))
    return pairs


def generate_group_matches():
    matches = []
    match_id = 1
    base_date = datetime(2026, 6, 11, tzinfo=timezone.utc)
    kickoff_hours = [12, 15, 18, 21]

    for group in "ABCDEFGHIJKL":
        teams_in_group = get_group_teams(group)
        if len(teams_in_group) != 4:
            continue

        pairs = round_robin_pairs(teams_in_group)

        group_dates = [
            base_date + timedelta(days=(ord(group) - ord("A")) * 3),
            base_date + timedelta(days=(ord(group) - ord("A")) * 3 + 3),
            base_date + timedelta(days=(ord(group) - ord("A")) * 3 + 7),
        ]

        for idx, (t1_idx, t2_idx) in enumerate(pairs):
            t1 = teams_in_group[t1_idx]
            t2 = teams_in_group[t2_idx]

            match_day = idx // 2
            kickoff = kickoff_hours[idx % 4]
            dt = group_dates[min(match_day, len(group_dates) - 1)].replace(
                hour=kickoff
            )
            venue = VENUES[(match_id - 1) % len(VENUES)]

            matches.append(
                {
                    "id": match_id,
                    "team1": t1["name"],
                    "team2": t2["name"],
                    "team1_code": t1["code"],
                    "team2_code": t2["code"],
                    "team1_flag": t1["flag"],
                    "team2_flag": t2["flag"],
                    "group": group,
                    "stage": "Group Stage",
                    "date_utc": dt.isoformat(),
                    "venue": venue,
                    "status": "upcoming",
                    "score_team1": None,
                    "score_team2": None,
                    "favorite_count": 0,
                }
            )
            match_id += 1

    return matches


def generate_knockout_matches(group_matches):
    matches = []
    match_id = len(group_matches) + 1
    base_date = datetime(2026, 7, 4, tzinfo=timezone.utc)

    knockout_names = [
        ("Round of 16", 8, 0),
        ("Quarter-finals", 4, 4),
        ("Semi-finals", 2, 8),
        ("Third Place", 1, 11),
        ("Final", 1, 12),
    ]

    for stage_name, num_matches, day_offset in knockout_names:
        for i in range(num_matches):
            session_hour = 14 if i % 2 == 0 else 19
            dt = base_date + timedelta(days=day_offset + (i // 2)) + timedelta(
                hours=session_hour
            )
            venue = VENUES[(match_id - 1) % len(VENUES)]

            stage_groups = ""
            if stage_name == "Round of 16":
                stage_groups = f"R16-{i+1}"

            matches.append(
                {
                    "id": match_id,
                    "team1": "TBD",
                    "team2": "TBD",
                    "team1_code": "TBD",
                    "team2_code": "TBD",
                    "team1_flag": "❓",
                    "team2_flag": "❓",
                    "group": stage_groups,
                    "stage": stage_name,
                    "date_utc": dt.isoformat(),
                    "venue": venue,
                    "status": "upcoming",
                    "score_team1": None,
                    "score_team2": None,
                    "favorite_count": 0,
                }
            )
            match_id += 1

    return matches


def get_all_matches():
    group_matches = generate_group_matches()
    knockout_matches = generate_knockout_matches(group_matches)
    return group_matches + knockout_matches


ALL_MATCHES = get_all_matches()
ALL_TEAMS = {t["code"]: t for t in TEAMS}

SQUAD_DATA = {
    "ARG": [
        {"name": "Lionel Messi", "number": 10, "position": "Forward", "rating": 93, "photo": "⚽"},
        {"name": "Emiliano Martínez", "number": 23, "position": "Goalkeeper", "rating": 89, "photo": "🧤"},
        {"name": "Julián Alvarez", "number": 9, "position": "Forward", "rating": 88, "photo": "⚽"},
        {"name": "Enzo Fernández", "number": 24, "position": "Midfielder", "rating": 87, "photo": "👟"},
    ],
    "BRA": [
        {"name": "Vinícius Jr", "number": 7, "position": "Forward", "rating": 91, "photo": "⚡"},
        {"name": "Alisson", "number": 1, "position": "Goalkeeper", "rating": 89, "photo": "🧤"},
        {"name": "Rodrygo", "number": 9, "position": "Forward", "rating": 87, "photo": "⚡"},
    ],
    "FRA": [
        {"name": "Kylian Mbappé", "number": 10, "position": "Forward", "rating": 92, "photo": "⚡"},
        {"name": "Antoine Griezmann", "number": 7, "position": "Midfielder", "rating": 87, "photo": "👟"},
        {"name": "Hugo Lloris", "number": 1, "position": "Goalkeeper", "rating": 87, "photo": "🧤"},
    ],
    "ESP": [
        {"name": "Pedri", "number": 16, "position": "Midfielder", "rating": 88, "photo": "👟"},
        {"name": "Unai Simón", "number": 1, "position": "Goalkeeper", "rating": 87, "photo": "🧤"},
    ],
    "ENG": [
        {"name": "Harry Kane", "number": 9, "position": "Forward", "rating": 89, "photo": "⚡"},
        {"name": "Jude Bellingham", "number": 22, "position": "Midfielder", "rating": 88, "photo": "👟"},
    ],
}

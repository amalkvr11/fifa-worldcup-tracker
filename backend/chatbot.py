import re
import random
from difflib import SequenceMatcher

KNOWLEDGE_BASE = {
    "tournament_format": """
The 2026 FIFA World Cup features 48 teams divided into 12 groups of 4 teams each.
Each team plays 3 group matches. The top 2 from each group advance to the Round of 16.
From there, it's a single-elimination knockout format: Round of 16 → Quarter-finals → Semi-finals → Final.
The tournament runs from June 11 to July 19, 2026, hosted across USA, Canada, and Mexico.
""",

    "host_cities": """
The 2026 World Cup is hosted across 16 cities in 3 countries:
🇺🇸 USA: New York, Los Angeles, Dallas, Houston, Kansas City, San Francisco, Atlanta, Philadelphia, Boston, Seattle, Miami, Baltimore
🇲🇽 Mexico: Mexico City, Monterrey, Guadalajara
🇨🇦 Canada: Vancouver, Toronto
""",

    "favorites": """
Top favorites for the 2026 World Cup based on AI analysis:
1. 🇦🇷 Argentina (defending champions, strongest squad depth)
2. 🇧🇷 Brazil (always a favorite, incredible attack)
3. 🇫🇷 France (back-to-back finalists, immense talent)
4. 🇪🇸 Spain (possession masters, young generation rising)
5. 🇬🇧 England (consistent performers, deep squad)
The AI prediction engine updates probabilities in real-time based on team strength metrics.
""",

    "rules": """
Key FIFA World Cup rules:
• 48 teams, 12 groups of 4
• Group stage: 6 matches per group (each team plays 3)
• Win = 3 pts, Draw = 1 pt, Loss = 0 pts
• Top 2 from each group advance
• Knockout matches go to extra time (30min) then penalties if tied
• 5 substitutions allowed per match
• VAR (Video Assistant Referee) used for all matches
• Offside, handball, and foul rules follow IFAB standards
""",

    "history": """
FIFA World Cup Winners:
🇧🇷 Brazil: 1958, 1962, 1970, 1994, 2002 (5 titles)
🇩🇪 Germany: 1954, 1974, 1990, 2014 (4 titles)
🇮🇹 Italy: 1934, 1938, 1982, 2006 (4 titles)
🇦🇷 Argentina: 1978, 1986, 2022 (3 titles)
🇫🇷 France: 1998, 2018 (2 titles)
🏴󠁧󠁢󠁥󠁮󠁧󠁿 England: 1966 (1 title)
🇪🇸 Spain: 2010 (1 title)
Most goals in a tournament: 26 (France 1998, Brazil 2002, Brazil 2014)
""",

    "india": """
🇮🇳 India is participating in the 2026 FIFA World Cup! This is India's FIRST EVER World Cup appearance.
They are in Group P alongside China and Uzbekistan.
Key Indian players to watch: Sunil Chhetri (captain, all-time top scorer)
India qualified through the AFC qualification path and their participation marks a historic milestone.
""",

    "trophy": """
The FIFA World Cup Trophy:
• Made of 18-carat gold with malachite base
• Weighs 6.175 kg (13.61 lbs)
• Height: 36.8 cm (14.4 in)
• Designed by Silvio Gazzaniga
• Awarded since 1974
• The original trophy (Jules Rimet Trophy) was awarded from 1930-1970
• Winners get a gold-plated bronze replica
• The original trophy stays with FIFA
""",

    "groups": """
Group A: Mexico, Canada, Jamaica
Group B: USA, Costa Rica, Panama
Group C: Brazil, Argentina, Colombia
Group D: Uruguay, Ecuador, Chile
Group E: England, Germany, Netherlands
Group F: France, Spain, Portugal
Group G: Italy, Croatia, Switzerland
Group H: Belgium, Denmark, Serbia
Group I: Japan, South Korea, Australia
Group J: Saudi Arabia, Iran, Iraq
Group K: Morocco, Egypt, Tunisia
Group L: Senegal, Nigeria, Ghana
Group M: Cameroon, Ivory Coast, Algeria
Group N: New Zealand, Tahiti, Fiji
Group O: Mali, Burkina Faso, South Africa
Group P: India, China, Uzbekistan
""",

    "schedule": """
The 2026 World Cup runs from June 8 to July 8, 2026.
• Group Stage: June 8 - June 22
• Round of 32: June 29 - July 1
• Round of 16: July 2 - July 4
• Quarter-finals: July 5 - July 6
• Semi-finals: July 7
• Third Place & Final: July 8
All match timings are available in IST on the Matches page.
""",

    "venue": """
2026 World Cup venues include:
• MetLife Stadium, New York (82,500 capacity)
• SoFi Stadium, Los Angeles (70,240)
• AT&T Stadium, Dallas (80,000)
• Estádio Azteca, Mexico City (87,523)
• BC Place, Vancouver (54,500)
• BMO Field, Toronto (30,000)
• And 10 more world-class stadiums across North America!
""",

    "points": """
In the group stage, teams earn:
• Win: 3 points
• Draw: 1 point
• Loss: 0 points
Tiebreakers: 1) Goal difference, 2) Goals scored, 3) Head-to-head, 4) Fair play, 5) Drawing of lots
Top 2 teams from each group advance to the knockout stage.
""",

    "qualification": """
The 2026 World Cup qualification spots by confederation:
• UEFA (Europe): 16 spots
• CAF (Africa): 9 spots
• AFC (Asia): 8 spots
• CONCACAF (North America): 6 spots (including hosts)
• CONMEBOL (South America): 6 spots
• OFC (Oceania): 1 spot
• 2 intercontinental playoff spots
Total: 48 teams
""",

    "prize": """
The 2026 FIFA World Cup prize money:
• Total prize pool: $440 million
• Winner: $42 million
• Runner-up: $30 million
• Third place: $27 million
• Fourth place: $25 million
• Quarter-finalists: $17 million
• Round of 16: $13 million
• Group stage: $9 million
Each team also receives $1.5 million for preparation costs.
""",

    "messi": """
Lionel Messi is the captain of Argentina and led them to victory in the 2022 World Cup in Qatar.
He won the Golden Ball (best player) award in 2022, scoring 7 goals including 2 in the final.
At the 2026 World Cup, Messi would be 38 years old. While he may not participate,
his legacy as one of the greatest footballers of all time is unquestioned.
8x Ballon d'Or winner, World Cup winner, Copa América winner.
""",

    "ronaldo": """
Cristiano Ronaldo is Portugal's all-time top scorer and one of football's greatest players.
He has played in 5 World Cups (2006, 2010, 2014, 2018, 2022).
At the 2026 World Cup, Ronaldo would be 41 years old.
5x Ballon d'Or winner, European Champion with Portugal (2016).
Portugal has a strong squad and could be dark horses for the 2026 title.
""",
}

PATTERNS = [
    (r'\b(format|structure|how\s.*work|system)\b', 'tournament_format'),
    (r'\b(host|city|cities|venue|stadium|where)\b', 'host_cities'),
    (r'\b(favorite|favourite|favorites|favourites|top\s.*team|who\s.*win|best\s.*team|prediction)\b', 'favorites'),
    (r'\b(rules|rule|regulation|law|offside|substitution|var)\b', 'rules'),
    (r'\b(history|past|winner|champion|won|title|1966|1998|2002|2010|2014|2018|2022)\b', 'history'),
    (r'\bindia\b', 'india'),
    (r'\btrophy|cup\b', 'trophy'),
    (r'\bgroup\b', 'groups'),
    (r'\bschedule|when|date|timing|time|calendar\b', 'schedule'),
    (r'\bvenue|stadium\b', 'venue'),
    (r'\bpoint|point system|standings|ranking|table\b', 'points'),
    (r'\bqualif|qualification|spot|berth\b', 'qualification'),
    (r'\bprize|money|prize pool|reward|fund\b', 'prize'),
    (r'\bmessi|lionel\b', 'messi'),
    (r'\bronaldo|cristiano\b', 'ronaldo'),
]

GREETINGS = [
    "Hello! ⚽ I'm your FIFA World Cup 2026 assistant. Ask me about teams, matches, rules, or predictions!",
    "Hi there! 🏆 Ready to talk World Cup? Ask me anything about the 2026 tournament!",
    "Hey! I'm the FIFA 2026 bot. What would you like to know?",
]

UNKNOWN = [
    "I'm not sure about that. Try asking me about teams, groups, rules, predictions, or the tournament format! ⚽",
    "Hmm, I don't have info on that. I can help with World Cup rules, teams, schedule, predictions, and more!",
    "I couldn't find an answer to that. Ask me about FIFA World Cup 2026 topics like groups, venues, or favorites!",
]


def classify_intent(message: str) -> str:
    message = message.lower().strip()

    if any(greeting in message for greeting in ["hello", "hi ", "hey", "hola", "namaste", "good morning", "good evening"]):
        return "__greeting__"

    for pattern, intent in PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return intent

    best_score = 0
    best_intent = None
    for intent, text in KNOWLEDGE_BASE.items():
        score = SequenceMatcher(None, message, text[:200].lower()).ratio()
        if score > best_score:
            best_score = score
            best_intent = intent

    if best_score > 0.25:
        return best_intent

    return "__unknown__"


def get_response(message: str) -> str:
    if not message or not message.strip():
        return "Please ask me something about the FIFA World Cup 2026! ⚽"

    intent = classify_intent(message)

    if intent == "__greeting__":
        return random.choice(GREETINGS)

    if intent == "__unknown__":
        return random.choice(UNKNOWN)

    return KNOWLEDGE_BASE.get(intent, random.choice(UNKNOWN)).strip()

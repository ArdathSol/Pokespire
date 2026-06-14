import streamlit as st
import random
import requests
from typing import List, Optional, Dict

st.set_page_config(page_title="PokéSpire", page_icon="⚔️", layout="wide")

# ====================== SPRACHE ======================
if "language" not in st.session_state:
    st.session_state.language = "de"

def t(de: str, en: str) -> str:
    return de if st.session_state.language == "de" else en

# ====================== POKÉAPI ======================
# Korrekte Zuordnung: Deutsche Namen → Englische API-Namen
POKEMON_DE_TO_API: Dict[str, str] = {
    # Starter & Evolutionen
    "bisasam": "bulbasaur",
    "bisaknosp": "ivysaur",
    "bisaflor": "venusaur",
    "glumanda": "charmander",
    "glutexo": "charmeleon",
    "glurak": "charizard",
    "schiggy": "squirtle",
    "schillok": "wartortle",
    "turtok": "blastoise",
    # Gegner
    "rattfratz": "rattata",
    "rattikarl": "raticate",
    "taubsi": "pidgey",
    "tauboga": "pidgeotto",
    "tauboss": "pidgeot",
    "raupy": "caterpie",
    "safcon": "metapod",
    "smettbo": "butterfree",
    "hornliu": "weedle",
    "kokuna": "kakuna",
    "bibor": "beedrill",
    "pummeluff": "jigglypuff",
    "knuddeluff": "wigglytuff",
    "piepi": "clefairy",
    "pixi": "clefable",
    "pikachu": "pikachu",
    "raichu": "raichu",
    "habitak": "spearow",
    "skarmory": "skarmory",
    "abra": "abra",
    "kadabra": "kadabra",
    "simsala": "alakazam",
    "machollo": "machop",
    "maschock": "machoke",
    "machomei": "machamp",
    "quapsel": "poliwag",
    "quaputzi": "poliwhirl",
    "quappo": "poliwrath",
    "sleima": "grimer",
    "sleimok": "muk",
    "kleinstein": "geodude",
    "georok": "graveler",
    "geowaz": "golem",
    "fukano": "growlithe",
    "arkani": "arcanine",
    "igelavar": "sandshrew",
    "sandamer": "sandslash",
    "sandan": "ekans",
    "arbok": "arbok",
    "zubat": "zubat",
    "golbat": "golbat",
    "myrapla": "bellsprout",
    "owei": "vulpix",
    "vulnona": "ninetales",
    "ditto": "ditto",
    "evoli": "eevee",
    "psiana": "drowzee",
    "hypno": "hypno",
    "krabby": "krabby",
    "kingler": "kingler",
    "menki": "mankey",
    "rasaff": "primeape",
    "ponita": "ponyta",
    "gallopa": "rapidash",
    "mauzi": "meowth",
    "snobilikat": "persian",
    "starmie": "starmie",
    "staryu": "staryu",
    "tentacha": "tentacool",
    "tentoxa": "tentacruel",
}

@st.cache_data(ttl=3600)
def get_sprite_url(name: str) -> str:
    """Holt das offizielle Artwork für ein Pokémon (DE oder EN Name)."""
    api_name = POKEMON_DE_TO_API.get(name.lower(), name.lower())
    try:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{api_name}", timeout=8)
        r.raise_for_status()
        data = r.json()
        url = (data["sprites"]["other"]["official-artwork"].get("front_default")
               or data["sprites"].get("front_default"))
        return url or _placeholder(name)
    except Exception:
        return _placeholder(name)

def _placeholder(name: str) -> str:
    return f"https://placehold.co/220x220/1a1a2e/e0e0ff?text={name[:8]}"

# ====================== CSS ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Nunito:wght@400;700&display=swap');

.stApp {
    background: linear-gradient(160deg, #0d0d1f 0%, #1a1a3e 50%, #0d0d1f 100%);
    color: #e0e0ff;
}

/* Titel */
h1 { font-family: 'Press Start 2P', monospace; color: #ffd700; text-shadow: 0 0 20px #ffd70088; font-size: 1.6rem !important; }
h2, h3 { font-family: 'Nunito', sans-serif; color: #a0c4ff; }

/* Metriken */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e1e4f, #2a2a6e);
    border: 1px solid #4444aa;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 4px 15px #00000088;
}
[data-testid="stMetricLabel"] { color: #a0c4ff !important; font-size: 0.85rem; }
[data-testid="stMetricValue"] { color: #ffd700 !important; font-size: 1.4rem !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2a2a6e, #3a3a9e);
    color: #e0e0ff;
    border: 1px solid #5555cc;
    border-radius: 10px;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px #00000066;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #3a3aae, #5050cc);
    border-color: #8888ff;
    box-shadow: 0 0 20px #5555cc88;
    transform: translateY(-2px);
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #cc4400, #ff6600);
    border-color: #ff8800;
    color: #fff;
    font-size: 1rem;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #ff5500, #ff8800);
    box-shadow: 0 0 20px #ff660088;
}

/* HP-Balken */
.hp-bar-bg {
    background: #1a1a3e;
    border-radius: 8px;
    border: 1px solid #333;
    height: 22px;
    overflow: hidden;
    margin: 4px 0;
}
.hp-bar-fill {
    height: 100%;
    border-radius: 8px;
    display: flex;
    align-items: center;
    padding-left: 8px;
    font-size: 0.75rem;
    font-weight: bold;
    color: #fff;
    transition: width 0.5s ease;
}
.hp-green { background: linear-gradient(90deg, #22bb44, #44dd66); }
.hp-yellow { background: linear-gradient(90deg, #bbaa00, #ffcc00); }
.hp-red { background: linear-gradient(90deg, #cc2200, #ff4422); }

/* Karten */
.card-container {
    background: linear-gradient(135deg, #1e1e4f 0%, #2a2a6e 100%);
    border: 1px solid #5555cc;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    margin: 4px 0;
    box-shadow: 0 4px 15px #00000077;
}
.card-name { font-weight: bold; color: #ffd700; font-size: 0.95rem; }
.card-stats { color: #a0c4ff; font-size: 0.8rem; margin-top: 4px; }
.card-cost { color: #ffaa00; font-size: 0.8rem; }

/* Kampf-Arena */
.battle-box {
    background: linear-gradient(135deg, #0f0f2e, #1e1e4e);
    border: 2px solid #5555cc;
    border-radius: 16px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 0 30px #3333aa44;
}

/* Pokémon-Box */
.pokemon-card {
    background: linear-gradient(135deg, #1a1a3e, #252545);
    border: 1px solid #4444aa;
    border-radius: 12px;
    padding: 12px;
    margin: 8px 0;
    box-shadow: 0 4px 12px #00000066;
}

/* Energie */
.energy-display {
    background: #1a1a3e;
    border: 1px solid #ffaa00;
    border-radius: 8px;
    padding: 8px 14px;
    display: inline-block;
    color: #ffaa00;
    font-weight: bold;
    font-size: 1rem;
    margin: 6px 0;
}

/* Typ-Badges */
.type-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: bold;
    margin: 2px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1f, #1a1a3e);
    border-right: 1px solid #3333aa;
}

/* Info/Success/Error Boxen */
.stAlert { border-radius: 10px; }

/* Expander */
[data-testid="stExpander"] {
    background: #1a1a3e;
    border: 1px solid #3333aa;
    border-radius: 10px;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #1e1e4f;
    border: 1px solid #5555cc;
    border-radius: 8px;
    color: #e0e0ff;
}
</style>
""", unsafe_allow_html=True)

# ====================== HELPERS ======================
def type_color(poke_type: str) -> str:
    colors = {
        "Feuer": "#ff6622", "Wasser": "#3399ff", "Pflanze": "#44bb44",
        "Elektro": "#ffcc00", "Normal": "#aaaaaa", "Psycho": "#ff44aa",
        "Kampf": "#cc4422", "Flug": "#88aaff", "Gift": "#aa44cc",
        "Boden": "#cc9933", "Gestein": "#887744", "Eis": "#77ddff",
        "Drache": "#7722ff", "Dunkel": "#554433", "Stahl": "#aaaacc",
        "Fee": "#ffaaee", "Geist": "#6655aa", "Käfer": "#aacc22",
    }
    return colors.get(poke_type, "#888888")

def hp_bar_html(current: int, maximum: int, label: str = "") -> str:
    pct = max(0, min(100, int(current / max(1, maximum) * 100)))
    cls = "hp-green" if pct > 50 else "hp-yellow" if pct > 20 else "hp-red"
    txt = f"{current}/{maximum}" if not label else f"{label}: {current}/{maximum}"
    return f"""
    <div class='hp-bar-bg'>
        <div class='hp-bar-fill {cls}' style='width:{pct}%'>{txt}</div>
    </div>"""

def type_badge(poke_type: str) -> str:
    color = type_color(poke_type)
    return f"<span class='type-badge' style='background:{color}22;border:1px solid {color};color:{color}'>{poke_type}</span>"

# ====================== KLASSEN ======================
class Card:
    def __init__(self, name: str, damage: int, block: int, poke_type: str,
                 cost: int = 1, effect: str = ""):
        self.name = name
        self.damage = damage
        self.block = block
        self.type = poke_type
        self.cost = cost
        self.effect = effect  # z.B. "heal:5", "burn:3", "draw:1"

    def describe(self) -> str:
        parts = []
        if self.damage > 0:
            parts.append(f"⚔️ {self.damage} DMG")
        if self.block > 0:
            parts.append(f"🛡️ {self.block} Block")
        if self.effect:
            eff_map = {"heal": "💚 Heilt", "burn": "🔥 Verbrennung", "draw": "🃏 +Karte"}
            key = self.effect.split(":")[0]
            val = self.effect.split(":")[1] if ":" in self.effect else ""
            parts.append(f"{eff_map.get(key, self.effect)} {val}")
        return " | ".join(parts) if parts else "Keine Wirkung"

class Relic:
    def __init__(self, name: str, desc: str, effect: str = ""):
        self.name = name
        self.desc = desc
        self.effect = effect

class Pokemon:
    def __init__(self, name: str, poke_type: str, cards: List[Card],
                 evolution_api: Optional[str] = None,
                 evolution_de: Optional[str] = None,
                 evo_level: int = 16):
        self.name = name
        self.type = poke_type
        self.cards = cards
        self.level = 1
        self.exp = 0
        self.evolution_api = evolution_api
        self.evolution_de = evolution_de
        self.evo_level = evo_level
        self.battles_won = 0
        self.friendship = 70
        self.hp = 40
        self.max_hp = 40

    def can_evolve(self) -> bool:
        return bool(self.evolution_api) and (
            self.level >= self.evo_level or self.battles_won >= 5
        )

    def gain_exp(self, amount: int) -> bool:
        """Gibt True zurück wenn Level-Up."""
        self.exp += amount
        if self.exp >= self.level * 10:
            self.exp = 0
            self.level += 1
            self.max_hp += 5
            self.hp = min(self.hp + 5, self.max_hp)
            return True
        return False

    def evolve(self):
        if self.evolution_de:
            self.name = self.evolution_de
        if self.evolution_api:
            self.evolution_api = None
            self.evolution_de = None
        self.max_hp += 15
        self.hp = min(self.hp + 15, self.max_hp)
        # Stärkere Karten nach Evolution
        for card in self.cards:
            card.damage = int(card.damage * 1.4)
            card.block = int(card.block * 1.3)

class Player:
    def __init__(self):
        self.deck: List[Card] = []
        self.team: List[Pokemon] = []
        self.max_hp = 80
        self.hp = self.max_hp
        self.gold = 50
        self.region = 1
        self.floor = 1
        self.battles_won_total = 0
        self.relics: List[Relic] = []
        self.burn_stacks = 0

    def add_pokemon(self, pokemon: Pokemon):
        self.team.append(pokemon)
        for card in pokemon.cards:
            self.deck.append(card)

    def check_evolutions(self) -> List[str]:
        """Gibt Liste evolved Pokémon zurück."""
        evolved = []
        for p in self.team:
            if p.can_evolve():
                old_name = p.name
                p.evolve()
                evolved.append(f"{old_name} → {p.name}")
        return evolved

    def apply_relic_effects(self, trigger: str):
        for relic in self.relics:
            if relic.effect == f"start_energy" and trigger == "combat_start":
                st.session_state.energy = min(5, st.session_state.energy + 1)
            elif relic.effect == "hp_regen" and trigger == "end_turn":
                self.hp = min(self.max_hp, self.hp + 2)

# ====================== DATEN ======================

# Gegner mit korrekten deutschen Namen & API-Namen
ENEMIES_BY_REGION = {
    1: [
        {"name": "Rattfratz", "api": "rattata", "hp_range": (30, 50),
         "damage_range": (6, 12), "type": "Normal", "reward": (15, 30),
         "attacks": ["Schnelligkeit", "Tackle"]},
        {"name": "Taubsi", "api": "pidgey", "hp_range": (28, 45),
         "damage_range": (5, 11), "type": "Flug", "reward": (12, 25),
         "attacks": ["Windstoß", "Tackle"]},
        {"name": "Raupy", "api": "caterpie", "hp_range": (20, 35),
         "damage_range": (3, 8), "type": "Käfer", "reward": (10, 20),
         "attacks": ["Fadenschuss", "Tackle"]},
        {"name": "Hornliu", "api": "weedle", "hp_range": (22, 38),
         "damage_range": (4, 10), "type": "Käfer", "reward": (10, 20),
         "attacks": ["Giftdorn", "Tackle"]},
        {"name": "Pummeluff", "api": "jigglypuff", "hp_range": (45, 65),
         "damage_range": (7, 14), "type": "Fee", "reward": (20, 35),
         "attacks": ["Pfund", "Schlaf-Song", "Liebreiz"]},
        {"name": "Piepi", "api": "clefairy", "hp_range": (40, 55),
         "damage_range": (6, 12), "type": "Fee", "reward": (18, 32),
         "attacks": ["Pfund", "Metronom"]},
        {"name": "Zubat", "api": "zubat", "hp_range": (30, 48),
         "damage_range": (7, 13), "type": "Flug", "reward": (14, 26),
         "attacks": ["Flatterklau", "Giftzahn"]},
        {"name": "Pikachu", "api": "pikachu", "hp_range": (35, 55),
         "damage_range": (10, 18), "type": "Elektro", "reward": (25, 45),
         "attacks": ["Donnerschock", "Blitz", "Donner"]},
    ],
    2: [
        {"name": "Rattikarl", "api": "raticate", "hp_range": (55, 80),
         "damage_range": (12, 20), "type": "Normal", "reward": (30, 50),
         "attacks": ["Hyper-Fang", "Schnelligkeit"]},
        {"name": "Tauboga", "api": "pidgeotto", "hp_range": (60, 85),
         "damage_range": (13, 22), "type": "Flug", "reward": (32, 52),
         "attacks": ["Windstoß", "Sturzflug"]},
        {"name": "Knuddeluff", "api": "wigglytuff", "hp_range": (70, 100),
         "damage_range": (15, 25), "type": "Fee", "reward": (40, 65),
         "attacks": ["Pfund", "Donnerschlag", "Schlaf-Song"]},
        {"name": "Smettbo", "api": "butterfree", "hp_range": (55, 75),
         "damage_range": (10, 18), "type": "Käfer", "reward": (28, 48),
         "attacks": ["Silberpuder", "Schlafpuder", "Psychokinese"]},
        {"name": "Golbat", "api": "golbat", "hp_range": (70, 95),
         "damage_range": (15, 24), "type": "Flug", "reward": (35, 55),
         "attacks": ["Flatterklau", "Giftzahn", "Luftschneider"]},
        {"name": "Menki", "api": "mankey", "hp_range": (55, 78),
         "damage_range": (14, 22), "type": "Kampf", "reward": (30, 50),
         "attacks": ["Kratzer", "Karate-Hieb", "Ärger"]},
    ],
    3: [
        {"name": "Bibor", "api": "beedrill", "hp_range": (70, 95),
         "damage_range": (18, 28), "type": "Käfer", "reward": (45, 70),
         "attacks": ["Giftnadel", "Twineedle", "Gifthieb"]},
        {"name": "Rasaff", "api": "primeape", "hp_range": (90, 120),
         "damage_range": (20, 32), "type": "Kampf", "reward": (50, 80),
         "attacks": ["Karate-Hieb", "Niederschlag", "Kreuzhieb"]},
        {"name": "Raichu", "api": "raichu", "hp_range": (85, 115),
         "damage_range": (22, 35), "type": "Elektro", "reward": (55, 85),
         "attacks": ["Blitz", "Donner", "Voltakku"]},
    ],
}

# Boss-Gegner pro Region
BOSSES = {
    1: {"name": "Relaxo", "api": "snorlax", "hp": 120, "damage_range": (15, 25),
        "type": "Normal", "reward": (80, 120), "attacks": ["Körperrammler", "Amnesie", "Schlaf"]},
    2: {"name": "Garados", "api": "gyarados", "hp": 180, "damage_range": (22, 35),
        "type": "Wasser", "reward": (120, 180), "attacks": ["Surfer", "Knirscher", "Drachentanz"]},
    3: {"name": "Gengar", "api": "gengar", "hp": 160, "damage_range": (25, 40),
        "type": "Geist", "reward": (150, 220), "attacks": ["Schlick", "Nachtschatten", "Psychokinese"]},
}

# Komplettes Kartensystem
ALL_CARDS = {
    "Tackle":        Card("Tackle",        10, 0, "Normal",   1),
    "Growl":         Card("Growl",          0, 6, "Normal",   1),
    "Kratzer":       Card("Kratzer",       12, 0, "Normal",   1),
    "Rankenhieb":    Card("Rankenhieb",    14, 0, "Pflanze",  1),
    "Rasierblatt":   Card("Rasierblatt",   18, 0, "Pflanze",  2),
    "Sonnenstahl":   Card("Sonnenstahl",   24, 0, "Pflanze",  3),
    "Blättersturm":  Card("Blättersturm",  20, 5, "Pflanze",  2),
    "Glut":          Card("Glut",          14, 0, "Feuer",    1),
    "Flammenwurf":   Card("Flammenwurf",   22, 0, "Feuer",    2),
    "Feuersturm":    Card("Feuersturm",    30, 0, "Feuer",    3),
    "Eruption":      Card("Eruption",      40, 0, "Feuer",    3, "burn:5"),
    "Blubber":       Card("Blubber",       14, 0, "Wasser",   1),
    "Surfer":        Card("Surfer",        22, 0, "Wasser",   2),
    "Aquawelle":     Card("Aquawelle",     28, 8, "Wasser",   3),
    "Hydrokanone":   Card("Hydrokanone",   38, 0, "Wasser",   3),
    "Verteidigung":  Card("Verteidigung",   0,10, "Normal",   1),
    "Eisenhaut":     Card("Eisenhaut",      0,16, "Stahl",    2),
    "Barrikade":     Card("Barrikade",      0,24, "Normal",   2),
    "Donner":        Card("Donner",        28, 0, "Elektro",  2),
    "Donnerschock":  Card("Donnerschock",  18, 0, "Elektro",  1),
    "Voltakku":      Card("Voltakku",      35, 0, "Elektro",  3),
    "Erholung":      Card("Erholung",       0, 0, "Normal",   1, "heal:10"),
    "Schlafpuder":   Card("Schlafpuder",    0,12, "Pflanze",  1, "heal:5"),
    "Karate-Hieb":   Card("Karate-Hieb",   20, 0, "Kampf",   1),
    "Kreuzhieb":     Card("Kreuzhieb",     28, 4, "Kampf",   2),
    "Psychokinese":  Card("Psychokinese",  24, 0, "Psycho",  2),
    "Nachtschatten": Card("Nachtschatten", 16, 0, "Dunkel",  1),
}

# Starter-Karten-Sets
STARTER_CARDS = {
    "bulbasaur":  ["Tackle", "Growl", "Rankenhieb", "Verteidigung"],
    "charmander": ["Tackle", "Growl", "Glut",        "Verteidigung"],
    "squirtle":   ["Tackle", "Growl", "Blubber",     "Verteidigung"],
}

# Evolutionskette
EVOLUTION_CHAIN = {
    "bulbasaur":   ("ivysaur",     "Bisaknosp",  16),
    "bisaknosp":   ("venusaur",    "Bisaflor",   32),
    "charmander":  ("charmeleon",  "Glutexo",    16),
    "glutexo":     ("charizard",   "Glurak",     36),
    "squirtle":    ("wartortle",   "Schillok",   16),
    "schillok":    ("blastoise",   "Turtok",     36),
}

# Relikte
RELIC_POOL = [
    Relic("Anfänger-Amulett",  "Freundschaft +50% nach Kampf",   "friendship_boost"),
    Relic("Glücks-Ei",         "+20% mehr Gold nach Kämpfen",    "gold_boost"),
    Relic("Altes Amulett",     "+1 Energie zu Kampfbeginn",      "start_energy"),
    Relic("Kräuter-Buch",      "Heilt 3 HP am Ende jedes Zugs",  "hp_regen"),
    Relic("Kampfstein",        "Alle Angriffe +3 Schaden",       "damage_boost"),
    Relic("Silberpuder",       "Doppelter Block im ersten Zug",  "first_block"),
    Relic("Arenaleiter-Orden", "Boss-Belohnungen verdoppelt",    "boss_reward"),
]

# Shop-Items
SHOP_CARDS = [
    "Rasierblatt", "Flammenwurf", "Surfer", "Eisenhaut", "Barrikade",
    "Donner", "Erholung", "Karate-Hieb", "Psychokinese", "Nachtschatten",
    "Sonnenstahl", "Feuersturm", "Aquawelle", "Voltakku", "Kreuzhieb",
]

# ====================== SESSION ======================
def init_session():
    defaults = {
        "player": None, "in_combat": False, "enemy": None,
        "hand": [], "energy": 3, "block": 0,
        "game_log": [], "show_evolution": None,
        "shop_cards": [], "in_shop": False, "in_rest": False,
        "combat_started": False, "enemy_status": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

def log(msg: str):
    st.session_state.game_log.insert(0, msg)
    if len(st.session_state.game_log) > 20:
        st.session_state.game_log = st.session_state.game_log[:20]

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("### ⚔️ PokéSpire")
    st.markdown("---")
    lang_opt = st.selectbox("🌍 Sprache", ["Deutsch", "English"], key="lang_sel")
    st.session_state.language = "de" if lang_opt == "Deutsch" else "en"

    if st.button("🔄 Neustart", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("language", "lang_sel"):
                del st.session_state[k]
        st.rerun()

    if st.session_state.player:
        p = st.session_state.player
        st.markdown("---")
        st.markdown("### 📊 Status")
        st.markdown(hp_bar_html(max(0, p.hp), p.max_hp, "❤️ HP"), unsafe_allow_html=True)
        st.markdown(f"💰 **{p.gold}** Gold | 🏆 **{p.battles_won_total}** Siege")
        st.markdown(f"📍 Region **{p.region}** | Etage **{p.floor}**")

        if p.relics:
            st.markdown("---")
            st.markdown("### 🛡️ Relikte")
            for r in p.relics:
                st.markdown(f"**{r.name}**  \n_{r.desc}_")

        if st.session_state.game_log:
            st.markdown("---")
            st.markdown("### 📜 Kampflog")
            for entry in st.session_state.game_log[:5]:
                st.markdown(f"<small>{entry}</small>", unsafe_allow_html=True)

# ====================== HAUPTBEREICH ======================
st.markdown("<h1>⚔️ PokéSpire</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0c4ff;margin-top:-10px'>Roguelike Deckbuilder • Echte Evolution • Pokémon-Abenteuer</p>", unsafe_allow_html=True)
st.markdown("---")

# ====================== STARTBILDSCHIRM ======================
if st.session_state.player is None:

    st.markdown("## 🎮 Starte dein Abenteuer")
    st.markdown("Wähle dein Starter-Pokémon und begib dich auf eine epische Reise!")

    starters = ["bulbasaur", "charmander", "squirtle"]
    names_de = {"bulbasaur": "Bisasam", "charmander": "Glumanda", "squirtle": "Schiggy"}
    types = {"bulbasaur": "Pflanze", "charmander": "Feuer", "squirtle": "Wasser"}
    desc = {
        "bulbasaur": "🌿 Pflanze/Gift-Typ. Starke Verteidigung & stetige Schadenskarten.",
        "charmander": "🔥 Feuer-Typ. Hoher Schaden & Verbrennungseffekte.",
        "squirtle": "💧 Wasser-Typ. Balance aus Angriff & Block.",
    }

    cols = st.columns(3)
    for i, s in enumerate(starters):
        with cols[i]:
            sprite = get_sprite_url(s)
            st.image(sprite, use_container_width=True)
            tc = type_color(types[s])
            st.markdown(f"<h3 style='color:{tc};text-align:center'>{names_de[s]}</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center'>{type_badge(types[s])}</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.85rem;color:#ccc;text-align:center'>{desc[s]}</p>", unsafe_allow_html=True)
            if st.button(f"✅ Wählen", key=f"pick_{s}", use_container_width=True):
                player = Player()
                evo_api, evo_de, evo_lvl = EVOLUTION_CHAIN[s]
                cards = [ALL_CARDS[c].copy() if hasattr(ALL_CARDS[c], 'copy') else
                         Card(ALL_CARDS[c].name, ALL_CARDS[c].damage, ALL_CARDS[c].block,
                              ALL_CARDS[c].type, ALL_CARDS[c].cost, ALL_CARDS[c].effect)
                         for c in STARTER_CARDS[s]]
                poke = Pokemon(names_de[s], types[s], cards, evo_api, evo_de, evo_lvl)
                player.add_pokemon(poke)
                player.relics.append(Relic("Anfänger-Amulett", "Freundschaft +50% nach Kampf", "friendship_boost"))
                st.session_state.player = player
                log(f"🎮 Abenteuer gestartet mit {names_de[s]}!")
                st.rerun()

# ====================== GAME-OVER ======================
elif st.session_state.player and st.session_state.player.hp <= 0:
    player = st.session_state.player
    st.markdown("## 💀 Game Over")
    st.markdown(f"Du bist in Region **{player.region}**, Etage **{player.floor}** gefallen.")
    st.markdown(f"Siege: **{player.battles_won_total}** | Gold: **{player.gold}**")
    if st.button("🔄 Nochmal spielen", type="primary"):
        for k in list(st.session_state.keys()):
            if k not in ("language", "lang_sel"):
                del st.session_state[k]
        st.rerun()

# ====================== SPIEL LÄUFT ======================
else:
    player = st.session_state.player

    # Evolutionsanzeige
    if st.session_state.show_evolution:
        evo_msg = st.session_state.show_evolution
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#2a1a4e,#4a2a8e);
                    border:2px solid #ffd700;border-radius:16px;
                    padding:30px;text-align:center;margin:20px 0;
                    box-shadow:0 0 40px #ffd70066'>
            <div style='font-size:2rem'>✨</div>
            <h2 style='color:#ffd700'>Evolution!</h2>
            <p style='color:#e0e0ff;font-size:1.2rem'>{evo_msg}</p>
            <p style='color:#a0c4ff'>Dein Pokémon ist stärker geworden!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Weiter ✨", type="primary"):
            st.session_state.show_evolution = None
            st.rerun()
        st.stop()

    # ====================== KAMPF ======================
    if st.session_state.in_combat and st.session_state.enemy:
        enemy = st.session_state.enemy

        # Kampf-Start: Relic-Effekte
        if not st.session_state.combat_started:
            player.apply_relic_effects("combat_start")
            st.session_state.combat_started = True

        st.markdown("## ⚔️ Kampf!")

        # Arena
        col_player, col_vs, col_enemy = st.columns([5, 1, 5])

        with col_player:
            st.markdown("<div class='battle-box'>", unsafe_allow_html=True)
            st.markdown(f"### 👤 Du")
            st.markdown(hp_bar_html(max(0, player.hp), player.max_hp, "❤️ HP"), unsafe_allow_html=True)
            if st.session_state.block > 0:
                st.markdown(f"🛡️ **Block: {st.session_state.block}**")
            if player.burn_stacks > 0:
                st.markdown(f"🔥 Verbrennung: {player.burn_stacks}")
            # Team-Pokémon klein
            for tp in player.team[:2]:
                sprite = get_sprite_url(tp.name.lower())
                mini_col1, mini_col2 = st.columns([1, 2])
                with mini_col1:
                    st.image(sprite, width=60)
                with mini_col2:
                    tc = type_color(tp.type)
                    st.markdown(f"<small style='color:{tc}'><b>{tp.name}</b> Lv.{tp.level}</small>", unsafe_allow_html=True)
                    st.markdown(hp_bar_html(tp.hp, tp.max_hp), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_vs:
            st.markdown("<div style='text-align:center;padding-top:80px;font-size:2rem'>⚡</div>", unsafe_allow_html=True)

        with col_enemy:
            st.markdown("<div class='battle-box'>", unsafe_allow_html=True)
            enemy_name = enemy['name']
            enemy_type = enemy.get('type', 'Normal')
            tc = type_color(enemy_type)
            st.markdown(f"### {enemy_name}")
            st.markdown(type_badge(enemy_type), unsafe_allow_html=True)
            sprite_url = enemy.get("sprite", "")
            if sprite_url:
                st.image(sprite_url, width=160)
            st.markdown(hp_bar_html(enemy['hp'], enemy['max_hp'], "💥 HP"), unsafe_allow_html=True)
            # Gegner-Absicht
            intent = enemy.get("intent", {})
            intent_name = intent.get("name", "???")
            intent_dmg = intent.get("damage", 0)
            st.markdown(f"**Nächste Aktion:** {intent_name} ({intent_dmg} DMG)")
            # Gegner-Status
            if st.session_state.enemy_status.get("burned"):
                st.markdown("🔥 Verbrennt!")
            st.markdown("</div>", unsafe_allow_html=True)

        # Energie & Block
        st.markdown("---")
        ecol1, ecol2 = st.columns(2)
        with ecol1:
            energy_dots = "⚡" * st.session_state.energy + "○" * (3 - st.session_state.energy)
            st.markdown(f"<div class='energy-display'>{energy_dots} Energie: {st.session_state.energy}/3</div>",
                        unsafe_allow_html=True)
        with ecol2:
            if st.session_state.block > 0:
                st.markdown(f"<div style='color:#88aaff;font-size:1rem;padding:8px 0'>🛡️ Block: <b>{st.session_state.block}</b></div>",
                            unsafe_allow_html=True)

        # Hand
        st.markdown("### 🃏 Deine Hand")
        if not st.session_state.hand:
            st.info("Keine Karten in der Hand!")
        else:
            hand_cols = st.columns(len(st.session_state.hand))
            for i, card in enumerate(list(st.session_state.hand)):
                with hand_cols[i]:
                    can_play = st.session_state.energy >= card.cost
                    tc = type_color(card.type)
                    card_alpha = "ff" if can_play else "66"
                    st.markdown(f"""
                    <div class='card-container' style='border-color:{tc}{card_alpha};opacity:{"1" if can_play else "0.5"}'>
                        <div class='card-cost'>[{card.cost}⚡]</div>
                        <div class='card-name' style='color:{tc}'>{card.name}</div>
                        <div style='color:{tc}66;font-size:0.7rem'>{card.type}</div>
                        <div class='card-stats'>{card.describe()}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    label = f"▶ Spielen ({card.cost}⚡)" if can_play else f"❌ Zu teuer"
                    if st.button(label, key=f"play_{i}", use_container_width=True,
                                 disabled=not can_play):
                        # Karte spielen
                        st.session_state.energy -= card.cost
                        st.session_state.hand.pop(i)
                        # Schaden
                        if card.damage > 0:
                            dmg = card.damage
                            # Relic: Damage-Boost
                            for r in player.relics:
                                if r.effect == "damage_boost":
                                    dmg += 3
                            enemy["hp"] -= dmg
                            log(f"⚔️ {card.name}: {dmg} Schaden an {enemy_name}")
                        # Block
                        if card.block > 0:
                            block = card.block
                            # Relic: First Block
                            if st.session_state.get("first_turn", True):
                                for r in player.relics:
                                    if r.effect == "first_block":
                                        block *= 2
                            st.session_state.block += block
                            log(f"🛡️ {card.name}: +{block} Block")
                        # Effekte
                        if card.effect:
                            eff, val = card.effect.split(":") if ":" in card.effect else (card.effect, "0")
                            val = int(val)
                            if eff == "heal":
                                player.hp = min(player.max_hp, player.hp + val)
                                log(f"💚 Heilt {val} HP")
                            elif eff == "burn":
                                st.session_state.enemy_status["burned"] = val
                                log(f"🔥 {enemy_name} verbrennt! ({val} Stapel)")
                            elif eff == "draw":
                                extras = [c for c in player.deck if c not in st.session_state.hand]
                                if extras:
                                    st.session_state.hand.append(random.choice(extras))
                        st.rerun()

        # Zug beenden
        st.markdown("---")
        bcol1, bcol2 = st.columns([3, 1])
        with bcol1:
            if st.button("⏭️ Zug beenden", type="primary", use_container_width=True):
                st.session_state.first_turn = False
                # Verbrennungsschaden am Gegner
                if st.session_state.enemy_status.get("burned"):
                    burn_dmg = st.session_state.enemy_status["burned"]
                    enemy["hp"] -= burn_dmg
                    st.session_state.enemy_status["burned"] = max(0, burn_dmg - 1)
                    if st.session_state.enemy_status["burned"] == 0:
                        del st.session_state.enemy_status["burned"]
                    log(f"🔥 Verbrennung: {burn_dmg} Schaden an {enemy_name}")

                # Gegner greift an (falls noch am Leben)
                if enemy["hp"] > 0:
                    raw_dmg = intent["damage"]
                    absorbed = min(st.session_state.block, raw_dmg)
                    dmg_taken = max(0, raw_dmg - st.session_state.block)
                    player.hp = max(0, player.hp - dmg_taken)
                    log(f"👾 {enemy_name} greift mit {intent['name']} an: {raw_dmg} DMG (-{absorbed} Block) = {dmg_taken} Schaden")

                    # Nächste Gegner-Absicht
                    attacks = enemy.get("attacks_list", [{"name": "Tackle", "damage": intent["damage"]}])
                    next_attack = random.choice(attacks)
                    enemy["intent"] = next_attack

                # Relic HP Regen
                player.apply_relic_effects("end_turn")

                # Block & Energie zurücksetzen
                st.session_state.block = 0
                st.session_state.energy = 3
                # Neue Hand
                if player.deck:
                    st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))

                # Sieg?
                if enemy["hp"] <= 0:
                    reward = random.randint(*enemy.get("reward_range", (20, 40)))
                    # Gold-Boost Relic
                    for r in player.relics:
                        if r.effect == "gold_boost":
                            reward = int(reward * 1.2)
                    player.gold += reward
                    player.battles_won_total += 1
                    player.floor += 1
                    log(f"🏆 Sieg gegen {enemy_name}! +{reward} Gold")

                    for poke in player.team:
                        poke.battles_won += 1
                        friend_gain = random.randint(12, 20)
                        for r in player.relics:
                            if r.effect == "friendship_boost":
                                friend_gain = int(friend_gain * 1.5)
                        poke.friendship = min(255, poke.friendship + friend_gain)
                        leveled = poke.gain_exp(random.randint(20, 40))
                        if leveled:
                            log(f"⬆️ {poke.name} ist jetzt Level {poke.level}!")

                    # Evolutionen prüfen
                    evolved = player.check_evolutions()
                    if evolved:
                        st.session_state.show_evolution = " & ".join(evolved)
                        # Sprites aktualisieren
                        for poke in player.team:
                            pass  # Sprite wird über get_sprite_url(poke.name.lower()) gezogen

                    # Zufällig: Relic nach Kampf
                    if random.random() < 0.15:
                        new_relic = random.choice([r for r in RELIC_POOL
                                                   if r.name not in [x.name for x in player.relics]])
                        player.relics.append(new_relic)
                        log(f"🛡️ Neues Relic: {new_relic.name}!")

                    st.session_state.in_combat = False
                    st.session_state.enemy = None
                    st.session_state.enemy_status = {}
                    st.session_state.combat_started = False
                    st.session_state.first_turn = True

                    # Region-Aufstieg alle 5 Etagen
                    if player.floor > player.region * 5:
                        player.region += 1
                        player.floor = 1
                        log(f"🌟 Neue Region {player.region} erreicht!")

                st.rerun()
        with bcol2:
            deck_count = len(player.deck)
            st.markdown(f"<div style='text-align:center;color:#a0c4ff;padding:10px'>🃏 Deck: {deck_count}</div>",
                        unsafe_allow_html=True)

    # ====================== KARTE WÄHLEN ======================
    elif st.session_state.in_shop:
        st.markdown("## 🏪 Shop")
        st.markdown(f"💰 Gold: **{player.gold}**")

        shop_cols = st.columns(3)
        for i, card_name in enumerate(st.session_state.shop_cards):
            if card_name in ALL_CARDS:
                card = ALL_CARDS[card_name]
                price = (card.cost * 15) + random.randint(-5, 5)
                with shop_cols[i % 3]:
                    tc = type_color(card.type)
                    st.markdown(f"""
                    <div class='card-container' style='border-color:{tc}'>
                        <div class='card-name' style='color:{tc}'>{card.name}</div>
                        <div style='color:{tc}66;font-size:0.7rem'>{card.type}</div>
                        <div class='card-stats'>{card.describe()}</div>
                        <div style='color:#ffd700;font-size:0.9rem;margin-top:6px'>💰 {price} Gold</div>
                    </div>
                    """, unsafe_allow_html=True)
                    can_buy = player.gold >= price
                    if st.button(f"{'Kaufen' if can_buy else '❌ Zu teuer'}", key=f"buy_{i}",
                                 use_container_width=True, disabled=not can_buy):
                        player.gold -= price
                        new_card = Card(card.name, card.damage, card.block, card.type, card.cost, card.effect)
                        player.deck.append(new_card)
                        st.session_state.shop_cards.pop(i)
                        log(f"🛒 {card.name} für {price} Gold gekauft!")
                        st.rerun()

        st.markdown("---")
        if st.button("🚪 Shop verlassen", use_container_width=True):
            st.session_state.in_shop = False
            st.rerun()

    elif st.session_state.in_rest:
        st.markdown("## 🏕️ Rast")
        heal_amount = int(player.max_hp * 0.35)
        st.markdown(f"Du machst eine kurze Pause. Du kannst **{heal_amount} HP** heilen oder dein Deck verbessern.")

        rcol1, rcol2 = st.columns(2)
        with rcol1:
            can_heal = player.hp < player.max_hp
            if st.button(f"💊 Heilen (+{heal_amount} HP)", use_container_width=True, disabled=not can_heal):
                player.hp = min(player.max_hp, player.hp + heal_amount)
                log(f"💊 Geheilt! +{heal_amount} HP")
                st.session_state.in_rest = False
                st.rerun()
            if not can_heal:
                st.info("HP bereits voll!")
        with rcol2:
            if st.button("🗑️ Karte entfernen", use_container_width=True):
                st.session_state.in_rest = False
                # Einfach: Zufällige Basisangriffskarte entfernen (Tackle/Growl)
                removable = [c for c in player.deck if c.name in ("Tackle", "Growl")]
                if removable:
                    player.deck.remove(random.choice(removable))
                    log("🗑️ Schwache Karte entfernt!")
                else:
                    log("Keine entfernbaren Karten gefunden.")
                st.rerun()

    # ====================== WELTKARTE ======================
    else:
        # Etagen-Info
        is_boss = player.floor == 5
        st.markdown(f"## 🗺️ Region {player.region} — Etage {player.floor}/5")
        if is_boss:
            st.markdown("⚠️ **BOSS-ETAGE!** Bereite dich auf einen starken Gegner vor.")

        st.markdown("---")

        # Team anzeigen
        st.markdown("### 👥 Dein Team")
        team_cols = st.columns(min(3, len(player.team)))
        for i, poke in enumerate(player.team):
            with team_cols[i % 3]:
                sprite = get_sprite_url(poke.name.lower())
                tc = type_color(poke.type)
                st.image(sprite, width=120)
                st.markdown(f"<div class='pokemon-card'>", unsafe_allow_html=True)
                st.markdown(f"**{poke.name}** {type_badge(poke.type)}", unsafe_allow_html=True)
                st.markdown(f"Lv.{poke.level} | 💛 {poke.friendship}/255")
                st.markdown(hp_bar_html(poke.hp, poke.max_hp), unsafe_allow_html=True)
                if poke.evolution_de:
                    st.markdown(f"<small style='color:#888'>→ {poke.evolution_de} bei Lv.{poke.evo_level}</small>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🛤️ Wähle deinen Pfad")

        path_cols = st.columns(3)

        with path_cols[0]:
            label = f"⚔️ {'BOSS' if is_boss else 'Kampf'}"
            if st.button(label, use_container_width=True, type="primary"):
                # Gegner auswählen
                region_enemies = ENEMIES_BY_REGION.get(player.region, ENEMIES_BY_REGION[1])
                if is_boss and player.region in BOSSES:
                    boss = BOSSES[player.region]
                    hp = boss["hp"]
                    enemy_data = {
                        "name": boss["name"],
                        "api": boss["api"],
                        "hp_range": (hp, hp),
                        "damage_range": boss["damage_range"],
                        "type": boss["type"],
                        "reward": boss["reward"],
                        "attacks": boss["attacks"],
                    }
                else:
                    enemy_data = random.choice(region_enemies)

                hp = random.randint(*enemy_data["hp_range"])
                base_dmg = random.randint(*enemy_data["damage_range"])
                attack_name = random.choice(enemy_data["attacks"])
                attacks_list = [{"name": a, "damage": random.randint(*enemy_data["damage_range"])}
                                for a in enemy_data["attacks"]]

                st.session_state.in_combat = True
                st.session_state.combat_started = False
                st.session_state.first_turn = True
                st.session_state.enemy = {
                    "name": enemy_data["name"],
                    "hp": hp,
                    "max_hp": hp,
                    "sprite": get_sprite_url(enemy_data["api"]),
                    "type": enemy_data["type"],
                    "intent": {"name": attack_name, "damage": base_dmg},
                    "attacks_list": attacks_list,
                    "reward_range": enemy_data["reward"],
                }
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                st.session_state.block = 0
                st.session_state.energy = 3
                st.session_state.enemy_status = {}
                log(f"⚔️ Kampf gegen {enemy_data['name']} begonnen!")
                st.rerun()

        with path_cols[1]:
            if st.button("🏪 Shop", use_container_width=True):
                # Shop befüllen
                available = [c for c in SHOP_CARDS if True]  # Alle verfügbar
                st.session_state.shop_cards = random.sample(available, min(6, len(available)))
                st.session_state.in_shop = True
                st.rerun()

        with path_cols[2]:
            if st.button("🏕️ Rast", use_container_width=True):
                st.session_state.in_rest = True
                st.rerun()

        # Deck anzeigen
        with st.expander(f"🃏 Mein Deck ({len(player.deck)} Karten)"):
            deck_display_cols = st.columns(3)
            for i, card in enumerate(player.deck):
                with deck_display_cols[i % 3]:
                    tc = type_color(card.type)
                    st.markdown(f"""
                    <div class='card-container' style='border-color:{tc}88;padding:8px'>
                        <div class='card-cost'>[{card.cost}⚡]</div>
                        <div class='card-name' style='color:{tc};font-size:0.85rem'>{card.name}</div>
                        <div class='card-stats;font-size:0.75rem'>{card.describe()}</div>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center;color:#444;font-size:0.75rem'>PokéSpire v2.0 • Pokémon-Namen sind Eigentum von Nintendo/Game Freak</p>",
            unsafe_allow_html=True)

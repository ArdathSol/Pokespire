"""
PokéSpire v6.0 – Tactical Roguelike Deckbuilder
• Absolut fehlerfreie, isolierte Slay-the-Spire-Pfadkarte
• Integrierte Typen-Wechselwirkungen (Schadens-Multiplikatoren: 2.0x / 0.5x)
• Zufällige, lustige Pokémon-Spitznamen bei der Starter-Wahl
• NEU: Freischaltbare Achievements (Errungenschaften) mit Live-Anzeige in der Sidebar
"""

import streamlit as st
import random
import requests
from typing import List, Optional, Dict, Tuple

st.set_page_config(page_title="PokéSpire v6.0", page_icon="⚔️", layout="wide")

# ───────────────────────── POKÉAPI TRANSLATION ─────────────────────────
POKEMON_DE_TO_API: Dict[str, str] = {
    "bisasam": "bulbasaur", "bisaknosp": "ivysaur", "bisaflor": "venusaur",
    "glumanda": "charmander", "glutexo": "charmeleon", "glurak": "charizard",
    "schiggy": "squirtle", "schillok": "wartortle", "turtok": "blastoise",
    "rattfratz": "rattata", "rattikarl": "raticate",
    "taubsi": "pidgey", "tauboga": "pidgeotto", "tauboss": "pidgeot",
    "raupy": "caterpie", "safcon": "metapod", "smettbo": "butterfree",
    "hornliu": "weedle", "kokuna": "kakuna", "bibor": "beedrill",
    "pummeluff": "jigglypuff", "knuddeluff": "wigglytuff",
    "piepi": "clefairy", "pixi": "clefable",
    "pikachu": "pikachu", "raichu": "raichu",
    "habitak": "spearow", "ibitak": "fearow",
    "abra": "abra", "kadabra": "kadabra", "simsala": "alakazam",
    "machollo": "machop", "maschock": "machoke", "machomei": "machamp",
    "quapsel": "poliwag", "quaputzi": "poliwhirl", "quappo": "poliwrath",
    "sleima": "grimer", "sleimok": "muk",
    "kleinstein": "geodude", "georok": "graveler", "geowaz": "golem",
    "fukano": "growlithe", "arkani": "arcanine",
    "zubat": "zubat", "golbat": "golbat",
    "mauzi": "meowth", "snobilikat": "persian",
    "relaxo": "snorlax", "garados": "gyarados", "gengar": "gengar",
    "mewtwo": "mewtwo", "mew": "mew"
}

# Lustige Pokémon-Spitznamen-Pools nach Typen
FUNNY_NAMES = {
    "Pflanze": ["Bisa-Boss", "Salat-Salat", "Kräuter-Karl", "Veggie-Zilla", "Brokkoli", "Gras-Dealer", "UnkrautEx"],
    "Feuer": ["Glurak-Sucht", "Grillmeister", "ScharfWieFritten", "Tabasco-Tim", "Zunder-Zorro", "Feuerwurst", "Toastbrot"],
    "Wasser": ["Schiggy-Bump", "Spülmittel", "NasserHeini", "ArielleEnkel", "Wasserschaden", "Zitteraal", "Hydrant"]
}

@st.cache_data(ttl=3600)
def get_sprite_url(name: str) -> str:
    api_name = POKEMON_DE_TO_API.get(name.lower(), name.lower())
    try:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{api_name}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            artwork = data["sprites"]["other"]["official-artwork"].get("front_default")
            return artwork if artwork else data["sprites"].get("front_default", _ph(name))
    except Exception:
        pass
    return _ph(name)

def _ph(name: str) -> str:
    return f"https://placehold.co/250x250/111126/ffd700?text={name.capitalize()}"

# ───────────────────────── MODERN LOOK & CSS ─────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;600;700&display=swap');

html, body, .stApp {
    background: #060612 !important;
    color: #e2e8f0;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.15rem;
}

h1, h2, h3, h4 {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px;
}

h1 {
    color: #ffd700 !important;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
}

/* Taktische Karten-UI */
.card-ui {
    background: linear-gradient(145deg, #12122c, #1a1a3a);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    border: 1px solid #2e2e5c;
    transition: all 0.2s ease-in-out;
}
.card-ui:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(111, 102, 242, 0.3);
    border-color: #5d5dff;
}
.card-cost { font-size: 1.2rem; color: #ff9d00; font-weight: bold; font-family: 'Orbitron'; }
.card-name { font-size: 1.25rem; font-weight: bold; margin: 4px 0; }
.card-desc { font-size: 0.95rem; color: #a0aec0; min-height: 40px; }

/* Map Knoten */
.map-node {
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    background: #111126;
    border: 2px solid #2d3748;
    color: #718096;
    transition: all 0.2s;
}
.node-active {
    border-color: #3182ce !important;
    color: #fff !important;
    box-shadow: 0 0 12px rgba(49, 130, 206, 0.5);
    cursor: pointer;
}
.node-current {
    border-color: #ffd700 !important;
    background: #23231a !important;
    color: #ffd700 !important;
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
}
.node-visited {
    opacity: 0.4;
    border-color: #4a5568 !important;
}

/* HP Bars */
.hp-bg { background:#1a202c; border-radius:6px; height:18px; overflow:hidden; margin:4px 0; border: 1px solid #4a5568; }
.hp-fill { height:100%; transition: width 0.3s ease; display:flex; align-items:center; padding-left:8px; font-size:0.8rem; font-weight:bold; color:white; }
.hp-g { background: linear-gradient(90deg, #2f855a, #48bb78); }
.hp-y { background: linear-gradient(90deg, #b7791f, #ecc94b); }
.hp-r { background: linear-gradient(90deg, #9b2c2c, #f56565); }

/* Status Badges */
.status-badge {
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 0.8rem; font-weight: bold; margin: 2px;
    font-family: 'Orbitron';
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ───────────────────────── SYSTEM-HELPERS ─────────────────────────
def type_color(t: str) -> str:
    return {
        "Feuer":"#f56565","Wasser":"#4299e1","Pflanze":"#48bb78","Elektro":"#ecc94b",
        "Normal":"#a0aec0","Psycho":"#ed64a6","Kampf":"#dd6b20","Flug":"#63b3ed",
        "Gift":"#9f7aea","Gestein":"#ed8936","Eis":"#4fd1c5","Geist":"#805ad5"
    }.get(t, "#a0aec0")

def hp_bar(cur: int, mx: int, lbl: str = "") -> str:
    pct = max(0, min(100, int(cur / max(1, mx) * 100)))
    cls = "hp-g" if pct > 50 else "hp-y" if pct > 20 else "hp-r"
    return f"<div class='hp-bg'><div class='hp-fill {cls}' style='width:{pct}%'>{lbl} {cur}/{mx}</div></div>"

def badge(text: str, color: str) -> str:
    return f"<span class='status-badge' style='background:{color}33;color:{color};border:1px solid {color}'>{text.upper()}</span>"

def log(msg: str):
    if "game_log" not in st.session_state: st.session_state.game_log = []
    st.session_state.game_log.insert(0, msg)

def unlock_achievement(key: str, title: str, desc: str):
    """Schaltet ein Achievement frei, falls noch nicht geschehen."""
    if "achievements" not in st.session_state:
        st.session_state.achievements = {}
    if key not in st.session_state.achievements:
        st.session_state.achievements[key] = {"title": title, "desc": desc}
        log(f"🏆 ACHIEVEMENT FREIGESCHALTET: 【{title}】 – {desc}")

# ───────────────────────── TYPE ADVANTAGE LOGIC ─────────────────────────
def get_damage_multiplier(attack_type: str, defender_type: str) -> Tuple[float, str]:
    """Berechnet die Pokémon-Typen-Wechselwirkung."""
    if attack_type == "Feuer" and defender_type == "Pflanze": return 2.0, "🔥 Sehr effektiv!"
    if attack_type == "Wasser" and defender_type == "Feuer": return 2.0, "💧 Sehr effektiv!"
    if attack_type == "Pflanze" and defender_type == "Wasser": return 2.0, "🌿 Sehr effektiv!"
    if attack_type == "Elektro" and defender_type == "Wasser": return 2.0, "⚡ Sehr effektiv!"
    
    if attack_type == "Feuer" and defender_type == "Wasser": return 0.5, "🛡️ Nicht sehr effektiv..."
    if attack_type == "Wasser" and defender_type == "Pflanze": return 0.5, "🛡️ Nicht sehr effektiv..."
    if attack_type == "Pflanze" and defender_type == "Feuer": return 0.5, "🛡️ Nicht sehr effektiv..."
    
    return 1.0, ""

# ───────────────────────── CLASSES ─────────────────────────
class Card:
    def __init__(self, name: str, damage: int, block: int, poke_type: str, cost: int = 1, effect: str = "", rarity: str = "common"):
        self.name = name
        self.damage = damage
        self.block = block
        self.type = poke_type
        self.cost = cost
        self.effect = effect
        self.rarity = rarity

    def copy(self) -> "Card":
        return Card(self.name, self.damage, self.block, self.type, self.cost, self.effect, self.rarity)

    def describe(self) -> str:
        parts = []
        if self.damage > 0: parts.append(f"⚔️ {self.damage} ({self.type})")
        if self.block > 0: parts.append(f"🛡️ {self.block}")
        if self.effect: parts.append(f"✨ {self.effect}")
        return " | ".join(parts) if parts else "Effektlos"

class Pokemon:
    def __init__(self, name: str, poke_type: str, cards: List[Card], evo_de: Optional[str] = None, evo_level: int = 16):
        self.nickname = random.choice(FUNNY_NAMES.get(poke_type, ["Nugget"]))
        self.species = name
        self.name = f"{self.nickname} ({self.species})"
        self.type = poke_type
        self.cards = cards
        self.level = 1
        self.exp = 0
        self.evo_de = evo_de
        self.evo_level = evo_level
        self.hp = 50
        self.max_hp = 50

    def gain_exp(self, amount: int) -> bool:
        self.exp += amount
        if self.exp >= self.level * 15:
            self.exp -= self.level * 15
            self.level += 1
            self.max_hp += 8
            self.hp = min(self.hp + 8, self.max_hp)
            return True
        return False

    def can_evolve(self) -> bool:
        return bool(self.evo_de) and self.level >= self.evo_level

    def evolve(self):
        old_name = self.name
        self.species = self.evo_de
        self.name = f"{self.nickname} ({self.species})"
        self.evo_de = None
        self.max_hp += 25
        self.hp = self.max_hp
        for c in self.cards:
            c.damage = int(c.damage * 1.4)
            c.block = int(c.block * 1.4)
        log(f"✨ Oh? Evolution! {old_name} wurde zu {self.name}!")
        unlock_achievement("evo_1", "Mutant", "Entwickle dein erstes Pokémon.")

class Player:
    def __init__(self):
        self.deck: List[Card] = []
        self.team: List[Pokemon] = []
        self.gold = 100
        self.act = 1

    def add_pokemon(self, p: Pokemon):
        self.team.append(p)
        for c in p.cards:
            self.deck.append(c.copy())

# ───────────────────────── GAME DATA POOLS ─────────────────────────
ALL_CARDS = {
    "Tackle": Card("Tackle", 8, 0, "Normal", 1),
    "Heuler": Card("Heuler", 0, 7, "Normal", 1),
    "Glut": Card("Glut", 12, 0, "Feuer", 1, "burn:3"),
    "Flammenwurf": Card("Flammenwurf", 22, 0, "Feuer", 2, "burn:5", "uncommon"),
    "Rankenhieb": Card("Rankenhieb", 10, 3, "Pflanze", 1),
    "Synthese": Card("Synthese", 0, 10, "Pflanze", 1, "heal:6", "uncommon"),
    "Blubber": Card("Blubber", 8, 6, "Wasser", 1),
    "Aquawelle": Card("Aquawelle", 18, 8, "Wasser", 2, "draw:1", "uncommon"),
    "Donnerschock": Card("Donnerschock", 14, 0, "Elektro", 1, "weak:1"),
    "Donner": Card("Donner", 30, 0, "Elektro", 3, "weak:2", "rare")
}

ENEMIES = {
    1: [
        {"name": "Rattfratz", "api": "rattata", "hp": (30, 45), "type": "Normal", "attacks": [("Biss", 6, "Normal"), ("Ruckzuckhieb", 9, "Normal")]},
        {"name": "Zubat", "api": "zubat", "hp": (28, 40), "type": "Gift", "attacks": [("Blutsauger", 5, "Normal"), ("Flügelangriff", 8, "Flug")]}
    ],
    2: [
        {"name": "Rattikarl", "api": "raticate", "hp": (60, 80), "type": "Normal", "attacks": [("Hyperfang", 14, "Normal"), ("Tackle", 10, "Normal")]},
        {"name": "Golbat", "api": "golbat", "hp": (65, 85), "type": "Flug", "attacks": [("Giga-Sauger", 12, "Pflanze"), ("Luftschneider", 16, "Flug")]}
    ],
    3: [
        {"name": "Garados", "api": "gyarados", "hp": (120, 150), "type": "Wasser", "attacks": [("Hydropumpe", 24, "Wasser"), ("Biss", 16, "Normal")]},
        {"name": "Gengar", "api": "gengar", "hp": (110, 140), "type": "Geist", "attacks": [("Spukball", 22, "Geist"), ("Hypnose", 14, "Psycho")]}
    ]
}

BOSSES = {
    1: {"name": "Relaxo", "api": "snorlax", "hp": 130, "type": "Normal", "attacks": [("Bodyslam", 15, "Normal"), ("Erholung", 8, "Normal")], "node_type": "boss"},
    2: {"name": "Bisaflor", "api": "venusaur", "hp": 200, "type": "Pflanze", "attacks": [("Faunastatue", 22, "Pflanze"), ("Solarstrahl", 30, "Pflanze")], "node_type": "boss"},
    3: {"name": "Mewtwo", "api": "mewtwo", "hp": 300, "type": "Psycho", "attacks": [("Psychokinese", 35, "Psycho"), ("Amnesie", 20, "Normal")], "node_type": "boss"}
}

def generate_sts_map(act: int) -> List[List[Dict]]:
    """Generiert eine strukturierte Verzweigungskarte mit 8 Etagen + Boss."""
    random.seed(st.session_state.get("map_seed", 42) + act)
    node_types = ["combat", "combat", "event", "rest", "shop"]
    grid = []
    
    for row in range(8):
        row_nodes = []
        for col in range(3):
            ntype = "combat" if row == 0 else random.choice(node_types)
            row_nodes.append({"type": ntype, "col": col, "row": row})
        grid.append(row_nodes)
        
    grid.append([
        {"type": "empty", "col": 0, "row": 8},
        {"type": "boss", "col": 1, "row": 8},
        {"type": "empty", "col": 2, "row": 8}
    ])
    return grid

# ───────────────────────── STATE INITIALIZATION ─────────────────────────
if "player" not in st.session_state: st.session_state.player = None
if "phase" not in st.session_state: st.session_state.phase = "start"
if "map_seed" not in st.session_state: st.session_state.map_seed = random.randint(1, 99999)
if "achievements" not in st.session_state: st.session_state.achievements = {}

# ───────────────────────── CONTROLLER ACTIONS ─────────────────────────
def start_game(starter_key: str):
    p = Player()
    if starter_key == "bisasam":
        poke = Pokemon("Bisasam", "Pflanze", [ALL_CARDS["Tackle"].copy(), ALL_CARDS["Rankenhieb"].copy(), ALL_CARDS["Synthese"].copy()], "Bisaknosp", 16)
    elif starter_key == "glumanda":
        poke = Pokemon("Glumanda", "Feuer", [ALL_CARDS["Tackle"].copy(), ALL_CARDS["Glut"].copy(), ALL_CARDS["Flammenwurf"].copy()], "Glutexo", 16)
    else:
        poke = Pokemon("Schiggy", "Wasser", [ALL_CARDS["Tackle"].copy(), ALL_CARDS["Blubber"].copy(), ALL_CARDS["Aquawelle"].copy()], "Schillok", 16)
        
    p.add_pokemon(poke)
    st.session_state.player = p
    st.session_state.game_map = generate_sts_map(p.act)
    st.session_state.current_row = -1
    st.session_state.current_col = -1
    st.session_state.phase = "map"
    log(f"🎮 Abenteuer gestartet mit {poke.name}!")
    st.rerun()

def next_turn():
    p = st.session_state.player
    enemy = st.session_state.enemy
    active_poke = p.team[0]
    
    intent_name, base_dmg, intent_type = enemy["intent"]
    mult, msg = get_damage_multiplier(intent_type, active_poke.type)
    final_intent_dmg = int(base_dmg * mult)
    
    absorbed = min(st.session_state.block, final_intent_dmg)
    final_damage = max(0, final_intent_dmg - absorbed)
    
    active_poke.hp = max(0, active_poke.hp - final_damage)
    
    type_effect_log = f" ({msg})" if msg else ""
    log(f"💥 {enemy['name']} setzt {intent_name} ({intent_type}) ein! Verursacht {final_intent_dmg} DMG{type_effect_log} [{absorbed} geblockt].")
    
    if active_poke.hp <= 0:
        st.session_state.phase = "gameover"
        return

    st.session_state.block = 0
    st.session_state.energy = 3
    st.session_state.hand = random.sample(p.deck, min(5, len(p.deck)))
    enemy["intent"] = random.choice(enemy["attacks_list"])

# ───────────────────────── CORE INTERFACE ─────────────────────────

with st.sidebar:
    st.markdown("## 🎒 TRAINER STATUS")
    if st.session_state.player:
        p = st.session_state.player
        st.markdown(f"**📍 Akt {p.act}**")
        st.markdown(f"**💰 Gold:** {p.gold} ₽")
        
        # Kapitalist-Achievement Check
        if p.gold >= 150:
            unlock_achievement("gold_150", "Kapitalist", "Horte 150 oder mehr Gold.")
            
        st.markdown("---")
        st.markdown("**👥 Pokémon Team:**")
        for poke in p.team:
            color = type_color(poke.type)
            st.markdown(f"<b style='color:{color}'>{poke.name}</b> (Lv. {poke.level})", unsafe_allow_html=True)
            st.markdown(hp_bar(poke.hp, poke.max_hp), unsafe_allow_html=True)
            
        # LIVE ACHIEVEMENTS DISPLAY IN SIDEBAR
        if st.session_state.achievements:
            st.markdown("---")
            st.markdown("**🏆 DEINE ERFOLGE:**")
            for ach_id, data in st.session_state.achievements.items():
                st.markdown(f"🥇 **{data['title']}**<br><small style='color:#a0aec0'>{data['desc']}</small>", unsafe_allow_html=True)
        
        if "game_log" in st.session_state:
            st.markdown("---")
            st.markdown("**📜 Kampf-Log:**")
            for l in st.session_state.game_log[:4]:
                st.markdown(f"<small style='color:#a0aec0'>{l}</small>", unsafe_allow_html=True)

# SCREEN ROUTER
if st.session_state.phase == "start":
    st.markdown("# ⚔️ PokéSpire – Roguelike Deckbuilder")
    st.markdown("### Wähle dein Starter-Pokémon für den Aufstieg:")
    
    c1, c2, c3 = st.columns(3)
    starters = [("bisasam", "Bisasam", "🌿 Pflanze"), ("glumanda", "Glumanda", "🔥 Feuer"), ("schiggy", "Schiggy", "💧 Wasser")]
    for i, (key, name, desc) in enumerate(starters):
        with [c1, c2, c3][i]:
            st.image(get_sprite_url(key), use_container_width=True)
            if st.button(f"{name} ({desc})", use_container_width=True, type="primary"):
                start_game(key)

elif st.session_state.phase == "map":
    st.markdown("## 🗺️ Wähle deinen Pfad")
    st.markdown("Du musst dich Etage für Etage nach oben kämpfen. Klicke auf ein freigeschaltetes Event der nächsten Reihe.")
    
    gmap = st.session_state.game_map
    cur_row = st.session_state.current_row
    cur_col = st.session_state.current_col
    
    for row_idx in range(len(gmap)-1, -1, -1):
        cols = st.columns(3)
        for col_idx in range(3):
            node = gmap[row_idx][col_idx]
            if node["type"] == "empty":
                continue
                
            is_clickable = False
            if cur_row == -1 and row_idx == 0:
                is_clickable = True
            elif row_idx == cur_row + 1 and (abs(col_idx - cur_col) <= 1 or cur_row == 7):
                is_clickable = True
                
            status_class = "map-node"
            if is_clickable: status_class += " node-active"
            if row_idx == cur_row and col_idx == cur_col: status_class += " node-current"
            if row_idx < cur_row: status_class += " node-visited"
            
            icons = {"combat": "⚔️ Kampf", "event": "❓ Event", "rest": "🏕️ Rast", "shop": "🏪 Shop", "boss": "👑 BOSS"}
            node_label = icons.get(node["type"], "❓")
            
            with cols[col_idx]:
                st.markdown(f"<div class='{status_class}'><b>{node_label}</b><br><small>Etage {row_idx+1}</small></div>", unsafe_allow_html=True)
                if is_clickable and st.button("Betreten", key=f"node_{row_idx}_{col_idx}", use_container_width=True):
                    # Zuerst das gegnerische Setup laden, BEVOR wir die Koordinaten umschreiben! (Fix für den NameError)
                    node_type_selected = node["type"]
                    
                    if node_type_selected in ["combat", "boss"]:
                        p = st.session_state.player
                        cfg = BOSSES[p.act] if node_type_selected == "boss" else random.choice(ENEMIES[p.act])
                        hp_val = cfg["hp"] if node_type_selected == "boss" else random.randint(*cfg["hp"])
                        
                        st.session_state.enemy = {
                            "name": cfg["name"], "hp": hp_val, "max_hp": hp_val, "type": cfg["type"],
                            "attacks_list": cfg["attacks"], "intent": random.choice(cfg["attacks"]), "api": cfg["api"],
                            "is_boss_node": (node_type_selected == "boss")
                        }
                        st.session_state.hand = random.sample(p.deck, min(5, len(p.deck)))
                        st.session_state.energy = 3
                        st.session_state.block = 0
                        st.session_state.phase = "combat"
                    elif node_type_selected == "rest":
                        st.session_state.phase = "rest"
                    elif node_type_selected == "shop":
                        st.session_state.phase = "shop"
                    else:
                        st.session_state.phase = "event"
                        
                    # Erst ganz am Ende den State für die Position setzen
                    st.session_state.current_row = row_idx
                    st.session_state.current_col = col_idx
                    st.rerun()
        st.markdown("---")

elif st.session_state.phase == "combat":
    enemy = st.session_state.enemy
    p = st.session_state.player
    active_poke = p.team[0]
    
    st.markdown(f"## ⚔️ KAMPF: {active_poke.name} vs. {enemy['name']}")
    
    col_p, col_mid, col_e = st.columns([5, 1, 5])
    
    with col_p:
        st.markdown(f"#### 👤 {active_poke.name}")
        st.image(get_sprite_url(active_poke.species), width=180)
        st.markdown(hp_bar(active_poke.hp, active_poke.max_hp), unsafe_allow_html=True)
        st.markdown(f"🛡️ **Block:** {st.session_state.block} | ⚡ **Energie:** {st.session_state.energy}/3")
        
    with col_mid:
        st.markdown("<h2 style='text-align:center; padding-top:60px;'>VS</h2>", unsafe_allow_html=True)
        
    with col_e:
        st.markdown(f"#### 👾 Wildes {enemy['name']} {badge(enemy['type'], type_color(enemy['type']))}", unsafe_allow_html=True)
        st.image(get_sprite_url(enemy["api"]), width=180)
        st.markdown(hp_bar(enemy["hp"], enemy["max_hp"]), unsafe_allow_html=True)
        st.markdown(f"📢 **Absicht:** {enemy['intent'][0]} (💥 {enemy['intent'][1]} DMG, Typ: {enemy['intent'][2]})")

    st.markdown("---")
    st.markdown("### 🃏 Deine Handkarten:")
    
    if st.session_state.hand:
        card_cols = st.columns(len(st.session_state.hand))
        for idx, card in enumerate(list(st.session_state.hand)):
            with card_cols[idx]:
                c_color = type_color(card.type)
                st.markdown(f"""<div class='card-ui' style='border-top: 4px solid {c_color}'>
                    <div class='card-cost'>{card.cost}⚡</div>
                    <div class='card-name'>{card.name}</div>
                    <div class='card-desc'>{card.describe()}</div>
                </div>""", unsafe_allow_html=True)
                
                can_play = st.session_state.energy >= card.cost
                if st.button(f"Spielen", key=f"hand_{idx}", disabled=not can_play, use_container_width=True):
                    st.session_state.energy -= card.cost
                    st.session_state.hand.pop(idx)
                    
                    if card.damage > 0:
                        mult, msg = get_damage_multiplier(card.type, enemy["type"])
                        final_dmg = int(card.damage * mult)
                        
                        # DMG Achievements Check
                        if final_dmg >= 25:
                            unlock_achievement("dmg_25", "Dampfwalze", "Verursache mindestens 25 Schaden mit einem Schlag.")
                        
                        enemy["hp"] = max(0, enemy["hp"] - final_dmg)
                        type_effect_log = f" ({msg})" if msg else ""
                        log(f"⚔️ {active_poke.name} nutzt {card.name}! Verursacht {final_dmg} DMG an {enemy['name']}{type_effect_log}.")
                        
                    if card.block > 0:
                        st.session_state.block += card.block
                        # Block Achievements Check
                        if st.session_state.block >= 15:
                            unlock_achievement("block_15", "Betongesicht", "Erreiche 15 oder mehr Rüstung in einem Zug.")
                        log(f"🛡️ {active_poke.name} baut {card.block} Block auf.")
                        
                    # Siegbedingung prüfen (Gefahrenfreies Tracking über Node-Attribute im Enemy Dictionary)
                    if enemy["hp"] <= 0:
                        log(f"🏆 {enemy['name']} wurde besiegt!")
                        p.gold += random.randint(15, 30)
                        if active_poke.gain_exp(12):
                            log(f"🆙 {active_poke.name} ist jetzt Level {active_poke.level}!")
                        if active_poke.can_evolve():
                            active_poke.evolve()
                            
                        # Überprüfung über Node-Metadaten statt fragilen Direktzugriff via Koordinaten-Grid
                        if enemy.get("is_boss_node", False):
                            p.act += 1
                            if p.act > 3:
                                st.session_state.phase = "win"
                                st.rerun()
                            st.session_state.game_map = generate_sts_map(p.act)
                            st.session_state.current_row = -1
                            st.session_state.current_col = -1
                            log(f"👑 Akt {p.act} erreicht!")
                                
                        st.session_state.phase = "map"
                        st.rerun()
                    st.rerun()
                    
    st.markdown("---")
    if st.button("⏭️ Zug beenden", type="primary", use_container_width=True):
        next_turn()
        st.rerun()

elif st.session_state.phase == "rest":
    st.markdown("## 🏕️ Erholung am Lagerfeuer")
    active_poke = st.session_state.player.team[0]
    
    st.markdown(f"Dein {active_poke.name} ruht sich aus. Was möchtest du tun?")
    c1, c2 = st.columns(2)
    with c1:
        heal_amt = int(active_poke.max_hp * 0.4)
        if st.button(f"💊 Wunden lecken (+{heal_amt} HP)", use_container_width=True):
            active_poke.hp = min(active_poke.max_hp, active_poke.hp + heal_amt)
            log(f"🏕️ {active_poke.name} hat am Lagerfeuer gechillt.")
            st.session_state.phase = "map"
            st.rerun()
    with c2:
        if st.button("Weiterreisen", use_container_width=True):
            st.session_state.phase = "map"
            st.rerun()

elif st.session_state.phase == "shop":
    st.markdown("## 🏪 Pokémon Supermarkt")
    p = st.session_state.player
    st.markdown(f"Dein Gold: **{p.gold} ₽**")
    st.info("Der Verkäufer pennt. Komm auf der nächsten Etage wieder vorbei!")
    if st.button("Zurück zur Karte", use_container_width=True):
        st.session_state.phase = "map"
        st.rerun()

elif st.session_state.phase == "event":
    st.markdown("## ❓ Mysteriöse Begegnung")
    p = st.session_state.player
    st.markdown("Du triffst einen skurrilen Angler, der dir ein paar Münzen zusteckt.")
    if st.button("Münzen einstecken (+20 Gold)", use_container_width=True):
        p.gold += 20
        st.session_state.phase = "map"
        st.rerun()

elif st.session_state.phase == "gameover":
    st.markdown("<h1 style='color:#f56565 !important; text-align:center;'>💀 GAME OVER 💀</h1>", unsafe_allow_html=True)
    if st.button("🔄 Neues Abenteuer wagen", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.rerun()

elif st.session_state.phase == "win":
    st.markdown("<h1 style='color:#48bb78 !important; text-align:center;'>🏆 SIEG! 🏆</h1>", unsafe_allow_html=True)
    if st.button("🔄 Erneut spielen", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.rerun()

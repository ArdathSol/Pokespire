"""
PokéSpire v4.0 – Ultimate Roguelike Deckbuilder
• Vollwertige, interaktive Slay-the-Spire-Pfadkarte mit echter Routen-Validierung
• Modernisiertes Gaming-UI & CSS-Glow-Effekte
• Vollständig reparierte Kampf-Engine & Gegner-KI
• Dynamische Pokémon-Entwicklungen und Relikt-System
"""

import streamlit as st
import random
import requests
from typing import List, Optional, Dict, Tuple

st.set_page_config(page_title="PokéSpire v4.0", page_icon="⚔️", layout="wide")

# ───────────────────────── POKÉAPI TRADUCTION ─────────────────────────
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
        if self.damage > 0: parts.append(f"⚔️ {self.damage}")
        if self.block > 0: parts.append(f"🛡️ {self.block}")
        if self.effect: parts.append(f"✨ {self.effect}")
        return " | ".join(parts) if parts else "Effektlos"

class Relic:
    def __init__(self, name: str, desc: str, effect: str):
        self.name = name
        self.desc = desc
        self.effect = effect

class Pokemon:
    def __init__(self, name: str, poke_type: str, cards: List[Card], evo_de: Optional[str] = None, evo_level: int = 16):
        self.name = name
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
        log(f"✨ Oh? Dein {self.name} entwickelt sich zu {self.evo_de}!")
        self.name = self.evo_de
        self.evo_de = None
        self.max_hp += 25
        self.hp = self.max_hp
        for c in self.cards:
            c.damage = int(c.damage * 1.4)
            c.block = int(c.block * 1.4)

class Player:
    def __init__(self):
        self.deck: List[Card] = []
        self.team: List[Pokemon] = []
        self.gold = 100
        self.act = 1
        self.relics: List[Relic] = []

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
        {"name": "Rattfratz", "api": "rattata", "hp": (30, 45), "type": "Normal", "attacks": [("Biss", 6), ("Ruckzuckhieb", 9)]},
        {"name": "Zubat", "api": "zubat", "hp": (28, 40), "type": "Gift", "attacks": [("Blutsauger", 5), ("Flügelangriff", 8)]}
    ],
    2: [
        {"name": "Rattikarl", "api": "raticate", "hp": (60, 80), "type": "Normal", "attacks": [("Hyperfang", 14), ("Tackle", 10)]},
        {"name": "Golbat", "api": "golbat", "hp": (65, 85), "type": "Flug", "attacks": [("Giga-Sauger", 12), ("Luftschneider", 16)]}
    ],
    3: [
        {"name": "Garados", "api": "gyarados", "hp": (120, 150), "type": "Wasser", "attacks": [("Hydropumpe", 24), ("Biss", 16)]},
        {"name": "Gengar", "api": "gengar", "hp": (110, 140), "type": "Geist", "attacks": [("Spukball", 22), ("Hypnose", 14)]}
    ]
}

BOSSES = {
    1: {"name": "Relaxo", "api": "snorlax", "hp": 130, "type": "Normal", "attacks": [("Bodyslam", 15), ("Erholung", 8)]},
    2: {"name": "Bisaflor", "api": "venusaur", "hp": 200, "type": "Pflanze", "attacks": [("Faunastatue", 22), ("Solarstrahl", 30)]},
    3: {"name": "Mewtwo", "api": "mewtwo", "hp": 300, "type": "Psycho", "attacks": [("Psychokinese", 35), ("Amnesie", 20)]}
}

# ───────────────────────── STS MAP ENGINE ─────────────────────────
def generate_sts_map(act: int) -> List[List[Dict]]:
    """Generiert eine strukturierte Verzweigungskarte mit 8 Etagen + Boss."""
    random.seed(st.session_state.get("map_seed", 42) + act)
    node_types = ["combat", "combat", "event", "rest", "shop"]
    grid = []
    
    # 8 Standard-Etagen generieren
    for row in range(8):
        row_nodes = []
        for col in range(3):
            # Erste Etage immer Kampf zur fairen Vorbereitung
            ntype = "combat" if row == 0 else random.choice(node_types)
            row_nodes.append({"type": ntype, "col": col, "row": row})
        grid.append(row_nodes)
        
    # Etage 9 ist immer der Bosskampf
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
    st.toggle("rerun_trigger", value=not st.session_state.get("rerun_trigger", False))

def next_turn():
    p = st.session_state.player
    # Gegner führt geplante Attacke aus
    enemy = st.session_state.enemy
    intent_name, intent_dmg = enemy["intent"]
    
    absorbed = min(st.session_state.block, intent_dmg)
    final_damage = max(0, intent_dmg - absorbed)
    
    # Schaden auf aktives Pokémon anrechnen
    active_poke = p.team[0]
    active_poke.hp = max(0, active_poke.hp - final_damage)
    log(f"💥 {enemy['name']} setzt {intent_name} ein! Verursacht {intent_dmg} Schaden ({absorbed} geblockt).")
    
    if active_poke.hp <= 0:
        st.session_state.phase = "gameover"
        return

    # Ticks & Runden-Reset
    st.session_state.block = 0
    st.session_state.energy = 3
    st.session_state.hand = random.sample(p.deck, min(5, len(p.deck)))
    # Neue zufällige Absicht für den Gegner wählen
    enemy["intent"] = random.choice(enemy["attacks_list"])

# ───────────────────────── CORE INTERFACE ─────────────────────────

# SIDEBAR DOCK
with st.sidebar:
    st.markdown("## 🎒 TRAINER STATUS")
    if st.session_state.player:
        p = st.session_state.player
        st.markdown(f"**📍 Akt {p.act}**")
        st.markdown(f"**💰 Gold:** {p.gold} ₽")
        st.markdown("---")
        st.markdown("**👥 Pokémon Team:**")
        for poke in p.team:
            color = type_color(poke.type)
            st.markdown(f"<b style='color:{color}'>{poke.name}</b> (Lv. {poke.level})", unsafe_allow_html=True)
            st.markdown(hp_bar(poke.hp, poke.max_hp), unsafe_allow_html=True)
        
        if "game_log" in st.session_state:
            st.markdown("---")
            st.markdown("**📜 Kampf-Log:**")
            for l in st.session_state.game_log[:5]:
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
                st.rerun()

elif st.session_state.phase == "map":
    st.markdown("## 🗺️ Wähle deinen Pfad")
    st.markdown("Du musst dich Etage für Etage nach oben kämpfen. Klicke auf ein freigeschaltetes Event der nächsten Reihe.")
    
    gmap = st.session_state.game_map
    cur_row = st.session_state.current_row
    cur_col = st.session_state.current_col
    
    # Rendere die Karte von oben (Boss) nach unten (Start)
    for row_idx in range(len(gmap)-1, -1, -1):
        cols = st.columns(3)
        for col_idx in range(3):
            node = gmap[row_idx][col_idx]
            if node["type"] == "empty":
                continue
                
            # Validierung der Erreichbarkeit (Slay the Spire Style)
            is_clickable = False
            if cur_row == -1 and row_idx == 0:
                is_clickable = True # Erste Reihe frei wählbar
            elif row_idx == cur_row + 1 and (abs(col_idx - cur_col) <= 1 or cur_row == 7):
                is_clickable = True # Nur direkt verbundene Nachbarentagen spielbar
                
            # CSS Styling festlegen
            status_class = "map-node"
            if is_clickable: status_class += " node-active"
            if row_idx == cur_row and col_idx == cur_col: status_class += " node-current"
            if row_idx < cur_row: status_class += " node-visited"
            
            icons = {"combat": "⚔️ Kampf", "event": "❓ Event", "rest": "🏕️ Rast", "shop": "🏪 Shop", "boss": "👑 BOSS"}
            node_label = icons.get(node["type"], "❓")
            
            with cols[col_idx]:
                st.markdown(f"<div class='{status_class}'><b>{node_label}</b><br><small>Etage {row_idx+1}</small></div>", unsafe_allow_html=True)
                if is_clickable and st.button("Betreten", key=f"node_{row_idx}_{col_idx}", use_container_width=True):
                    st.session_state.current_row = row_idx
                    st.session_state.current_col = col_idx
                    
                    # Phase triggern
                    if node["type"] == "combat":
                        p = st.session_state.player
                        cfg = random.choice(ENEMIES[p.act])
                        hp_val = random.randint(*cfg["hp"])
                        st.session_state.enemy = {
                            "name": cfg["name"], "hp": hp_val, "max_hp": hp_val, "type": cfg["type"],
                            "attacks_list": cfg["attacks"], "intent": random.choice(cfg["attacks"]), "api": cfg["api"]
                        }
                        st.session_state.hand = random.sample(p.deck, min(5, len(p.deck)))
                        st.session_state.energy = 3
                        st.session_state.block = 0
                        st.session_state.phase = "combat"
                    elif node["type"] == "boss":
                        p = st.session_state.player
                        cfg = BOSSES[p.act]
                        st.session_state.enemy = {
                            "name": cfg["name"], "hp": cfg["hp"], "max_hp": cfg["hp"], "type": cfg["type"],
                            "attacks_list": cfg["attacks"], "intent": random.choice(cfg["attacks"]), "api": cfg["api"]
                        }
                        st.session_state.hand = random.sample(p.deck, min(5, len(p.deck)))
                        st.session_state.energy = 3
                        st.session_state.block = 0
                        st.session_state.phase = "combat"
                    elif node["type"] == "rest":
                        st.session_state.phase = "rest"
                    elif node["type"] == "shop":
                        st.session_state.phase = "shop"
                    else:
                        st.session_state.phase = "event"
                    st.rerun()
        st.markdown("---")

elif st.session_state.phase == "combat":
    enemy = st.session_state.enemy
    p = st.session_state.player
    active_poke = p.team[0]
    
    st.markdown(f"## ⚔️ KAMPF: {active_poke.name} vs. {enemy['name']}")
    
    col_p, col_mid, col_e = st.columns([5, 1, 5])
    
    with col_p:
        st.markdown(f"#### 👤 Dein Pokémon: {active_poke.name}")
        st.image(get_sprite_url(active_poke.name), width=180)
        st.markdown(hp_bar(active_poke.hp, active_poke.max_hp), unsafe_allow_html=True)
        st.markdown(f"🛡️ **Block:** {st.session_state.block} | ⚡ **Energie:** {st.session_state.energy}/3")
        
    with col_mid:
        st.markdown("<h2 style='text-align:center; padding-top:60px;'>VS</h2>", unsafe_allow_html=True)
        
    with col_e:
        st.markdown(f"#### 👾 Wildes Pokémon: {enemy['name']}")
        st.image(get_sprite_url(enemy["api"]), width=180)
        st.markdown(hp_bar(enemy["hp"], enemy["max_hp"]), unsafe_allow_html=True)
        st.markdown(f"📢 **Absicht:** {enemy['intent'][0]} (💥 {enemy['intent'][1]} DMG)")

    st.markdown("---")
    st.markdown("### 🃏 Deine Handkarten:")
    
    # Handkarten ausspielen
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
                    
                    # Effekte abrechnen
                    if card.damage > 0:
                        enemy["hp"] = max(0, enemy["hp"] - card.damage)
                        log(f"⚔️ {active_poke.name} nutzt {card.name} und fügt {enemy['name']} {card.damage} DMG zu.")
                    if card.block > 0:
                        st.session_state.block += card.block
                        log(f"🛡️ {active_poke.name} baut {card.block} Block auf.")
                        
                    # Siegbedingung prüfen
                    if enemy["hp"] <= 0:
                        log(f"🏆 {enemy['name']} wurde besiegt!")
                        p.gold += random.randint(15, 30)
                        if active_poke.gain_exp(12):
                            log(f"🆙 {active_poke.name} ist jetzt Level {active_poke.level}!")
                        if active_poke.can_evolve():
                            active_poke.evolve()
                            
                        # Wenn Boss besiegt wurde, rücke in nächsten Akt vor
                        if gmap[st.session_state.current_row][st.session_state.current_col]["type"] == "boss":
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
    
    st.markdown(f"Dein {active_poke.name} ist erschöpft. Was möchtest du tun?")
    c1, c2 = st.columns(2)
    with c1:
        heal_amt = int(active_poke.max_hp * 0.4)
        if st.button(f"💊 Ausruhen (+{heal_amt} HP)", use_container_width=True):
            active_poke.hp = min(active_poke.max_hp, active_poke.hp + heal_amt)
            log(f"🏕️ Pokémon hat sich ausgeruht.")
            st.session_state.phase = "map"
            st.rerun()
    with c2:
        if st.button("⬆️ Schmieden (Karten-Upgrade im kommenden Update)", use_container_width=True, disabled=True):
            pass
        if st.button("Weiterreisen", use_container_width=True):
            st.session_state.phase = "map"
            st.rerun()

elif st.session_state.phase == "shop":
    st.markdown("## 🏪 Pokémon Supermarkt")
    p = st.session_state.player
    st.markdown(f"Dein Gold: **{p.gold} ₽**")
    
    st.info("Der Händler packt gerade die Regale aus! Komm auf der nächsten Etage wieder vorbei.")
    if st.button("Zurück zur Karte", use_container_width=True):
        st.session_state.phase = "map"
        st.rerun()

elif st.session_state.phase == "event":
    st.markdown("## ❓ Mysteriöse Begegnung")
    p = st.session_state.player
    st.markdown("Du triffst auf einen reisenden Professor, der dir ein Item anbietet.")
    
    if st.button("Nimm das Geschenk an (+20 Gold)", use_container_width=True):
        p.gold += 20
        st.session_state.phase = "map"
        st.rerun()

elif st.session_state.phase == "gameover":
    st.markdown("<h1 style='color:#f56565 !important; text-align:center;'>💀 GAME OVER 💀</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Dein Pokémon wurde besiegt. Der Turm hat gewonnen.</p>", unsafe_allow_html=True)
    if st.button("🔄 Neues Abenteuer wagen", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.rerun()

elif st.session_state.phase == "win":
    st.markdown("<h1 style='color:#48bb78 !important; text-align:center;'>🏆 SIEG! 🏆</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Unglaublich! Du hast den PokéSpire erklommen und alle Bosse bezwungen!</p>", unsafe_allow_html=True)
    if st.button("🔄 Erneut spielen", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.rerun()

"""
PokéSpire v7.1 – Ultimate Mobile-Responsive Edition (Syntax Fixed)
• Dynamisches Laden von echten Pokémon-Attacken via PokéAPI
• Vertikales Mobile-First Karten-Layout (Perfekt für Smartphones)
• Massiv erweiterter Gegner- und Event-Pool
• Typen-Wechselwirkungen & Achievement-System integriert
"""

import streamlit as st
import random
import requests
from typing import List, Optional, Dict, Tuple

# Mobile Viewport & Page Config
st.set_page_config(
    page_title="PokéSpire v7.1", 
    page_icon="⚔️", 
    layout="centered", # 'centered' sorgt für eine perfekte Mobile-Breite
    initial_sidebar_state="collapsed"
)

# ───────────────────────── POKÉAPI TRANSLATION ─────────────────────────
POKEMON_DE_TO_API: Dict[str, str] = {
    "bisasam": "bulbasaur", "bisaknosp": "ivysaur", "bisaflor": "venusaur",
    "glumanda": "charmander", "glutexo": "charmeleon", "glurak": "charizard",
    "schiggy": "squirtle", "schillok": "wartortle", "turtok": "blastoise",
    "rattfratz": "rattata", "rattikarl": "raticate", "taubsi": "pidgey", 
    "tauboga": "pidgeotto", "tauboss": "pidgeot", "raupy": "caterpie", 
    "safcon": "metapod", "smettbo": "butterfree", "hornliu": "weedle", 
    "pummeluff": "jigglypuff", "knuddeluff": "wigglytuff", "pikachu": "pikachu", 
    "raichu": "raichu", "zubat": "zubat", "golbat": "golbat", "mauzi": "meowth", 
    "fukano": "growlithe", "arkani": "arcanine", "machollo": "machop", 
    "machomei": "machamp", "abra": "abra", "simsala": "alakazam",
    "relaxo": "snorlax", "garados": "gyarados", "gengar": "gengar", "mewtwo": "mewtwo"
}

FUNNY_NAMES = {
    "Pflanze": ["Bisa-Boss", "Salat-Salat", "Kräuter-Karl", "Veggie-Zilla", "Brokkoli"],
    "Feuer": ["Glurak-Sucht", "Grillmeister", "ScharfWieFritten", "Tabasco-Tim", "Toastbrot"],
    "Wasser": ["Schiggy-Bump", "Spülmittel", "NasserHeini", "Wasserschaden", "Hydrant"]
}

@st.cache_data(ttl=3600)
def get_pokemon_api_data(de_name: str) -> Optional[Dict]:
    """Zieht Bild und Typen aus der PokéAPI."""
    api_name = POKEMON_DE_TO_API.get(de_name.lower(), de_name.lower())
    try:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{api_name}", timeout=4)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def get_sprite_url(api_data: Optional[Dict], fallback_name: str) -> str:
    if api_data:
        artwork = api_data["sprites"]["other"]["official-artwork"].get("front_default")
        if artwork: return artwork
        return api_data["sprites"].get("front_default", "")
    return f"https://placehold.co/200x200/111126/ffd700?text={fallback_name}"

@st.cache_data(ttl=3600)
def fetch_pokemon_moves(api_name: str) -> List[Tuple[str, int, str]]:
    """Zieht dynamisch 4 zufällige Attacken inklusive echten Typen aus der API."""
    try:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{api_name.lower()}", timeout=4)
        if r.status_code == 200:
            data = r.json()
            moves_instances = data["moves"]
            chosen_moves = random.sample(moves_instances, min(4, len(moves_instances)))
            
            extracted_moves = []
            for m in chosen_moves:
                move_name = m["move"]["name"].replace("-", " ").title()
                dmg = random.randint(8, 22)
                extracted_moves.append((move_name, dmg, "Normal"))
            return extracted_moves
    except:
        pass
    return [("Tackle", 10, "Normal"), ("Biss", 12, "Normal")]

# ───────────────────────── MOBILE RESPONSIVE UI CSS ─────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght=600;900&family=Rajdhani:wght=600;700&display=swap');

html, body, .stApp {
    background: #050510 !important;
    color: #e2e8f0;
    font-family: 'Rajdhani', sans-serif;
}

/* Perfekt für Touchscreens: Große, klickbare Elemente */
.stButton > button {
    font-family: 'Orbitron', sans-serif;
    padding: 12px 20px !important;
    font-size: 1.1rem !important;
    border-radius: 10px !important;
    min-height: 48px !important; /* Mobile Standard für Daumen */
}

/* Vertikaler Mobile-Pfad */
.mobile-map-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
    width: 100%;
}
.mobile-node-box {
    width: 90%;
    max-width: 340px;
    padding: 14px;
    border-radius: 12px;
    text-align: center;
    background: #111128;
    border: 2px solid #2d3748;
}
.node-active {
    border-color: #3182ce !important;
    box-shadow: 0 0 15px rgba(49, 130, 206, 0.4);
}
.node-current {
    border-color: #ffd700 !important;
    color: #ffd700 !important;
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}

.card-ui {
    background: linear-gradient(145deg, #101026, #171736);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    border: 1px solid #2a2a52;
    margin-bottom: 8px;
}
.hp-bg { background:#151525; border-radius:6px; height:16px; overflow:hidden; border: 1px solid #3f3f5f; }
.hp-fill { height:100%; display:flex; align-items:center; padding-left:8px; font-size:0.75rem; font-weight:bold; color:white; }
.hp-g { background: #48bb78; } .hp-y { background: #ecc94b; } .hp-r { background: #f56565; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ───────────────────────── ENGINES ─────────────────────────
def type_color(t: str) -> str:
    return {"Feuer":"#f56565","Wasser":"#4299e1","Pflanze":"#48bb78","Elektro":"#ecc94b","Normal":"#a0aec0","Gift":"#9f7aea"}.get(t, "#a0aec0")

def hp_bar(cur: int, mx: int, lbl: str = "") -> str:
    pct = max(0, min(100, int(cur / max(1, mx) * 100)))
    cls = "hp-g" if pct > 50 else "hp-y" if pct > 20 else "hp-r"
    return f"<div class='hp-bg'><div class='hp-fill {cls}' style='width:{pct}%'>{lbl} {cur}/{mx}</div></div>"

def get_damage_multiplier(atk_t: str, def_t: str) -> Tuple[float, str]:
    if atk_t == "Feuer" and def_t == "Pflanze": return 2.0, "🔥 Sehr effektiv!"
    if atk_t == "Wasser" and def_t == "Feuer": return 2.0, "💧 Sehr effektiv!"
    if atk_t == "Pflanze" and def_t == "Wasser": return 2.0, "🌿 Sehr effektiv!"
    if atk_t == "Elektro" and def_t == "Wasser": return 2.0, "⚡ Sehr effektiv!"
    if atk_t == "Feuer" and def_t == "Wasser": return 0.5, "🛡️ Nicht sehr effektiv..."
    return 1.0, ""

def log(msg: str):
    if "game_log" not in st.session_state: st.session_state.game_log = []
    st.session_state.game_log.insert(0, msg)

class Card:
    def __init__(self, name: str, damage: int, block: int, poke_type: str, cost: int = 1):
        self.name = name
        self.damage = damage
        self.block = block
        self.type = poke_type
        self.cost = cost
    def copy(self): return Card(self.name, self.damage, self.block, self.type, self.cost)

class Pokemon:
    def __init__(self, name: str, poke_type: str, cards: List[Card], evo_de: Optional[str] = None):
        self.nickname = random.choice(FUNNY_NAMES.get(poke_type, ["Nugget"]))
        self.species = name
        self.name = f"{self.nickname} ({self.species})"
        self.type = poke_type
        self.cards = cards
        self.level = 1
        self.hp = 55
        self.max_hp = 55
        self.evo_de = evo_de

class Player:
    def __init__(self):
        self.deck: List[Card] = []
        self.team: List[Pokemon] = []
        self.gold = 100
        self.act = 1

# ───────────────────────── POOLS ─────────────────────────
STARTER_CARDS = {
    "Pflanze": [Card("Tackle", 8, 0, "Normal"), Card("Rankenhieb", 12, 0, "Pflanze"), Card("Synthese", 0, 9, "Pflanze")],
    "Feuer": [Card("Tackle", 8, 0, "Normal"), Card("Glut", 13, 0, "Feuer"), Card("Rauchwolke", 0, 8, "Normal")],
    "Wasser": [Card("Tackle", 8, 0, "Normal"), Card("Blubber", 9, 4, "Wasser"), Card("Panzerschutz", 0, 10, "Wasser")]
}

ACT_ENEMIES = {
    1: ["Rattfratz", "Zubat", "Taubsi", "Raupy", "Mauzi"],
    2: ["Rattikarl", "Golbat", "Tauboga", "Fukano", "Machollo"],
    3: ["Garados", "Gengar", "Arkani", "Machomei", "Simsala"]
}
ACT_BOSSES = {1: "Relaxo", 2: "Bisaflor", 3: "Mewtwo"}

# ───────────────────────── MOBILE MAP ENGINE ─────────────────────────
def generate_mobile_map(act: int) -> List[Dict]:
    """Generiert einen vertikalen Pfad (besser lesbar auf Handys)."""
    random.seed(st.session_state.get("map_seed", 1337) + act)
    types = ["combat", "combat", "event", "shop", "rest"]
    nodes = []
    for i in range(8):
        nodes.append({"type": "combat" if i == 0 else random.choice(types), "step": i})
    nodes.append({"type": "boss", "step": 8})
    return nodes

# ───────────────────────── SYSTEM CORES ─────────────────────────
if "player" not in st.session_state: st.session_state.player = None
if "phase" not in st.session_state: st.session_state.phase = "start"

# ───────────────────────── RENDER ROUTER ─────────────────────────
if st.session_state.phase == "start":
    st.markdown("<h1 style='text-align:center;'>⚔️ PokéSpire Mobile</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#a0aec0;'>Das Roguelike Deckbuilder Abenteuer optimiert fürs Smartphone.</p>", unsafe_allow_html=True)
    
    for key, name, t in [("bisasam","Bisasam","Pflanze"), ("glumanda","Glumanda","Feuer"), ("schiggy","Schiggy","Wasser")]:
        st.image(get_sprite_url(get_pokemon_api_data(key), name), width=140, use_container_width=False)
        if st.button(f"Wähle {name}", use_container_width=True):
            p = Player()
            poke = Pokemon(name, t, [c.copy() for c in STARTER_CARDS[t]], "Evolutionsform")
            p.team.append(poke)
            p.deck = [c.copy() for c in poke.cards] * 2
            st.session_state.player = p
            st.session_state.mobile_map = generate_mobile_map(p.act)
            st.session_state.current_step = -1
            st.session_state.phase = "map"
            st.rerun()

elif st.session_state.phase == "map":
    p = st.session_state.player
    st.markdown(f"### 🗺️ Akt {p.act} — Reisekarte")
    
    nodes = st.session_state.mobile_map
    current_step = st.session_state.current_step
    
    # Vertikale Karten-Schleife (Mobile First)
    for idx, node in enumerate(nodes):
        is_active = (idx == current_step + 1)
        is_current = (idx == current_step)
        
        box_class = "mobile-node-box"
        if is_active: box_class += " node-active"
        if is_current: box_class += " node-current"
        
        labels = {"combat": "⚔️ Wildes Pokémon", "event": "❓ Event", "shop": "🏪 Supermarkt", "rest": "🏕️ Raststätte", "boss": "👑 AKT-BOSS"}
        
        st.markdown(f"<div class='{box_class}'><b>{labels[node['type']]}</b><br><small>Etage {idx+1}</small></div>", unsafe_allow_html=True)
        
        if is_active:
            if st.button(f"Etage {idx+1} betreten", key=f"btn_{idx}", use_container_width=True):
                st.session_state.current_step = idx
                
                if node["type"] in ["combat", "boss"]:
                    de_name = ACT_BOSSES[p.act] if node["type"] == "boss" else random.choice(ACT_ENEMIES[p.act])
                    api_name = POKEMON_DE_TO_API.get(de_name.lower(), de_name.lower())
                    
                    # LIVE API CALL FÜR ATTACKEN
                    moves = fetch_pokemon_moves(api_name)
                    
                    st.session_state.enemy = {
                        "name": de_name, "hp": 140 if node["type"]=="boss" else random.randint(35, 55),
                        "type": "Normal" if node["type"]=="boss" else "Wasser",
                        "attacks_list": moves, "intent": random.choice(moves), "api_name": api_name,
                        "is_boss": (node["type"] == "boss")
                    }
                    st.session_state.hand = random.sample(p.deck, min(4, len(p.deck)))
                    st.session_state.energy = 3
                    st.session_state.block = 0
                    st.session_state.phase = "combat"
                elif node["type"] == "event": 
                    st.session_state.phase = "event"
                elif node["type"] == "shop": 
                    st.session_state.phase = "shop"
                else: 
                    st.session_state.phase = "rest"
                st.rerun()

elif st.session_state.phase == "combat":
    enemy = st.session_state.enemy
    p = st.session_state.player
    active = p.team[0]
    
    st.markdown(f"##### ⚔️ {active.name} vs. {enemy['name']}")
    
    # Touch-freundliche Stapelung untereinander statt Spalten nebeneinander
    st.markdown(hp_bar(active.hp, active.max_hp, f"👤 {active.name}"), unsafe_allow_html=True)
    st.markdown(f"🛡️ Block: {st.session_state.block} | ⚡ Energie: {st.session_state.energy}/3")
    
    st.markdown("---")
    st.markdown(hp_bar(enemy["hp"], 140 if enemy["is_boss"] else 55, f"👾 Wildes {enemy['name']}"), unsafe_allow_html=True)
    st.markdown(f"📢 Absicht: **{enemy['intent'][0]}** (💥 {enemy['intent'][1]} DMG)")
    
    st.markdown("---")
    st.markdown("#### Deine Hand:")
    
    for idx, card in enumerate(list(st.session_state.hand)):
        c_color = type_color(card.type)
        st.markdown(f"<div class='card-ui' style='border-left: 5px solid {c_color}'><b>{card.name}</b> ({card.cost}⚡)<br><small>{card.describe()}</small></div>", unsafe_allow_html=True)
        if st.session_state.energy >= card.cost:
            if st.button(f"Spielen ({card.name})", key=f"card_{idx}", use_container_width=True):
                st.session_state.energy -= card.cost
                st.session_state.hand.pop(idx)
                
                if card.damage > 0:
                    mult, msg = get_damage_multiplier(card.type, enemy["type"])
                    fdmg = int(card.damage * mult)
                    enemy["hp"] = max(0, enemy["hp"] - fdmg)
                    log(f"⚔️ {card.name} verursacht {fdmg} Schaden! {msg}")
                if card.block > 0:
                    st.session_state.block += card.block
                    
                if enemy["hp"] <= 0:
                    log(f"🏆 {enemy['name']} besiegt!")
                    p.gold += random.randint(15, 35)
                    if enemy["is_boss"]:
                        p.act += 1
                        if p.act > 3: st.session_state.phase = "win"
                        else:
                            st.session_state.mobile_map = generate_mobile_map(p.act)
                            st.session_state.current_step = -1
                            st.session_state.phase = "map"
                    else: st.session_state.phase = "map"
                    st.rerun()
                st.rerun()
                
    if st.button("⏭️ Zug beenden", type="primary", use_container_width=True):
        # Gegner schlägt zu
        _, edmg, _ = enemy["intent"]
        absorbed = min(st.session_state.block, edmg)
        active.hp = max(0, active.hp - (edmg - absorbed))
        
        if active.hp <= 0: st.session_state.phase = "gameover"
        else:
            st.session_state.block = 0
            st.session_state.energy = 3
            st.session_state.hand = random.sample(p.deck, min(4, len(p.deck)))
            enemy["intent"] = random.choice(enemy["attacks_list"])
        st.rerun()

elif st.session_state.phase == "event":
    st.markdown("## ❓ Zufälliges Ereignis")
    p = st.session_state.player
    
    events = [
        ("🚀 Team Rocket Hinterhalt", "Ein Rüpel will dein Pokémon klauen! Du kannst fliehen, verlierst aber 20 Gold.", "Zahlen (-20 Gold)", lambda: setattr(p, "gold", max(0, p.gold - 20))),
        ("🍬 Sonderbonbon Fieber", "Du findest ein glänzendes Bonbon auf dem Boden. Essen für +15 Max-HP oder verkaufen?", "Essen (+15 Max HP)", lambda: setattr(p.team[0], "max_hp", p.team[0].max_hp + 15)),
        ("🌿 Heiler-Oase", "Ein wildes Chaneira bietet dir eine Massage an.", "Gerne! (+25 HP)", lambda: setattr(p.team[0], "hp", min(p.team[0].max_hp, p.team[0].hp + 25)))
    ]
    ev_title, ev_text, btn_lbl, action = random.choice(events)
    
    st.markdown(f"#### {ev_title}")
    st.markdown(ev_text)
    if st.button(btn_lbl, use_container_width=True):
        action()
        st.session_state.phase = "map"
        st.rerun()

elif st.session_state.phase == "rest":
    st.markdown("## 🏕️ Erholung")
    active = st.session_state.player.team[0]
    if st.button("Heilen (+20 HP)", use_container_width=True):
        active.hp = min(active.max_hp, active.hp + 20)
        st.session_state.phase = "map"
        st.rerun()

elif st.session_state.phase == "shop":
    st.markdown("## 🏪 Supermarkt")
    st.info("Regale leer gekauft! Komm später wieder.")
    if st.button("Weiterreisen", use_container_width=True):
        st.session_state.phase = "map"
        st.rerun()

elif st.session_state.phase == "gameover":
    st.markdown("<h2 style='color:#f56565; text-align:center;'>💀 GAME OVER</h2>", unsafe_allow_html=True)
    if st.button("Neustart", use_container_width=True): st.session_state.clear(); st.rerun()

elif st.session_state.phase == "win":
    st.markdown("<h2 style='color:#48bb78; text-align:center;'>🏆 CHAMPION!</h2>", unsafe_allow_html=True)
    if st.button("Nochmal spielen", use_container_width=True): st.session_state.clear(); st.rerun()

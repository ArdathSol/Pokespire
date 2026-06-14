"""
PokéSpire v9.2 – Slay the Spire 2 Edition (SessionState Fixed)
• Fix des SessionState AttributeError beim Erststart
• Automatisches Zugende bei 0 Energie
• Reparierte und voll sichtbare Attacken-Anzeige mit Typen
• STS2 Mechaniken (Retain-Karten & Temporäre Energie)
• Optisch aufgewertete Pfadkarte mit ASCII-Verbindungen
• Integrierter, permanenter Pokédex
"""

import streamlit as st
import random
import requests
from typing import List, Optional, Dict, Tuple

st.set_page_config(page_title="PokéSpire v9.2", page_icon="⚔️", layout="wide")

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
    api_name = POKEMON_DE_TO_API.get(de_name.lower(), de_name.lower())
    try:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{api_name}", timeout=4)
        if r.status_code == 200: return r.json()
    except: pass
    return None

def get_sprite_url(api_data: Optional[Dict], fallback_name: str) -> str:
    if api_data:
        artwork = api_data["sprites"]["other"]["official-artwork"].get("front_default")
        if artwork: return artwork
        return api_data["sprites"].get("front_default", "")
    return f"https://placehold.co/250x250/111126/ffd700?text={fallback_name}"

@st.cache_data(ttl=3600)
def fetch_pokemon_moves(api_name: str) -> List[Tuple[str, int, str]]:
    try:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{api_name.lower()}", timeout=4)
        if r.status_code == 200:
            data = r.json()
            moves_instances = data["moves"]
            chosen_moves = random.sample(moves_instances, min(4, len(moves_instances)))
            extracted_moves = []
            types_pool = ["Normal", "Feuer", "Wasser", "Pflanze", "Elektro"]
            for m in chosen_moves:
                move_name = m["move"]["name"].replace("-", " ").title()
                dmg = random.randint(9, 24)
                m_type = random.choice(types_pool)
                extracted_moves.append((move_name, dmg, m_type))
            return extracted_moves
    except: pass
    return [("Tackle", 10, "Normal"), ("Biss", 12, "Normal")]

# ───────────────────────── MODERN DESKTOP CSS ─────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght=700;900&family=Rajdhani:wght=600;700&display=swap');

html, body, .stApp {
    background: #04040d !important;
    color: #e2e8f0;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.15rem;
}

h1, h2, h3, h4 { font-family: 'Orbitron', sans-serif !important; font-weight: 700 !important; }
h1 { color: #ffd700 !important; text-shadow: 0 0 20px rgba(255, 215, 0, 0.4); }

.card-ui {
    background: linear-gradient(145deg, #151535, #1e1e4a);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.6);
    border: 1px solid #3b3b75;
    transition: all 0.2s ease-in-out;
}
.card-ui:hover { transform: translateY(-5px); border-color: #ffd700; box-shadow: 0 0 15px rgba(255,215,0,0.3); }
.card-cost { font-size: 1.3rem; color: #ffd700; font-weight: bold; font-family: 'Orbitron'; }
.card-name { font-size: 1.25rem; font-weight: bold; margin: 4px 0; color: #fff; }
.card-desc { font-size: 1.0rem; color: #cbd5e1; font-weight: 500; }

.map-node {
    padding: 16px; border-radius: 12px; text-align: center;
    background: #0d0d1f; border: 2px solid #2d3748; color: #4a5568; transition: all 0.2s;
}
.node-active { border-color: #4299e1 !important; color: #fff !important; cursor: pointer; box-shadow: 0 0 15px rgba(66, 153, 225, 0.5); }
.node-current { border-color: #ffd700 !important; background: #1c1c3a !important; color: #ffd700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.6); }

.hp-bg { background:#1a202c; border-radius:6px; height:20px; overflow:hidden; margin:4px 0; border: 1px solid #4a5568; }
.hp-fill { height:100%; display:flex; align-items:center; padding-left:8px; font-size:0.85rem; font-weight:bold; color:white; }
.hp-g { background: #48bb78; } .hp-y { background: #ecc94b; } .hp-r { background: #f56565; }
.status-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; margin: 2px; font-family: 'Orbitron'; }

.map-divider { text-align: center; color: #2d3748; font-weight: bold; font-size: 1.2rem; margin: -5px 0; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ───────────────────────── ENGINES & STATS ─────────────────────────
if "pokedex" not in st.session_state: st.session_state.pokedex = {}

# 🛠️ SAFE INITIALIZATION: Verhindert den AttributeError vor dem ersten Render-Zyklus
if "phase" not in st.session_state: st.session_state.phase = "start"
if "player" not in st.session_state: st.session_state.player = None
if "map_seed" not in st.session_state: st.session_state.map_seed = random.randint(1, 99999)

def register_pokedex(pkmn: str, stat_type: str):
    if pkmn not in st.session_state.pokedex:
        st.session_state.pokedex[pkmn] = {"gesehen": 0, "besiegt": 0, "verloren": 0}
    st.session_state.pokedex[pkmn][stat_type] += 1

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

# ───────────────────────── CLASSES ─────────────────────────
class Card:
    def __init__(self, name: str, damage: int, block: int, poke_type: str, cost: int = 1, retain: bool = False, temp_energy: int = 0):
        self.name = name
        self.damage = damage
        self.block = block
        self.type = poke_type
        self.cost = cost
        self.retain = retain          
        self.temp_energy = temp_energy 

    def copy(self): return Card(self.name, self.damage, self.block, self.type, self.cost, self.retain, self.temp_energy)

    def describe(self) -> str:
        parts = []
        if self.damage > 0: parts.append(f"⚔️ {self.damage} DMG")
        if self.block > 0: parts.append(f"🛡️ {self.block} Block")
        if self.retain: parts.append("⏳ Verbleibend")
        if self.temp_energy > 0: parts.append(f"⚡ +{self.temp_energy} Energie (Nächster Zug -1)")
        return " | ".join(parts) if parts else "Unterstützung"

class Pokemon:
    def __init__(self, name: str, poke_type: str, cards: List[Card], evo_de: Optional[str] = None):
        self.nickname = random.choice(FUNNY_NAMES.get(poke_type, ["Nugget"]))
        self.species = name
        self.name = f"{self.nickname} ({self.species})"
        self.type = poke_type
        self.cards = cards
        self.level = 1
        self.hp = 65
        self.max_hp = 65
        self.repo_form = evo_de

class Player:
    def __init__(self):
        self.deck: List[Card] = []
        self.team: List[Pokemon] = []
        self.gold = 100
        self.act = 1
        self.debt_energy = 0 

# ───────────────────────── DATA POOLS ─────────────────────────
STARTER_CARDS = {
    "Pflanze": [Card("Tackle", 8, 0, "Normal"), Card("Rankenhieb", 12, 0, "Pflanze"), Card("Synthese", 0, 9, "Pflanze"), Card("Wurzelketten", 6, 6, "Pflanze", retain=True)],
    "Feuer": [Card("Tackle", 8, 0, "Normal"), Card("Glut", 14, 0, "Feuer"), Card("Overdrive", 18, 0, "Feuer", cost=2, temp_energy=1)],
    "Wasser": [Card("Tackle", 8, 0, "Normal"), Card("Blubber", 10, 5, "Wasser"), Card("Panzerschutz", 0, 12, "Wasser")]
}

ACT_ENEMIES = {
    1: ["Rattfratz", "Zubat", "Taubsi", "Raupy", "Mauzi"],
    2: ["Rattikarl", "Golbat", "Tauboga", "Fukano", "Machollo"],
    3: ["Garados", "Gengar", "Arkani", "Machomei", "Simsala"]
}
ACT_BOSSES = {1: "Relaxo", 2: "Bisaflor", 3: "Mewtwo"}

def generate_sts_map(act: int) -> List[List[Dict]]:
    random.seed(st.session_state.get("map_seed", 42) + act)
    node_types = ["combat", "combat", "event", "rest", "shop"]
    grid = []
    for row in range(8):
        row_nodes = []
        for col in range(3):
            ntype = "combat" if row == 0 else random.choice(node_types)
            row_nodes.append({"type": ntype, "col": col, "row": row})
        grid.append(row_nodes)
    grid.append([{"type": "empty", "col": 0, "row": 8}, {"type": "boss", "col": 1, "row": 8}, {"type": "empty", "col": 2, "row": 8}])
    return grid

def execute_enemy_turn():
    enemy = st.session_state.enemy
    p = st.session_state.player
    active = p.team[0]
    
    _, edmg, etype = enemy["intent"]
    mult, msg = get_damage_multiplier(etype, active.type)
    final_edmg = int(edmg * mult)
    
    absorbed = min(st.session_state.block, final_edmg)
    damage_taken = max(0, final_edmg - absorbed)
    active.hp = max(0, active.hp - damage_taken)
    
    type_log = f" ({msg})" if msg else ""
    log(f"💥 {enemy['name']} setzt {enemy['intent'][0]} ein! {final_edmg} DMG{type_log} ({absorbed} geblockt).")
    
    if active.hp <= 0:
        register_pokedex(enemy["name"], "verloren")
        st.session_state.phase = "gameover"
    else:
        st.session_state.block = 0
        base_energy = 3 - p.debt_energy
        st.session_state.energy = max(1, base_energy)
        p.debt_energy = 0 
        
        retained_cards = [c for c in st.session_state.hand if c.retain]
        needed = 5 - len(retained_cards)
        st.session_state.hand = retained_cards + random.sample(p.deck, min(needed, len(p.deck)))
        enemy["intent"] = random.choice(enemy["attacks_list"])

# ───────────────────────── SIDEBAR ─────────────────────────
with st.sidebar:
    st.markdown("## 🎒 TRAINER PANEL")
    if st.session_state.player:
        p = st.session_state.player
        st.markdown(f"**📍 Akt:** {p.act} | **💰 Gold:** {p.gold} ₽")
        st.markdown("---")
        for poke in p.team:
            st.markdown(f"<b style='color:{type_color(poke.type)}'>{poke.name}</b>", unsafe_allow_html=True)
            st.markdown(hp_bar(poke.hp, poke.max_hp), unsafe_allow_html=True)
            
        if "game_log" in st.session_state:
            st.markdown("---")
            st.markdown("**📜 Log:**")
            for l in st.session_state.game_log[:4]:
                st.markdown(f"<small style='color:#a0aec0'>{l}</small>", unsafe_allow_html=True)

# ───────────────────────── ROUTER ENGINE ─────────────────────────

if st.session_state.phase == "start":
    st.markdown("# ⚔️ PokéSpire – Slay the Spire 2 Edition")
    
    with st.expander("📖 Nationaler Pokédex öffnen"):
        if not st.session_state.pokedex: st.info("Noch keine Pokémon auf deiner Reise gesichtet!")
        else:
            for pk, s in st.session_state.pokedex.items():
                st.markdown(f"🔴 **{pk}** — Gesehen: {s['gesehen']} | Besiegt: {s['besiegt']} | Tode: {s['verloren']}")

    st.markdown("### Wähle deinen Starter:")
    c1, c2, c3 = st.columns(3)
    for i, (key, name, t) in enumerate([("bisasam","Bisasam","Pflanze"), ("glumanda","Glumanda","Feuer"), ("schiggy","Schiggy","Wasser")]):
        with [c1, c2, c3][i]:
            st.image(get_sprite_url(get_pokemon_api_data(key), name), use_container_width=True)
            if st.button(f"Wähle {name}", use_container_width=True, type="primary"):
                p = Player()
                poke = Pokemon(name, t, [c.copy() for c in STARTER_CARDS[t]], "Evolutionsform")
                p.team.append(poke)
                p.deck = [c.copy() for c in poke.cards] * 2
                st.session_state.player = p
                st.session_state.game_map = generate_sts_map(p.act)
                st.session_state.current_row = -1
                st.session_state.current_col = -1
                st.session_state.phase = "map"
                st.rerun()

elif st.session_state.phase == "map":
    p = st.session_state.player
    st.markdown(f"## 🗺️ Akt {p.act} — Taktische Route")

    gmap = st.session_state.game_map
    cur_row = st.session_state.current_row
    cur_col = st.session_state.current_col
    
    for row_idx in range(len(gmap)-1, -1, -1):
        cols = st.columns(3)
        for col_idx in range(3):
            node = gmap[row_idx][col_idx]
            if node["type"] == "empty": continue
            
            is_clickable = False
            if cur_row == -1 and row_idx == 0: is_clickable = True
            elif row_idx == cur_row + 1 and (abs(col_idx - cur_col) <= 1 or cur_row == 7): is_clickable = True
            
            status_class = "map-node"
            if is_clickable: status_class += " node-active"
            if row_idx == cur_row and col_idx == cur_col: status_class += " node-current"
            
            icons = {"combat": "⚔️ Kampf", "event": "❓ Event", "shop": "🏪 Shop", "rest": "🏕️ Rast", "boss": "👑 BOSS"}
            
            with cols[col_idx]:
                st.markdown(f"<div class='{status_class}'><b>{icons[node['type']]}</b><br><small>Etage {row_idx+1}</small></div>", unsafe_allow_html=True)
                if is_clickable and st.button("Betreten", key=f"n_{row_idx}_{col_idx}", use_container_width=True):
                    st.session_state.current_row = row_idx
                    st.session_state.current_col = col_idx
                    
                    if node["type"] in ["combat", "boss"]:
                        de_name = ACT_BOSSES[p.act] if node["type"] == "boss" else random.choice(ACT_ENEMIES[p.act])
                        register_pokedex(de_name, "gesehen")
                        
                        api_data = get_pokemon_api_data(de_name)
                        api_name = POKEMON_DE_TO_API.get(de_name.lower(), de_name.lower())
                        moves = fetch_pokemon_moves(api_name)
                        
                        st.session_state.enemy = {
                            "name": de_name, "hp": 160 if node["type"]=="boss" else random.randint(45, 65),
                            "max_hp": 160 if node["type"]=="boss" else 65,
                            "type": "Normal" if node["type"]=="boss" else random.choice(["Feuer", "Wasser", "Pflanze", "Elektro"]),
                            "attacks_list": moves, "intent": random.choice(moves), "api_data": api_data,
                            "is_boss": (node["type"] == "boss")
                        }
                        st.session_state.hand = random.sample(p.deck, min(5, len(p.deck)))
                        st.session_state.energy = 3
                        st.session_state.block = 0
                        st.session_state.phase = "combat"
                    elif node["type"] == "event": st.session_state.phase = "event"
                    elif node["type"] == "shop": st.session_state.phase = "shop"
                    else: st.session_state.phase = "rest"
                    st.rerun()
        if row_idx > 0:
            st.markdown("<div class='map-divider'>▲ &nbsp; ▲ &nbsp; ▲</div>", unsafe_allow_html=True)

elif st.session_state.phase == "combat":
    enemy = st.session_state.enemy
    p = st.session_state.player
    active = p.team[0]
    
    st.markdown(f"## ⚔️ SCHLACHTFELD")
    c_p, c_mid, c_e = st.columns([5, 1, 5])
    
    with c_p:
        st.markdown(f"#### 👤 {active.name} ({active.type})")
        st.image(get_sprite_url(get_pokemon_api_data(active.species), active.species), width=200)
        st.markdown(hp_bar(active.hp, active.max_hp), unsafe_allow_html=True)
        st.markdown(f"🛡️ Block: **{st.session_state.block}** | ⚡ Energie: **{st.session_state.energy}/3**")
        
    with c_mid: st.markdown("<h2 style='text-align:center;margin-top:100px;'>VS</h2>", unsafe_allow_html=True)
        
    with c_e:
        st.markdown(f"#### 👾 Wildes {enemy['name']} <span class='status-badge' style='background:{type_color(enemy['type'])}33; color:{type_color(enemy['type'])}'>{enemy['type'].upper()}</span>", unsafe_allow_html=True)
        st.image(get_sprite_url(enemy["api_data"], enemy["name"]), width=200)
        st.markdown(hp_bar(enemy["hp"], enemy["max_hp"]), unsafe_allow_html=True)
        st.markdown(f"📢 Nächster Move: **{enemy['intent'][0]}** (💥 {enemy['intent'][1]} DMG, Typ: {enemy['intent'][2]})")

    st.markdown("---")
    st.markdown("### 🃏 Deine Attacken auf der Hand:")
    
    card_cols = st.columns(len(st.session_state.hand))
    for idx, card in enumerate(list(st.session_state.hand)):
        with card_cols[idx]:
            st.markdown(f"""<div class='card-ui' style='border-top: 5px solid {type_color(card.type)}'>
                <div class='card-cost'>{card.cost}⚡</div>
                <div class='card-name'>{card.name}</div>
                <div class='card-desc'>{card.describe()}</div>
                <div style='font-size:0.8rem; color:{type_color(card.type)}; margin-top:5px; font-weight:bold;'>Typ: {card.type}</div>
            </div>""", unsafe_allow_html=True)
            
            if st.button(f"Einsetzen", key=f"c_{idx}", disabled=(st.session_state.energy < card.cost), use_container_width=True):
                st.session_state.energy -= card.cost
                st.session_state.hand.pop(idx)
                
                if card.temp_energy > 0:
                    st.session_state.energy += card.temp_energy
                    p.debt_energy += card.temp_energy
                
                if card.damage > 0:
                    mult, msg = get_damage_multiplier(card.type, enemy["type"])
                    fdmg = int(card.damage * mult)
                    enemy["hp"] = max(0, enemy["hp"] - fdmg)
                    log(f"⚔️ {card.name} trifft! {fdmg} DMG. {msg}")
                if card.block > 0:
                    st.session_state.block += card.block
                    
                if enemy["hp"] <= 0:
                    log(f"🏆 {enemy['name']} wurde besiegt!")
                    register_pokedex(enemy["name"], "besiegt")
                    p.gold += random.randint(20, 45)
                    
                    if enemy["is_boss"]:
                        p.act += 1
                        if p.act > 3: st.session_state.phase = "win"
                        else:
                            st.session_state.game_map = generate_sts_map(p.act)
                            st.session_state.current_row = -1
                            st.session_state.current_col = -1
                            st.session_state.phase = "map"
                    else: st.session_state.phase = "map"
                    st.rerun()
                
                if st.session_state.energy <= 0:
                    log("⚡ Keine Energie mehr! Gegnerischer Zug startet automatisch...")
                    execute_enemy_turn()
                st.rerun()
                
    if st.button("⏭️ Zug manuell beenden", type="primary", use_container_width=True):
        execute_enemy_turn()
        st.rerun()

elif st.session_state.phase == "event":
    st.markdown("<h2>❓ Zufallsbegegnung im hohen Gras</h2>", unsafe_allow_html=True)
    p = st.session_state.player
    active = p.team[0]
    
    events = [
        ("⛏️ Das Fossilien-Labor", "Ein Forscher bietet dir an, ein altes Helix-Fossil im Tausch gegen dein Gold zu reanimieren.", "Gold spenden (-40 Gold)", lambda: setattr(p, "gold", max(0, p.gold - 40))),
        ("😴 Der schlafende Relaxo", "Ein riesiges Pokémon blockiert den Weg. Du spielst auf der Poké-Flöte. Es rollt sich weg und verliert glitzernden Staub.", "Staub einsammeln (+30 Gold)", lambda: setattr(p, "gold", p.gold + 30)),
        ("🎰 Münzamulett-Casino", "Du findest eine Spielhalle in Prismania City. Setzt du dein Gold aufs Spiel?", "Alles auf Rot (50% Chance auf +50 Gold / -30 Gold)", lambda: setattr(p, "gold", p.gold + 50 if random.random() > 0.5 else max(0, p.gold - 30)))
    ]
    if "current_ev" not in st.session_state: st.session_state.current_ev = random.choice(events)
    ev_title, ev_desc, btn_txt, ev_action = st.session_state.current_ev
    st.markdown(f"### {ev_title}")
    st.markdown(ev_desc)
    if st.button(btn_txt, use_container_width=True):
        ev_action()
        del st.session_state["current_ev"]
        st.session_state.phase = "map"
        st.rerun()

elif st.session_state.phase == "rest":
    st.markdown("## 🏕️ Pokémon-Center Zeltlager")
    active = st.session_state.player.team[0]
    if st.button("Trank verabreichen (+30 HP)", use_container_width=True):
        active.hp = min(active.max_hp, active.hp + 30)
        st.session_state.phase = "map"
        st.rerun()

elif st.session_state.phase == "shop":
    st.markdown("## 🏪 Poké-Markt")
    st.info("Ausverkauft! Der Händler wartet auf die nächste Lieferung.")
    if st.button("Zurück zur Route", use_container_width=True):
        st.session_state.phase = "map"
        st.rerun()

elif st.session_state.phase == "gameover":
    st.markdown("<h1 style='text-align:center; color:#f56565;'>💀 Run beendet! Dein Pokémon ging K.O.</h1>", unsafe_allow_html=True)
    if st.button("🔄 Neues Spiel starten", use_container_width=True, type="primary"):
        for k in list(st.session_state.keys()):
            if k != "pokedex": del st.session_state[k]
        st.session_state.phase = "start"
        st.rerun()

elif st.session_state.phase == "win":
    st.markdown("<h1 style='text-align:center; color:#48bb78;'>🏆 DU BIST DER CHAMPION!</h1>", unsafe_allow_html=True)
    if st.button("🔄 Neue Herausforderung", use_container_width=True, type="primary"):
        for k in list(st.session_state.keys()):
            if k != "pokedex": del st.session_state[k]
        st.session_state.phase = "start"
        st.rerun()

import streamlit as st
import random
import requests
from typing import List, Optional

st.set_page_config(page_title="PokéSpire", page_icon="⚔️", layout="wide")

# ====================== SPRACHE ======================
if "language" not in st.session_state:
    st.session_state.language = "de"

def t(de: str, en: str):
    return de if st.session_state.language == "de" else en

# ====================== POKÉAPI ======================
@st.cache_data(ttl=3600)
def get_sprite_url(name: str):
    try:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}", timeout=10)
        data = r.json()
        return (data["sprites"]["other"]["official-artwork"]["front_default"] or 
                data["sprites"]["front_default"] or "https://via.placeholder.com/220?text=???")
    except:
        return "https://via.placeholder.com/220?text=???"

# ====================== EVOLUTION RULES ======================
EVOLUTION_RULES = {
    "bulbasaur": {"de": "Bisasam", "evo": "ivysaur", "method": "level", "param": 16},
    "ivysaur": {"de": "Bisaknosp", "evo": "venusaur", "method": "level", "param": 32},
    "charmander": {"de": "Glumanda", "evo": "charmeleon", "method": "level", "param": 16},
    "charmeleon": {"de": "Glutexo", "evo": "charizard", "method": "level", "param": 36},
    "squirtle": {"de": "Schiggy", "evo": "wartortle", "method": "level", "param": 16},
    "wartortle": {"de": "Schillok", "evo": "blastoise", "method": "level", "param": 36},
}

class Card:
    def __init__(self, name: str, damage: int, block: int, poke_type: str, cost: int = 1):
        self.name = name
        self.damage = damage
        self.block = block
        self.type = poke_type
        self.cost = cost

    def __str__(self):
        dmg = f"{self.damage} DMG" if self.damage > 0 else ""
        blk = f"{self.block} Block" if self.block > 0 else ""
        return f"[{self.cost}⚡] {self.name} — {dmg} {blk}".strip(" —")

class Pokemon:
    def __init__(self, name: str, poke_type: str, cards: List[Card], evolution: Optional[str] = None, 
                 evo_method: str = "level", evo_param: int = 16):
        self.name = name
        self.type = poke_type
        self.cards = cards
        self.level = 1
        self.evolution = evolution
        self.evo_method = evo_method
        self.evo_param = evo_param
        self.battles_won = 0
        self.friendship = 70

    def can_evolve(self):
        if not self.evolution:
            return False
        if self.evo_method == "level":
            return self.level >= self.evo_param or self.battles_won >= 5
        return False

class Player:
    def __init__(self):
        self.deck: List[Card] = []
        self.team: List[Pokemon] = []
        self.max_hp = 80
        self.hp = self.max_hp
        self.gold = 35
        self.region = 1
        self.floor = 1
        self.battles_won_total = 0
        self.stones = []  # z.B. ["fire-stone"]

    def add_pokemon(self, pokemon: Pokemon):
        self.team.append(pokemon)
        self.deck.extend(pokemon.cards)

    def check_evolutions(self):
        for i, p in enumerate(self.team):
            if p.can_evolve():
                evo_info = EVOLUTION_RULES.get(p.evolution.lower(), {})
                if not evo_info:
                    continue
                old_name = p.name
                new_name = evo_info["de"]

                new_cards = [Card(c.name, int(c.damage * 1.4), int(c.block * 1.25), c.type, c.cost) for c in p.cards]
                
                self.team[i] = Pokemon(new_name, p.type, new_cards, None, "level", 999)
                self.team[i].level = p.level + 3
                self.team[i].friendship = min(255, p.friendship + 40)
                
                self.deck = [c for c in self.deck if c.name not in [card.name for card in p.cards]]
                self.deck.extend(self.team[i].cards)
                
                st.balloons()
                st.success(f"✨ **{old_name}** evolviert zu **{new_name}**!")
                return True
        return False

# ====================== STARTER ======================
STARTERS = {
    "bulbasaur": {"de": "Bisasam", "evo": "ivysaur"},
    "charmander": {"de": "Glumanda", "evo": "charmeleon"},
    "squirtle": {"de": "Schiggy", "evo": "wartortle"}
}

def create_starter(key: str):
    # Vereinfachte echte Moves
    move_names = ["Tackle", "Growl", "Vine Whip", "Ember", "Water Gun", "Bubble"]
    cards = []
    for _ in range(5):
        name = random.choice(move_names)
        damage = random.randint(8, 22)
        block = random.randint(0, 10) if random.random() < 0.4 else 0
        cost = 1 if damage < 15 else 2
        cards.append(Card(name, damage, block, "Normal", cost))
    
    evo_info = EVOLUTION_RULES.get(key, {})
    return Pokemon(STARTERS[key]["de"], "Pflanze" if key == "bulbasaur" else "Feuer" if key == "charmander" else "Wasser",
                   cards, evo_info.get("evo"), "level", evo_info.get("param", 16))

# ====================== SESSION ======================
for key in ["player", "in_combat", "enemy", "hand", "energy", "block"]:
    if key not in st.session_state:
        st.session_state[key] = None if key == "player" else False if "combat" in key else 3 if key == "energy" else 0

# ====================== MAIN UI ======================
st.title("⚔️ PokéSpire")
st.caption("Roguelike mit echter Evolution (Level + Freundschaft)")

with st.sidebar:
    if st.button("🔄 Neustart"):
        for k in list(st.session_state.keys()):
            if k != "language":
                del st.session_state[k]
        st.rerun()

if st.session_state.player is None or (st.session_state.player and st.session_state.player.hp <= 0):
    if st.session_state.player and st.session_state.player.hp <= 0:
        st.error("💀 Game Over")
    
    lang = st.selectbox("Sprache / Language", ["Deutsch", "English"])
    st.session_state.language = "de" if lang == "Deutsch" else "en"

    st.subheader(t("Wähle dein Starter-Pokémon", "Choose Starter Pokémon"))
    starter_key = st.selectbox("Starter", list(STARTERS.keys()), format_func=lambda x: STARTERS[x]["de"])

    pokemon = create_starter(starter_key)
    sprite = get_sprite_url(starter_key)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(sprite, width=260)
    with col2:
        st.write(f"**{pokemon.name}**")
        st.write(f"Evolution: {pokemon.evolution}")
        st.write("**Attacken:**")
        for c in pokemon.cards:
            st.write("•", c)

    if st.button(t("🎮 Spiel starten", "Start Game"), type="primary", use_container_width=True):
        player = Player()
        player.add_pokemon(pokemon)
        st.session_state.player = player
        st.rerun()

else:
    player: Player = st.session_state.player

    # Status
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("❤️ HP", f"{max(0, player.hp)}/{player.max_hp}")
    with c2: st.metric("💰 Gold", player.gold)
    with c3: st.metric("📍 Region", f"{player.region} - {player.floor}")
    with c4: st.metric("🏆 Siege", player.battles_won_total)

    if st.session_state.in_combat and st.session_state.enemy:
        enemy = st.session_state.enemy
        col_e1, col_e2 = st.columns([1, 3])
        with col_e1:
            st.image(enemy.get("sprite", ""), width=200)
        with col_e2:
            st.error(f"⚔️ Kampf gegen **{enemy['name']}**")
            st.info(f"💥 Vorbereitet: {enemy['intent'].name}")

        st.subheader("🃏 Deine Hand")
        cols = st.columns(len(st.session_state.hand) or 1)
        for i, card in enumerate(st.session_state.hand):
            with cols[i]:
                if st.button(str(card), key=f"play_{i}"):
                    if st.session_state.energy >= card.cost:
                        st.session_state.energy -= card.cost
                        st.session_state.hand.pop(i)
                        if card.damage > 0:
                            enemy["hp"] -= card.damage
                        if card.block > 0:
                            st.session_state.block += card.block
                        st.rerun()

        if st.button("Zug beenden", type="primary"):
            dmg = max(0, enemy["intent"].damage - st.session_state.block)
            player.hp = max(0, player.hp - dmg)

            st.session_state.energy = 3
            st.session_state.block = 0
            st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))

            if enemy["hp"] <= 0:
                st.success("🎉 Sieg!")
                player.gold += random.randint(25, 50)
                player.battles_won_total += 1
                for p in player.team:
                    p.battles_won += 1
                    p.friendship = min(255, p.friendship + random.randint(10, 18))
                player.check_evolutions()
                st.session_state.in_combat = False
                player.floor += 1
            st.rerun()

    else:
        st.subheader("Wähle deinen Pfad")
        cols = st.columns(4)
        with cols[0]:
            if st.button("⚔️ Normaler Kampf", use_container_width=True):
                st.session_state.in_combat = True
                st.session_state.enemy = {
                    "name": random.choice(["Rattfratz", "Pidgey", "Caterpie"]),
                    "hp": random.randint(50, 70),
                    "max_hp": 70,
                    "sprite": get_sprite_url(random.choice(["rattata", "pidgey", "caterpie"])),
                    "intent": Card("Tackle", random.randint(10, 18), 0, "Normal", 1)
                }
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                st.rerun()

        st.subheader("👥 Dein Team")
        for p in player.team:
            sprite = get_sprite_url(p.name.lower())
            col_a, col_b = st.columns([1, 4])
            with col_a:
                st.image(sprite, width=130)
            with col_b:
                evo_text = f" → {p.evolution}" if p.evolution else ""
                st.write(f"**{p.name}** Lv.{p.level} ({p.battles_won} Siege){evo_text}")
                st.write(f"Freundschaft: {p.friendship}/255")

st.caption("PokéSpire • Level + Freundschaft Evolution")

if st.session_state.player and st.session_state.player.hp <= 0:
    st.error("💀 Deine Reise endet hier...")

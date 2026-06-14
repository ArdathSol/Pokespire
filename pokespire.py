import streamlit as st
import random
import json
from typing import List, Optional

st.set_page_config(page_title="PokéSpire", page_icon="⚔️", layout="centered")

# ====================== DATA ======================
class Card:
    def __init__(self, name: str, damage: int, block: int, poke_type: str, cost: int = 1):
        self.name = name
        self.damage = damage
        self.block = block
        self.type = poke_type
        self.cost = cost

    def __str__(self):
        return f"[{self.cost}⚡] {self.name} — {self.damage} DMG | {self.block} Block"

class Pokemon:
    def __init__(self, name: str, poke_type: str, cards: List[Card], evolution: Optional[str] = None, evolves_at: int = 0):
        self.name = name
        self.type = poke_type
        self.cards = cards
        self.level = 1
        self.evolution = evolution
        self.evolves_at = evolves_at
        self.battles_won = 0

    def can_evolve(self):
        return self.evolution is not None and self.battles_won >= self.evolves_at

POKEMON_DB = {
    "Glumanda": Pokemon("Glumanda", "Feuer", [
        Card("Glut", 8, 0, "Feuer"), Card("Kratzer", 6, 3, "Normal"), Card("Feuerwirbel", 12, 0, "Feuer", 2)
    ], "Glurak", 3),
    "Glurak": Pokemon("Glurak", "Feuer", [
        Card("Flammenwurf", 15, 0, "Feuer", 2), Card("Drachenwut", 18, 0, "Drache", 2), Card("Feuersturm", 22, 5, "Feuer", 3)
    ]),
    "Schiggy": Pokemon("Schiggy", "Wasser", [
        Card("Blubber", 7, 6, "Wasser"), Card("Tackle", 8, 3, "Normal"), Card("Aquaknarre", 13, 0, "Wasser", 2)
    ], "Turtok", 3),
    "Turtok": Pokemon("Turtok", "Wasser", [
        Card("Hydropumpe", 16, 0, "Wasser", 2), Card("Panzer", 0, 12, "Wasser", 2), Card("Aquaschwanz", 20, 4, "Wasser", 3)
    ]),
    "Bisasam": Pokemon("Bisasam", "Pflanze", [
        Card("Rankenhieb", 8, 5, "Pflanze"), Card("Tackle", 7, 4, "Normal"), Card("Blattschneider", 14, 0, "Pflanze", 2)
    ], "Bisaflor", 3),
    "Bisaflor": Pokemon("Bisaflor", "Pflanze", [
        Card("Solarstrahl", 19, 0, "Pflanze", 3), Card("Blütenwirbel", 15, 8, "Pflanze", 2), Card("Rankenpeitsche", 17, 6, "Pflanze", 2)
    ]),
}

class Player:
    def __init__(self):
        self.deck: List[Card] = []
        self.team: List[Pokemon] = []
        self.max_hp = 80
        self.hp = self.max_hp
        self.gold = 30
        self.region = 1
        self.floor = 1
        self.battles_won_total = 0

    def add_pokemon(self, pokemon: Pokemon):
        self.team.append(pokemon)
        self.deck.extend(pokemon.cards)

# ====================== SESSION ======================
if "player" not in st.session_state:
    st.session_state.player = None
if "in_combat" not in st.session_state:
    st.session_state.in_combat = False
if "enemy" not in st.session_state:
    st.session_state.enemy = None
if "hand" not in st.session_state:
    st.session_state.hand = []
if "energy" not in st.session_state:
    st.session_state.energy = 3
if "block" not in st.session_state:
    st.session_state.block = 0
if "message" not in st.session_state:
    st.session_state.message = ""

# ====================== UI ======================
st.title("⚔️ PokéSpire")
st.caption("Pokémon Roguelike • Slay the Spire Style")

with st.sidebar:
    st.header("Menü")
    if st.button("🏠 Hauptmenü", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key != "player":
                del st.session_state[key]
        st.rerun()

if st.session_state.player is None:
    st.subheader("Willkommen in PokéSpire!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🆕 Neues Spiel starten", type="primary", use_container_width=True):
            player = Player()
            starters = ["Glumanda", "Schiggy", "Bisasam"]
            choice = st.selectbox("Wähle dein Starter-Pokémon", starters, key="starter_select")
            player.add_pokemon(POKEMON_DB[choice])
            st.session_state.player = player
            st.rerun()
else:
    player: Player = st.session_state.player

    # Status Bar
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("HP", f"{player.hp}/{player.max_hp}")
    with col2:
        st.metric("Gold", player.gold)
    with col3:
        st.metric("Region", f"{player.region}-{player.floor}")

    if st.session_state.in_combat and st.session_state.enemy:
        enemy = st.session_state.enemy
        st.error(f"**⚔️ Kampf gegen {enemy['name']}** | HP: {enemy['hp']}/{enemy['max_hp']}")

        # Enemy Intent
        st.info(f"💥 Gegner bereitet **{enemy['intent'].name}** vor!")

        st.write("### Deine Hand")
        cols = st.columns(len(st.session_state.hand) or 1)
        for i, card in enumerate(st.session_state.hand):
            with cols[i]:
                if st.button(str(card), key=f"play_{i}", use_container_width=True):
                    if st.session_state.energy >= card.cost:
                        st.session_state.energy -= card.cost
                        st.session_state.hand.pop(i)
                        if card.damage > 0:
                            enemy["hp"] -= card.damage
                            st.session_state.message = f"✅ {card.name} macht {card.damage} Schaden!"
                        if card.block > 0:
                            st.session_state.block += card.block
                            st.session_state.message = f"🛡️ {card.name} gibt {card.block} Block!"
                        st.rerun()

        # Controls
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Zug beenden", type="secondary"):
                # Enemy attacks
                dmg = max(0, enemy["intent"].damage - st.session_state.block)
                player.hp -= dmg
                st.session_state.message = f"💥 Gegner macht {dmg} Schaden!"

                # New turn
                st.session_state.energy = 3
                st.session_state.block = 0
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                
                # Enemy new intent
                enemy["intent"] = random.choice(enemy["moves"])

                if enemy["hp"] <= 0:
                    st.success("🎉 Sieg!")
                    player.gold += random.randint(25, 40)
                    for p in player.team:
                        p.battles_won += 1
                    st.session_state.in_combat = False
                    player.floor += 1
                st.rerun()

        with c2:
            if st.button("Aufgeben", type="primary"):
                st.session_state.in_combat = False

        if st.session_state.message:
            st.write(st.session_state.message)

    else:
        # Exploration
        st.subheader("Wohin möchtest du gehen?")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("⚔️ Normaler Kampf", use_container_width=True):
                st.session_state.in_combat = True
                moves = [Card("Tackle", 9, 0, "Normal"), Card("Biss", 11, 0, "Normal")]
                st.session_state.enemy = {
                    "name": "Wildes Rattfratz",
                    "hp": 45,
                    "max_hp": 45,
                    "moves": moves,
                    "intent": random.choice(moves)
                }
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                st.rerun()
        with col2:
            if st.button("🔥 Elite Kampf", use_container_width=True):
                st.session_state.in_combat = True
                moves = [Card("Flammenwurf", 16, 0, "Feuer", 2)]
                st.session_state.enemy = {
                    "name": "Elite-Trainer",
                    "hp": 75,
                    "max_hp": 75,
                    "moves": moves,
                    "intent": random.choice(moves)
                }
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                st.rerun()

        # Team & Deck
        tab1, tab2 = st.tabs(["👥 Team", "🃏 Deck"])
        with tab1:
            for p in player.team:
                evo = f" → {p.evolution}" if p.can_evolve() else ""
                st.write(f"**{p.name}** Lv.{p.level} ({p.battles_won} Siege){evo}")
        with tab2:
            for card in player.deck:
                st.write(str(card))

# Win Condition
if player.hp > 0 and player.region >= 4 and player.floor > 5:
    st.balloons()
    st.success("🎊 **Du hast die Pokémon-Liga besiegt!**")

st.caption("PokéSpire Streamlit • Card Game Mechanics")

import streamlit as st
import random
import json
import os
from typing import List, Optional

st.set_page_config(page_title="PokéSpire", page_icon="⚔️", layout="wide")

# ====================== CARD & POKEMON ======================
class Card:
    def __init__(self, name: str, damage: int, block: int, poke_type: str, cost: int = 1):
        self.name = name
        self.damage = damage
        self.block = block
        self.type = poke_type
        self.cost = cost

    def __str__(self):
        return f"[{self.cost}⚡] {self.name} - {self.damage} DMG | {self.block} Block"

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

# ====================== PLAYER ======================
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

def init_session():
    if "player" not in st.session_state:
        st.session_state.player = None
    if "in_combat" not in st.session_state:
        st.session_state.in_combat = False
    if "current_enemy" not in st.session_state:
        st.session_state.current_enemy = None
    if "hand" not in st.session_state:
        st.session_state.hand = []
    if "block" not in st.session_state:
        st.session_state.block = 0

init_session()

# ====================== UI ======================
st.title("⚔️ PokéSpire")
st.caption("Pokémon Roguelike im Stil von Slay the Spire")

# Sidebar
with st.sidebar:
    st.header("Menü")
    if st.button("🏠 Hauptmenü"):
        st.session_state.player = None
        st.session_state.in_combat = False
        st.rerun()

# Main Game
if st.session_state.player is None:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🆕 Neues Spiel", type="primary", use_container_width=True):
            player = Player()
            starters = ["Glumanda", "Schiggy", "Bisasam"]
            choice = st.selectbox("Wähle dein Starter-Pokémon", starters)
            player.add_pokemon(POKEMON_DB[choice])
            st.session_state.player = player
            st.rerun()
    with col2:
        if st.button("📂 Spiel laden", use_container_width=True):
            st.info("Laden wird noch entwickelt (Session-State wird bei Neustart gelöscht)")
else:
    player = st.session_state.player
    st.write(f"**Region {player.region} — Stockwerk {player.floor}**")
    st.progress(player.hp / player.max_hp, text=f"HP: {player.hp}/{player.max_hp} | Gold: {player.gold}")

    # Navigation
    tab1, tab2, tab3, tab4 = st.tabs(["🌍 Karte", "👥 Team", "🃏 Deck", "💾 Speichern"])

    with tab1:
        if st.session_state.in_combat:
            enemy = st.session_state.current_enemy
            st.error(f"⚔️ Kampf gegen **{enemy.name}** (HP: {enemy.hp}/{enemy.max_hp})")

            st.write("**Deine Hand:**")
            cols = st.columns(len(st.session_state.hand))
            for i, card in enumerate(st.session_state.hand):
                with cols[i]:
                    if st.button(str(card), key=f"card_{i}"):
                        # Play card
                        energy = 3  # simplified
                        st.session_state.hand.pop(i)
                        if card.damage > 0:
                            enemy.hp -= card.damage
                        if card.block > 0:
                            st.session_state.block += card.block
                        st.rerun()

            if st.button("Zug beenden"):
                # Enemy attack (simplified)
                dmg = 10 - st.session_state.block
                if dmg > 0:
                    player.hp -= max(0, dmg)
                st.session_state.block = 0
                st.session_state.hand = player.deck[:5]
                st.rerun()

            if enemy.hp <= 0:
                st.success("🎉 Sieg!")
                player.gold += 30
                for p in player.team:
                    p.battles_won += 1
                st.session_state.in_combat = False
                player.floor += 1
                st.rerun()

        else:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("⚔️ Normaler Kampf", use_container_width=True):
                    st.session_state.in_combat = True
                    st.session_state.current_enemy = type('obj', (object,), {'name': 'Wildes Rattfratz', 'hp': 45, 'max_hp': 45})()
                    st.session_state.hand = player.deck[:5]
                    st.rerun()
            with col2:
                if st.button("🔥 Elite Kampf", use_container_width=True):
                    st.session_state.in_combat = True
                    st.session_state.current_enemy = type('obj', (object,), {'name': 'Elite-Trainer', 'hp': 75, 'max_hp': 75})()
                    st.session_state.hand = player.deck[:5]
                    st.rerun()

    with tab2:
        st.write("### Dein Team")
        for p in player.team:
            evo = f" → {p.evolution}" if p.can_evolve() else ""
            st.write(f"**{p.name}** Lv.{p.level} ({p.battles_won} Siege){evo}")

    with tab3:
        st.write("### Dein Deck")
        for card in player.deck:
            st.write(str(card))

    with tab4:
        if st.button("💾 Aktuellen Stand speichern (Session)"):
            st.success("Fortschritt in diesem Browser-Tab gespeichert!")

# Footer
st.caption("PokéSpire Streamlit Edition • Einfach auf GitHub hochladen und mit Streamlit Cloud verbinden")

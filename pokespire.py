import streamlit as st
import random
from typing import List, Optional

st.set_page_config(page_title="PokéSpire", page_icon="⚔️", layout="wide")

# ====================== SPRACHE ======================
if "language" not in st.session_state:
    st.session_state.language = "de"

def t(text_de: str, text_en: str):
    return text_de if st.session_state.language == "de" else text_en

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

POKEMON_IMAGES = {
    "Glumanda": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/004.png",
    "Schiggy": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/007.png",
    "Bisasam": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/001.png",
    "Glurak": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/006.png",
    "Turtok": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/009.png",
    "Bisaflor": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/003.png",
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
st.caption(t("Ein Pokémon-Roguelike wie Slay the Spire", "A Pokémon Roguelike like Slay the Spire"))

with st.sidebar:
    st.header(t("Menü", "Menu"))
    if st.button(t("🏠 Hauptmenü", "🏠 Main Menu"), use_container_width=True):
        for key in list(st.session_state.keys()):
            if key not in ["language"]:
                del st.session_state[key]
        st.rerun()

# Sprachauswahl (nur am Anfang)
if st.session_state.player is None:
    col1, col2 = st.columns([1, 5])
    with col1:
        lang = st.selectbox("Sprache / Language", ["Deutsch", "English"], key="lang_select")
        st.session_state.language = "de" if lang == "Deutsch" else "en"

if st.session_state.player is None:
    st.subheader(t("Willkommen in PokéSpire!", "Welcome to PokéSpire!"))
    
    starters = ["Glumanda", "Schiggy", "Bisasam"]
    choice_name = st.selectbox(
        t("Wähle dein Starter-Pokémon", "Choose your Starter Pokémon"),
        starters
    )
    
    col_img, col_info = st.columns([1, 2])
    with col_img:
        st.image(POKEMON_IMAGES[choice_name], width=220)
    
    with col_info:
        p = POKEMON_DB[choice_name]
        st.write(f"**{choice_name}** — {p.type}")
        st.write(t("**Basis-Attacken:**", "**Base Moves:**"))
        for card in p.cards:
            st.write(f"• {card}")
    
    if st.button(t("🎮 Spiel starten", "🎮 Start Game"), type="primary", use_container_width=True):
        player = Player()
        player.add_pokemon(POKEMON_DB[choice_name])
        st.session_state.player = player
        st.rerun()

else:
    player: Player = st.session_state.player

    # Status Bar
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t("HP", "HP"), f"{max(0, player.hp)}/{player.max_hp}")
    with col2:
        st.metric(t("Gold", "Gold"), player.gold)
    with col3:
        st.metric(t("Region", "Region"), f"{player.region} - {player.floor}")
    with col4:
        st.metric(t("Siege", "Wins"), player.battles_won_total)

    if st.session_state.in_combat and st.session_state.enemy:
        enemy = st.session_state.enemy
        st.error(f"⚔️ {t('Kampf gegen', 'Battle vs')} **{enemy['name']}** | HP: {max(0, enemy['hp'])}/{enemy['max_hp']}")

        st.info(f"💥 {t('Gegner bereitet vor', 'Enemy preparing')}: **{enemy['intent'].name}**")

        st.subheader(t("Deine Hand", "Your Hand"))
        cols = st.columns(len(st.session_state.hand) or 1)
        for i, card in enumerate(st.session_state.hand):
            with cols[i]:
                if st.button(str(card), key=f"play_{i}", use_container_width=True):
                    if st.session_state.energy >= card.cost:
                        st.session_state.energy -= card.cost
                        st.session_state.hand.pop(i)
                        if card.damage > 0:
                            enemy["hp"] -= card.damage
                        if card.block > 0:
                            st.session_state.block += card.block
                        st.rerun()

        c1, c2 = st.columns(2)
        with c1:
            if st.button(t("Zug beenden", "End Turn"), use_container_width=True):
                dmg = max(0, enemy["intent"].damage - st.session_state.block)
                player.hp = max(0, player.hp - dmg)
                
                st.session_state.energy = 3
                st.session_state.block = 0
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                enemy["intent"] = random.choice(enemy["moves"])

                if enemy["hp"] <= 0:
                    st.success(t("🎉 Sieg!", "🎉 Victory!"))
                    player.gold += random.randint(25, 45)
                    for p in player.team:
                        p.battles_won += 1
                    st.session_state.in_combat = False
                    player.floor += 1
                st.rerun()

        with c2:
            if st.button(t("Aufgeben", "Forfeit"), use_container_width=True):
                st.session_state.in_combat = False

    else:
        st.subheader(t("Wohin möchtest du gehen?", "Where do you want to go?"))
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚔️ " + t("Normaler Kampf", "Normal Fight"), use_container_width=True):
                st.session_state.in_combat = True
                moves = [Card("Tackle", 9, 0, "Normal"), Card("Biss", 11, 0, "Normal")]
                st.session_state.enemy = {
                    "name": t("Wildes Rattfratz", "Wild Rattata"),
                    "hp": 48, "max_hp": 48,
                    "moves": moves,
                    "intent": random.choice(moves)
                }
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                st.rerun()
        with col2:
            if st.button("🔥 " + t("Elite Kampf", "Elite Battle"), use_container_width=True):
                st.session_state.in_combat = True
                moves = [Card("Flammenwurf", 16, 0, "Feuer", 2)]
                st.session_state.enemy = {
                    "name": t("Elite-Trainer", "Elite Trainer"),
                    "hp": 78, "max_hp": 78,
                    "moves": moves,
                    "intent": random.choice(moves)
                }
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                st.rerun()

        tab1, tab2 = st.tabs([t("👥 Team", "👥 Team"), t("🃏 Deck", "🃏 Deck")])
        with tab1:
            for p in player.team:
                st.image(POKEMON_IMAGES.get(p.name, ""), width=140)
                evo = f" → {p.evolution}" if p.can_evolve() else ""
                st.write(f"**{p.name}** Lv.{p.level} ({p.battles_won} {t('Siege','Wins')}){evo}")
        with tab2:
            for card in player.deck:
                st.write(str(card))

# Win Condition (sicherer)
if st.session_state.player and st.session_state.player.hp > 0 and st.session_state.player.region >= 4 and st.session_state.player.floor > 5:
    st.balloons()
    st.success(t("🎊 Du hast die Pokémon-Liga besiegt!", "🎊 You have defeated the Pokémon League!"))

st.caption("PokéSpire • Streamlit Edition")

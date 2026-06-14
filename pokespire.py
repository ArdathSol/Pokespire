import streamlit as st
import random
from typing import List, Optional

st.set_page_config(page_title="PokéSpire", page_icon="⚔️", layout="wide")

# ====================== SPRACHE ======================
if "language" not in st.session_state:
    st.session_state.language = "de"

def t(de: str, en: str):
    return de if st.session_state.language == "de" else en

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

POKEMON_DB = { ... }  # (gleiche Daten wie vorher – aus Platzgründen gekürzt, nimm die vorherige Version)

POKEMON_IMAGES = {
    "Glumanda": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/004.png",
    "Schiggy": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/007.png",
    "Bisasam": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/001.png",
    "Glurak": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/006.png",
    "Turtok": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/009.png",
    "Bisaflor": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/003.png",
    "Rattfratz": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/019.png",
    "Elite-Trainer": "https://i.imgur.com/5z5z5z5.png"  # Platzhalter
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

    def check_evolutions(self):
        evolved = False
        for p in self.team:
            if p.can_evolve():
                new_poke = POKEMON_DB.get(p.evolution)
                if new_poke:
                    idx = self.team.index(p)
                    old_name = p.name
                    self.team[idx] = Pokemon(new_poke.name, new_poke.type, new_poke.cards.copy(), 
                                           new_poke.evolution, new_poke.evolves_at)
                    self.team[idx].battles_won = p.battles_won
                    self.deck = [c for c in self.deck if c.name not in [card.name for card in p.cards]]
                    self.deck.extend(self.team[idx].cards)
                    st.success(f"🌟 {old_name} hat sich zu **{new_poke.name}** entwickelt!")
                    evolved = True
        return evolved

# ====================== SESSION ======================
for key in ["player", "in_combat", "enemy", "hand", "energy", "block", "message", "path_history"]:
    if key not in st.session_state:
        st.session_state[key] = None if key == "player" else False if key == "in_combat" else [] if key == "path_history" else 0 if key in ["energy","block"] else ""

# ====================== UI ======================
st.title("⚔️ PokéSpire")
st.caption(t("Pokémon Roguelike • Slay the Spire Style", "Pokémon Roguelike • Slay the Spire Style"))

# Hauptmenü / Neustart
if st.session_state.player is None or (st.session_state.player and st.session_state.player.hp <= 0):
    if st.session_state.player and st.session_state.player.hp <= 0:
        st.error("💀 GAME OVER")
        st.balloons()
    
    col_lang, _ = st.columns([1,4])
    with col_lang:
        lang = st.selectbox("Sprache / Language", ["Deutsch", "English"])
        st.session_state.language = "de" if lang == "Deutsch" else "en"

    st.subheader(t("Willkommen in PokéSpire!", "Welcome to PokéSpire!"))
    starters = ["Glumanda", "Schiggy", "Bisasam"]
    choice = st.selectbox(t("Starter-Pokémon wählen", "Choose Starter"), starters)
    
    col1, col2 = st.columns([1,2])
    with col1:
        st.image(POKEMON_IMAGES[choice], width=220)
    with col2:
        p = POKEMON_DB[choice]
        st.write(f"**{choice}** — {p.type}")
        for card in p.cards:
            st.write("•", card)
    
    if st.button(t("🎮 Neues Spiel starten", "🎮 Start New Game"), type="primary"):
        player = Player()
        player.add_pokemon(POKEMON_DB[choice])
        st.session_state.player = player
        st.session_state.in_combat = False
        st.rerun()

else:
    player = st.session_state.player

    # Status
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("HP", f"{max(0, player.hp)}/{player.max_hp}")
    with c2: st.metric(t("Gold", "Gold"), player.gold)
    with c3: st.metric("Region", f"{player.region}-{player.floor}")
    with c4: st.metric(t("Siege", "Wins"), player.battles_won_total)

    # === KAMPF ===
    if st.session_state.in_combat and st.session_state.enemy:
        enemy = st.session_state.enemy
        col_e1, col_e2 = st.columns([1,3])
        with col_e1:
            st.image(POKEMON_IMAGES.get(enemy["name"].split()[-1], "https://via.placeholder.com/150"), width=180)
        with col_e2:
            st.error(f"⚔️ {t('Kampf gegen', 'Battle vs')} **{enemy['name']}**")
            st.info(f"💥 {t('Vorbereitete Attacke', 'Intent')}: **{enemy['intent'].name}**")

        # Hand
        st.subheader(t("Deine Hand", "Your Hand"))
        cols = st.columns(len(st.session_state.hand) or 1)
        for i, card in enumerate(st.session_state.hand):
            with cols[i]:
                if st.button(str(card), key=f"card{i}"):
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
            if st.button(t("Zug beenden", "End Turn"), type="primary"):
                # Enemy Attack
                dmg = max(0, enemy["intent"].damage - st.session_state.block)
                player.hp = max(0, player.hp - dmg)

                # Neue Runde
                st.session_state.energy = 3
                st.session_state.block = 0
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                enemy["intent"] = random.choice(enemy["moves"])

                if enemy["hp"] <= 0:
                    st.success(t("🎉 Sieg!", "🎉 Victory!"))
                    reward = random.randint(25, 45)
                    player.gold += reward
                    player.battles_won_total += 1
                    for p in player.team:
                        p.battles_won += 1
                    player.check_evolutions()
                    st.session_state.in_combat = False
                    player.floor += 1
                st.rerun()

    else:
        # === PFAD-AUSWAHL (Slay the Spire Style) ===
        st.subheader(t("Wähle deinen Pfad", "Choose your Path"))
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("⚔️ " + t("Kampf", "Fight"), use_container_width=True):
                st.session_state.in_combat = True
                st.session_state.enemy = {
                    "name": t("Wildes Rattfratz", "Wild Rattata"),
                    "hp": 50, "max_hp": 50,
                    "moves": [Card("Biss", 11, 0, "Normal"), Card("Tackle", 8, 0, "Normal")],
                    "intent": Card("Biss", 11, 0, "Normal")
                }
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                st.rerun()

        with col2:
            if st.button("🔥 " + t("Elite", "Elite"), use_container_width=True):
                st.session_state.in_combat = True
                st.session_state.enemy = {
                    "name": t("Elite-Trainer", "Elite Trainer"),
                    "hp": 85, "max_hp": 85,
                    "moves": [Card("Flammenwurf", 16, 0, "Feuer", 2)],
                    "intent": Card("Flammenwurf", 16, 0, "Feuer", 2)
                }
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                st.rerun()

        with col3:
            if st.button("🛒 " + t("Shop", "Shop"), use_container_width=True):
                st.success(t("Heiltrank gekauft (+35 HP)", "Heal Potion bought (+35 HP)"))
                player.hp = min(player.max_hp, player.hp + 35)
                player.gold = max(0, player.gold - 25)

        with col4:
            if st.button("🛡️ " + t("Rast", "Rest"), use_container_width=True):
                heal = 20
                player.hp = min(player.max_hp, player.hp + heal)
                st.success(t(f"Du ruhst dich aus (+{heal} HP)", f"You rested (+{heal} HP)"))

        with col5:
            if st.button("❓ " + t("Event", "Event"), use_container_width=True):
                if random.random() < 0.6:
                    new_poke = random.choice(list(POKEMON_DB.keys()))
                    player.add_pokemon(POKEMON_DB[new_poke])
                    st.success(f"✨ {new_poke} hat sich deinem Team angeschlossen!")

        # Team & Deck
        tab1, tab2 = st.tabs([t("👥 Team", "Team"), t("🃏 Deck", "Deck")])
        with tab1:
            for p in player.team:
                st.image(POKEMON_IMAGES.get(p.name, ""), width=130)
                evo = f" → {p.evolution}" if p.can_evolve() else ""
                st.write(f"**{p.name}** Lv.{p.level} ({p.battles_won} Siege){evo}")

        with tab2:
            for card in player.deck:
                st.write(str(card))

# Win / Game Over
if st.session_state.player and st.session_state.player.hp <= 0:
    st.error("💀 " + t("Deine Reise endet hier...", "Your journey ends here..."))
    if st.button(t("Neues Spiel starten", "Start New Game")):
        st.session_state.player = None
        st.rerun()

elif st.session_state.player and st.session_state.player.region >= 4 and st.session_state.player.floor > 6:
    st.balloons()
    st.success(t("🎊 Du hast die Pokémon-Liga besiegt!", "🎊 You defeated the Pokémon League!"))

st.caption("PokéSpire • Verbesserte Version")

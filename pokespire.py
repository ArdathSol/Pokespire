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
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}", timeout=8)
        data = r.json()
        return (data["sprites"]["other"]["official-artwork"]["front_default"] or 
                data["sprites"]["front_default"])
    except:
        return "https://via.placeholder.com/220?text=???"

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

class Relic:
    def __init__(self, name: str, desc: str, effect: str = ""):
        self.name = name
        self.desc = desc
        self.effect = effect

class Pokemon:
    def __init__(self, name: str, poke_type: str, cards: List[Card], evolution: Optional[str] = None, evo_param: int = 16):
        self.name = name
        self.type = poke_type
        self.cards = cards
        self.level = 1
        self.evolution = evolution
        self.evo_param = evo_param
        self.battles_won = 0
        self.friendship = 70

    def can_evolve(self):
        return self.evolution and (self.level >= self.evo_param or self.battles_won >= 5)

class Player:
    def __init__(self):
        self.deck: List[Card] = []
        self.team: List[Pokemon] = []
        self.max_hp = 80
        self.hp = self.max_hp
        self.gold = 40
        self.region = 1
        self.floor = 1
        self.battles_won_total = 0
        self.relics: List[Relic] = []
        self.friendship_bonus = 0

    def add_pokemon(self, pokemon: Pokemon):
        self.team.append(pokemon)
        self.deck.extend(pokemon.cards)

# ====================== SESSION ======================
for key in ["player", "in_combat", "enemy", "hand", "energy", "block"]:
    if key not in st.session_state:
        st.session_state[key] = None if key == "player" else False if "combat" in key else 3 if key == "energy" else 0

# ====================== UI ======================
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #0a0a1f, #1a1a2e); color: #e0e0ff; }
    .metric { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("⚔️ PokéSpire")
st.caption(t("Roguelike mit echter Evolution • Level + Freundschaft", "Roguelike with real Evolution"))

with st.sidebar:
    if st.button("🔄 Neustart"):
        for k in list(st.session_state.keys()):
            if k != "language":
                del st.session_state[k]
        st.rerun()

if st.session_state.player is None or (st.session_state.player and st.session_state.player.hp <= 0):
    if st.session_state.player and st.session_state.player.hp <= 0:
        st.error("💀 Game Over - Deine Reise endet hier.")
    
    lang = st.selectbox("Sprache / Language", ["Deutsch", "English"])
    st.session_state.language = "de" if lang == "Deutsch" else "en"

    st.subheader(t("Wähle dein Starter-Pokémon", "Choose Starter Pokémon"))
    starters = ["bulbasaur", "charmander", "squirtle"]
    choice = st.selectbox("Starter", starters, format_func=lambda x: {"bulbasaur":"Bisasam", "charmander":"Glumanda", "squirtle":"Schiggy"}[x])

    col1, col2 = st.columns([1,2])
    with col1:
        st.image(get_sprite_url(choice), width=280)
    with col2:
        st.write(f"**{ {'bulbasaur':'Bisasam', 'charmander':'Glumanda', 'squirtle':'Schiggy'}[choice] }**")
        st.write("**Basis-Attacken:**")
        st.info("Attacken werden dynamisch generiert")

    if st.button(t("🎮 Spiel starten", "Start Game"), type="primary", use_container_width=True):
        # Einfacher Starter
        player = Player()
        cards = [Card("Tackle", 10, 3, "Normal", 1), Card("Growl", 0, 6, "Normal", 1),
                 Card("Vine Whip" if choice=="bulbasaur" else "Ember" if choice=="charmander" else "Water Gun", 14, 0, "Grass" if choice=="bulbasaur" else "Fire" if choice=="charmander" else "Water", 2)]
        p = Pokemon({"bulbasaur":"Bisasam", "charmander":"Glumanda", "squirtle":"Schiggy"}[choice], 
                    "Pflanze" if choice=="bulbasaur" else "Feuer" if choice=="charmander" else "Wasser", 
                    cards, "ivysaur" if choice=="bulbasaur" else "charmeleon" if choice=="charmander" else "wartortle")
        player.add_pokemon(p)
        st.session_state.player = player
        st.rerun()

else:
    player = st.session_state.player

    # Status Bar
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("❤️ HP", f"{max(0, player.hp)}/{player.max_hp}")
    with c2: st.metric("💰 Gold", player.gold)
    with c3: st.metric("📍 Region", f"{player.region} - {player.floor}")
    with c4: st.metric("🏆 Siege", player.battles_won_total)

    # Relikte
    if player.relics:
        with st.expander("🛡️ Relikte"):
            for r in player.relics:
                st.write(f"**{r.name}**: {r.desc}")

    if st.session_state.in_combat and st.session_state.enemy:
        enemy = st.session_state.enemy
        col_e1, col_e2 = st.columns([1, 3])
        with col_e1:
            st.image(enemy.get("sprite", ""), width=200)
        with col_e2:
            st.error(f"⚔️ Kampf gegen **{enemy['name']}**")
            st.info(f"💥 Vorbereitet: {enemy['intent'].name}")

        # Energie Anzeige
        st.write(f"**Energie:** {'⚡' * st.session_state.energy} **({st.session_state.energy}/3)**")

        st.subheader("🃏 Deine Hand")
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
                    p.friendship = min(255, p.friendship + random.randint(12, 20))
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
                    "name": random.choice(["Rattfratz", "Taubsi", "Raupy", "Hornliu"]),
                    "hp": random.randint(48, 75),
                    "max_hp": 75,
                    "sprite": get_sprite_url(random.choice(["rattata", "pidgey", "caterpie", "weedle"])),
                    "intent": Card("Tackle", random.randint(9, 17), 0, "Normal", 1)
                }
                st.session_state.hand = random.sample(player.deck, min(5, len(player.deck)))
                st.rerun()

        # Team
        st.subheader("👥 Dein Team")
        for p in player.team:
            sprite = get_sprite_url(p.name.lower())
            col_a, col_b = st.columns([1,4])
            with col_a:
                st.image(sprite, width=130)
            with col_b:
                evo = f" → {p.evolution}" if p.evolution else ""
                st.write(f"**{p.name}** Lv.{p.level}{evo}")
                st.write(f"Freundschaft: {p.friendship}/255")

st.caption("PokéSpire • Verbessertes UI + Relikte + Energie-System")

if st.session_state.player and st.session_state.player.hp <= 0:
    st.error("💀 Deine Reise endet hier...")

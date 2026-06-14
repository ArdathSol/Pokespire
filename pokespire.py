import random
import json
import os
from typing import List, Optional

SAVE_FILE = "pokespire_save.json"

# ====================== CARD & POKEMON ======================
class Card:
    def __init__(self, name: str, damage: int, block: int, poke_type: str, cost: int = 1):
        self.name = name
        self.damage = damage
        self.block = block
        self.type = poke_type
        self.cost = cost

    def __str__(self):
        return f"[{self.cost}⚡] {self.name} - {self.damage} Schaden | {self.block} Block"

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class Pokemon:
    def __init__(self, name: str, poke_type: str, cards: List[Card], evolution: Optional[str] = None, evolves_at: int = 0):
        self.name = name
        self.type = poke_type
        self.cards = cards
        self.level = 1
        self.evolution = evolution
        self.evolves_at = evolves_at
        self.battles_won = 0

    def get_all_cards(self):
        return self.cards.copy()

    def can_evolve(self):
        return self.evolution is not None and self.battles_won >= self.evolves_at

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "level": self.level,
            "battles_won": self.battles_won,
            "cards": [c.to_dict() for c in self.cards]
        }

    @classmethod
    def from_dict(cls, data, pokemon_db):
        cards = [Card.from_dict(c) for c in data.get("cards", [])]
        base = pokemon_db.get(data["name"])
        if base:
            p = Pokemon(base.name, base.type, cards, base.evolution, base.evolves_at)
            p.level = data.get("level", 1)
            p.battles_won = data.get("battles_won", 0)
            return p
        return None

POKEMON_DB = {
    "Glumanda": Pokemon("Glumanda", "Feuer", [Card("Glut", 8, 0, "Feuer"), Card("Kratzer", 6, 3, "Normal"), Card("Feuerwirbel", 12, 0, "Feuer", 2)], "Glurak", 3),
    "Glurak": Pokemon("Glurak", "Feuer", [Card("Flammenwurf", 15, 0, "Feuer", 2), Card("Drachenwut", 18, 0, "Drache", 2), Card("Feuersturm", 22, 5, "Feuer", 3)]),
    "Schiggy": Pokemon("Schiggy", "Wasser", [Card("Blubber", 7, 6, "Wasser"), Card("Tackle", 8, 3, "Normal"), Card("Aquaknarre", 13, 0, "Wasser", 2)], "Turtok", 3),
    "Turtok": Pokemon("Turtok", "Wasser", [Card("Hydropumpe", 16, 0, "Wasser", 2), Card("Panzer", 0, 12, "Wasser", 2), Card("Aquaschwanz", 20, 4, "Wasser", 3)]),
    "Bisasam": Pokemon("Bisasam", "Pflanze", [Card("Rankenhieb", 8, 5, "Pflanze"), Card("Tackle", 7, 4, "Normal"), Card("Blattschneider", 14, 0, "Pflanze", 2)], "Bisaflor", 3),
    "Bisaflor": Pokemon("Bisaflor", "Pflanze", [Card("Solarstrahl", 19, 0, "Pflanze", 3), Card("Blütenwirbel", 15, 8, "Pflanze", 2), Card("Rankenpeitsche", 17, 6, "Pflanze", 2)]),
}

def get_pokemon(name: str):
    p = POKEMON_DB.get(name)
    if p:
        return Pokemon(p.name, p.type, p.cards.copy(), p.evolution, p.evolves_at)
    return None

# ====================== PLAYER ======================
class Player:
    def __init__(self):
        self.deck: List[Card] = []
        self.team: List[Pokemon] = []
        self.max_hp = 80
        self.hp = self.max_hp
        self.gold = 30
        self.battles_won_total = 0
        self.region = 1
        self.floor = 1

    def add_pokemon(self, pokemon: Pokemon):
        self.team.append(pokemon)
        self.deck.extend(pokemon.get_all_cards())
        print(f"✨ {pokemon.name} ({pokemon.type}) schließt sich deinem Team an!")

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def check_evolutions(self):
        for poke in list(self.team):
            if poke.can_evolve():
                print(f"\n🌟 {poke.name} kann sich zu {poke.evolution} entwickeln!")
                if input(f"Entwickeln? (j/n): ").lower() == 'j':
                    new_poke = get_pokemon(poke.evolution)
                    if new_poke:
                        idx = self.team.index(poke)
                        self.team[idx] = new_poke
                        self.deck = [c for c in self.deck if c.name not in [card.name for card in poke.cards]]
                        self.deck.extend(new_poke.get_all_cards())
                        print(f"🎉 {poke.name} → {new_poke.name}!")
                        return True
        return False

    def to_dict(self):
        return {
            "hp": self.hp,
            "max_hp": self.max_hp,
            "gold": self.gold,
            "battles_won_total": self.battles_won_total,
            "region": self.region,
            "floor": self.floor,
            "team": [p.to_dict() for p in self.team],
            "deck": [c.to_dict() for c in self.deck]
        }

    @classmethod
    def from_dict(cls, data):
        player = cls()
        player.hp = data.get("hp", 80)
        player.max_hp = data.get("max_hp", 80)
        player.gold = data.get("gold", 30)
        player.battles_won_total = data.get("battles_won_total", 0)
        player.region = data.get("region", 1)
        player.floor = data.get("floor", 1)

        for p_data in data.get("team", []):
            poke = Pokemon.from_dict(p_data, POKEMON_DB)
            if poke:
                player.team.append(poke)
                for card in poke.get_all_cards():
                    player.deck.append(card)
        return player

# ====================== COMBAT ======================
class Enemy:
    def __init__(self, name: str, hp: int, moves: List[Card]):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.moves = moves

    def get_intent(self):
        return random.choice(self.moves)

def combat(player: Player, enemy: Enemy):
    print(f"\n⚔️  Kampf gegen {enemy.name}!\n")
    energy = 3
    block = 0
    player.shuffle_deck()

    while player.hp > 0 and enemy.hp > 0:
        if len(player.deck) < 5:
            player.shuffle_deck()
        hand = player.deck[:5]
        player.deck = player.deck[5:]

        print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp} | Deine HP: {player.hp}/{player.max_hp}")
        print(f"Energie: {energy} | Block: {block}\nHand:")
        for i, card in enumerate(hand):
            print(f"{i+1}. {card}")

        intent = enemy.get_intent()
        print(f"\n{enemy.name} bereitet {intent.name} vor...")

        while energy > 0 and hand:
            try:
                choice = input("\nKarte wählen (Nummer) oder 'e' Ende: ").strip().lower()
                if choice == 'e':
                    break
                idx = int(choice) - 1
                if 0 <= idx < len(hand):
                    card = hand.pop(idx)
                    energy -= card.cost
                    if card.damage > 0:
                        enemy.hp -= card.damage
                        print(f"→ {card.name} macht {card.damage} Schaden!")
                    if card.block > 0:
                        block += card.block
                        print(f"→ {card.name} gibt {card.block} Block!")
            except:
                continue

        dmg = max(0, intent.damage - block)
        if dmg > 0:
            player.hp -= dmg
            print(f"{enemy.name} macht {dmg} Schaden!")
        block = max(0, block - intent.damage)
        energy = 3

    if player.hp > 0:
        print(f"\n🎉 Sieg gegen {enemy.name}!")
        player.gold += random.randint(20, 40)
        player.battles_won_total += 1
        for p in player.team:
            p.battles_won += 1
        return True
    return False

# ====================== SAVE / LOAD ======================
def save_game(player: Player):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(player.to_dict(), f, ensure_ascii=False, indent=2)
        print("💾 Spiel gespeichert!")
        return True
    except:
        print("Fehler beim Speichern!")
        return False

def load_game():
    if not os.path.exists(SAVE_FILE):
        print("Kein Speicherstand gefunden.")
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        player = Player.from_dict(data)
        print("✅ Spielstand geladen!")
        return player
    except:
        print("Fehler beim Laden!")
        return None

# ====================== MENUS ======================
def show_team(player: Player):
    print("\n=== Dein Team ===")
    for i, p in enumerate(player.team):
        evo = f" → {p.evolution}" if p.can_evolve() else ""
        print(f"{i+1}. {p.name} Lv.{p.level} ({p.battles_won} Siege){evo}")

def choose_path():
    print("\n1. Kampf  2. Elite  3. Shop  4. Event  5. Team  6. Speichern  7. Beenden")
    return input("Wahl: ").strip()

def main_menu():
    print("\n" + "="*55)
    print("                  POKÉSPIRE")
    print("="*55)
    print("1. Neues Spiel starten")
    print("2. Spiel laden")
    print("3. Beenden")
    return input("\nWahl: ").strip()

def main():
    while True:
        choice = main_menu()
        if choice == "3":
            print("Bis zum nächsten Mal!")
            break
        elif choice == "1":
            player = Player()
            starters = ["Glumanda", "Schiggy", "Bisasam"]
            print("\nWähle dein Starter-Pokémon:")
            for i, s in enumerate(starters, 1):
                print(f"{i}. {s}")
            try:
                sel = int(input("\nNummer: ")) - 1
                player.add_pokemon(get_pokemon(starters[sel]))
            except:
                player.add_pokemon(get_pokemon("Glumanda"))
        elif choice == "2":
            player = load_game()
            if not player:
                continue
        else:
            continue

        # Hauptspiel
        while player.hp > 0 and player.region <= 4:
            print(f"\n=== REGION {player.region} — Stockwerk {player.floor}/5 ===")
            path = choose_path()

            if path == "1":
                enemies = [
                    Enemy("Wildes Rattfratz", 40, [Card("Biss", 10, 0, "Normal")]),
                    Enemy("Trainer", 50, [Card("Tackle", 9, 0, "Normal"), Card("Donnerschock", 12, 0, "Elektro")])
                ]
                combat(player, random.choice(enemies))
            elif path == "2":
                combat(player, Enemy("Elite-Trainer", 75, [Card("Flammenwurf", 16, 0, "Feuer", 2)]))
            elif path == "3":
                print(f"🛒 Gold: {player.gold}")
                if input("Heiltrank (25 Gold)? j/n: ").lower() == 'j' and player.gold >= 25:
                    player.hp = min(player.max_hp, player.hp + 35)
                    player.gold -= 25
            elif path == "4":
                if random.random() < 0.6:
                    rare = random.choice(list(POKEMON_DB.keys()))
                    player.add_pokemon(get_pokemon(rare))
            elif path == "5":
                show_team(player)
            elif path == "6":
                save_game(player)
            elif path == "7":
                break

            player.check_evolutions()
            player.floor += 1
            if player.floor > 5:
                player.floor = 1
                player.region += 1

        if player.hp > 0 and player.region > 4:
            print("\n🎊 GRATULATION! Du hast die Liga besiegt!")
        else:
            print("\nGame Over...")

        if input("\nZurück zum Hauptmenü? (j/n): ").lower() != 'j':
            break

if __name__ == "__main__":
    main()
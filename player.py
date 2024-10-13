from minion import Minion
from spell import Spell
from deck import Deck
import random

class Player:
    """Represents a player in the game."""

    def __init__(self, name):
        self.name = name
        self.health = 30
        self.mana = 0
        self.mana_crystals = 0
        self.hand = []
        self.board = []
        self.deck = None

    def start_turn(self):
        """Starts a new turn for the player."""
        self.mana_crystals += 1
        if self.mana_crystals > 10:
            self.mana_crystals = 10
        self.mana = self.mana_crystals

        if len(self.hand) < 10:
            card = self.deck.draw_card()
            if card:
                self.hand.append(card)
                print(f"{self.name} drew {card.name}")
            else:
                print(f"{self.name}'s deck is empty!")

        print(f"{self.name} has {self.mana} mana for this turn.")

        for minion in self.board:
            minion.summoned_this_turn = False
        

    def draw_initial_hand(self):
        """Draws the player's initial hand of cards."""
        for _ in range(3):
            if len(self.hand) < 10:
                card = self.deck.draw_card()
                if card:
                    self.hand.append(card)
                    print(f"{self.name} drew {card.name} (Initial Hand)")
                else:
                    print(f"{self.name}'s deck is empty!")
    def display_player_view(self):
        """Displays the current player's hand and board."""
        print(f"\n{self.name}'s Hand:")
        for i, card in enumerate(self.hand):
            print(f"{i + 1}: {card.name}")

        print(f"\n{self.name}'s Board:")
        for i, minion in enumerate(self.board):
            print(f"{i + 1}: {minion}")

    def display_opponent_view(self):
        """Displays only the opponent's board (hides hand)."""
        print(f"\n{self.name}'s Board:")
        for i, minion in enumerate(self.board):
            print(f"{i + 1}: {minion}")

    def play_minion(self, card_index):
        """Plays a minion card from the player's hand."""
        if card_index < len(self.hand) and isinstance(self.hand[card_index], Minion):
            card = self.hand[card_index]
            if self.mana >= card.mana_cost:
                self.mana -= card.mana_cost
                card.summoned_this_turn = True
                self.board.append(card)
                self.hand.pop(card_index)
                print(f"{self.name} played {card.name}")
                print(f"{self.name} has {self.mana} mana left.")

                # Apply the minion's effect if it has one
                card.apply_effect(self)
            else:
                print(f"Not enough mana to play {card.name}!")
        else:
            print("Invalid minion card selection!")
            

    def play_spell(self, card_index, target=None, other_player=None):
        """Plays a spell card from the player's hand."""
        if card_index < len(self.hand) and isinstance(self.hand[card_index], Spell):
            spell = self.hand[card_index]
            if self.mana >= spell.mana_cost:
                self.mana -= spell.mana_cost
                self.hand.pop(card_index)
    
                # Handle various spells
                if spell.name == "Fireball":
                    self.cast_fireball(target, other_player)
                elif spell.name == "Polymorph":
                    self.cast_polymorph(target, other_player)
                elif spell.name == "Flamestrike":
                    self.cast_flamestrike(other_player)
                elif spell.name == "Holy Nova":
                    self.cast_holy_nova()
                elif spell.name == "Deadly Shot":
                    self.cast_deadly_shot(other_player)
                elif spell.name == "Cataclysm":
                    self.cast_cataclysm(other_player)
    
                print(f"{self.name} has {self.mana} mana left.")
            else:
                print(f"Not enough mana to cast {spell.name}!")
        else:
            print("Invalid spell card selection!")

    def cast_fireball(self, target, other_player):
        """Casts the Fireball spell on a target."""
        if isinstance(target, Minion):
            print(f"{self.name} casts Fireball on {target.name}, dealing 6 damage!")
            if target.take_damage(6):
                # Remove the target minion from the opponent's board if it dies
                target_index = other_player.board.index(target)
                other_player.board.pop(target_index)
        elif isinstance(target, Player):
            print(f"{self.name} casts Fireball on {target.name}, dealing 6 damage!")
            target.take_damage(6)
        else:
            print("Invalid target for Fireball!")
            
    def cast_polymorph(self, target, other_player):
        """Casts the Polymorph spell on a target minion."""
        if isinstance(target, Minion):
            print(f"{self.name} casts Polymorph on {target.name}, turning it into a 1/1 Sheep!")
            sheep = Minion("Sheep", 1, 1, 1, "A helpless sheep.")
            target_index = other_player.board.index(target)
            other_player.board[target_index] = sheep
        else:
            print("Polymorph can only target minions!")

    def cast_flamestrike(self, other_player):
        """Casts the Flamestrike spell."""
        print(f"{self.name} casts Flamestrike, dealing 5 damage to all enemy minions!")
        for minion in other_player.board:
            if minion.take_damage(5):
                other_player.board.remove(minion)

    def cast_holy_nova(self, other_player):
        """Casts the Holy Nova spell."""
        print(f"{self.name} casts Holy Nova, dealing 2 damage to all enemy minions and healing all friendly characters!")

        # Deal 2 damage to enemy minions
        for minion in other_player.board:
            if minion.take_damage(2):
                other_player.board.remove(minion)

        # Heal all friendly minions and hero
        self.health += 2
        print(f"{self.name} heals for 2 health, now at {self.health} health!")

        for minion in self.board:
            minion.health += 2
            print(f"{minion.name} heals for 2 health, now at {minion.name} health!")

    def cast_deadly_shot(self, other_player):
        """Casts the Deadly Shot spell."""
        if other_player.board:
            import random
            random_minion = random.choice(other_player.board)
            print(f"{self.name} casts Deadly Shot, destroying {random_minion.name}!")
            other_player.board.remove(random_minion)
        else:
            print("No enemy minions to target with Deadly Shot!")

    def cast_cataclysm(self, other_player):
        """Casts the Cataclysm spell."""
        print(f"{self.name} casts Cataclysm, destroying all minions and discarding 2 cards!")

        # Destroy all minions
        self.board.clear()
        other_player.board.clear()

        # Discard 2 cards if possible
        for _ in range(2):
            if self.hand:
                discarded_card = self.hand.pop(0)  # Discard the first two cards in hand
                print(f"{self.name} discards {discarded_card.name}")
            else:
                print("No cards left to discard.")

    def take_damage(self, damage):
        """Deals damage to the player and checks if they have lost."""
        self.health -= damage
        print(f"{self.name} takes {damage} damage, now at {self.health} health.")
        if self.health <= 0:
            print(f"{self.name} has lost the game!")

    def has_taunt(self):
        """Checks if any minion on the board has Taunt."""
        return any(minion.effect == "Taunt" for minion in self.board)

    def get_taunt_minion(self):
        """Returns the first minion with Taunt on the board."""
        return next((minion for minion in self.board if minion.effect == "Taunt"), None)

    def attack_with_minion(self, attacker_index, target, other_player):
        """Handles the minion's attack."""
        if attacker_index < len(self.board):
            attacker = self.board[attacker_index]

        # Check if minion was just summoned and can't attack unless it has Charge
        if attacker.summoned_this_turn and "Charge" not in attacker.effect:
            print(f"{attacker.name} cannot attack this turn because it was just played.")
            return

        # Check if opponent has Taunt minions and prioritize them
        if other_player.has_taunt():
            taunt_minion = other_player.get_taunt_minion()
            print(f"{self.name} must attack {taunt_minion.name} because it has Taunt!")
            target = taunt_minion

        # Check if target is a Stealth minion and prevent attack if Stealthed
        if isinstance(target, Minion) and "Stealth" in target.effect:
            print(f"{target.name} cannot be attacked while it has Stealth!")
            return

        # Handle attack logic
        if isinstance(target, Minion):
            print(f"{attacker.name} attacks {target.name}!")
            if target.take_damage(attacker.attack):
                # Remove target if it dies
                target_index = other_player.board.index(target)
                other_player.board.pop(target_index)
            if attacker.take_damage(target.attack):
                # Remove attacker if it dies
                self.board.pop(attacker_index)
            
            # If Stealth minion attacks, it loses Stealth
            if "Stealth" in attacker.effect:
                print(f"{attacker.name} loses Stealth after attacking!")
                attacker.effect.remove("Stealth")

        elif isinstance(target, Player):
            print(f"{attacker.name} attacks {target.name}!")
            target.take_damage(attacker.attack)

    def has_taunt(self):
        """Checks if any minion on the board has Taunt (ignores Stealthed Taunt minions)."""
        return any(minion.effect == "Taunt" and "Stealth" not in minion.effect for minion in self.board)
    

    def game_loop(self, other_player):
        """Handles the main game loop between two players."""
        current_player = self
        game_over = False

    # Both players draw initial hands
        self.draw_initial_hand()
        other_player.draw_initial_hand()
    
        while not game_over:
            print(f"\n{current_player.name}'s turn!")
            current_player.start_turn()

            turn_over = False
        while not turn_over:
            # Clear screen to simulate turn visibility
            print("\n" * 100)

            # Display only the current player's hand and board, and opponent's board
            current_player.display_player_view()
            other_player.display_opponent_view()

            print("\nChoose an action:")
            print("1: Play a minion")
            print("2: Play a spell")
            print("3: Attack with a minion")
            print("4: End turn")

            action = input("Enter the action number: ")

            if action == "1":
                card_index = int(input("Choose the minion to play (number in hand): ")) - 1
                current_player.play_minion(card_index)

            elif action == "2":
                card_index = int(input("Choose the spell to play (number in hand): ")) - 1
                spell_name = current_player.hand[card_index].name
                if spell_name == "Fireball":
                    target_type = input("Fireball target: (1) Minion or (2) Player: ")
                    if target_type == "1":
                        target_index = int(input("Choose the minion target (number on board): ")) - 1
                        target = other_player.board[target_index]
                    elif target_type == "2":
                        target = other_player
                    current_player.play_spell(card_index, target, other_player)

            elif action == "3":
                attacker_index = int(input("Choose the attacking minion (number on board): ")) - 1
                target_type = input("Attack target: (1) Minion or (2) Player: ")
                if target_type == "1":
                    target_index = int(input("Choose the minion target (number on board): ")) - 1
                    target = other_player.board[target_index]
                elif target_type == "2":
                    target = other_player
                current_player.attack_with_minion(attacker_index, target, other_player)

            elif action == "4":
                turn_over = True
            else:
                print("Invalid Input")

        if other_player.health <= 0:
            print(f"{other_player.name} has lost the game!")
            game_over = True

        # Switch turns
        current_player, other_player = other_player, current_player

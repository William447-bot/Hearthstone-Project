from minion import Minion
from spell import Spell
from deck import Deck
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 30
        self.mana = 0
        self.hand = []
        self.board = []
        self.deck = None

    def draw_initial_hand(self):
        """Draw an initial hand of 5 cards."""
        for _ in range(5):
            card = self.deck.draw_card()
            if card:
                self.hand.append(card)
        print(f"{self.name} draws their initial hand.")

    def start_turn(self):
        """Starts a new turn by drawing a card and updating mana."""
        # Increase mana each turn (to a max of 10)
        self.mana = min(self.mana + 1, 10)
        # Draw a card
        card = self.deck.draw_card()
        if card:
            self.hand.append(card)
        print(f"{self.name} starts their turn with {self.mana} mana and draws a card.")

    def display_player_view(self):
        """Displays the player's hand and board for their view."""
        print(f"{self.name}'s view:")
        print(f"Health: {self.health}, Mana: {self.mana}")
        print("Hand:")
        for idx, card in enumerate(self.hand):
            print(f"{idx + 1}: {card}")
        print("Board:")
        for idx, minion in enumerate(self.board):
            print(f"{idx + 1}: {minion}")

    def display_opponent_view(self):
        """Displays the opponent's board for the current player."""
        print("Opponent's Board:")
        for idx, minion in enumerate(self.board):
            print(f"{idx + 1}: {minion}")

    def play_minion(self, card_index):
        """Plays a minion from the hand to the board."""
        if card_index < 0 or card_index >= len(self.hand):
            print("Invalid card index.")
            return

        card = self.hand[card_index]
        if not isinstance(card, Minion):
            print("That is not a minion.")
            return

        if self.mana < card.mana_cost:
            print("Not enough mana to play this card.")
            return

        # Play the minion
        self.mana -= card.mana_cost
        self.board.append(card)
        self.hand.pop(card_index)
        print(f"{self.name} plays {card.name} on the board.")

        # Trigger minion's effect if any
        card.trigger_effect()

    def play_spell(self, card_index, target, other_player):
        """Plays a spell from the hand."""
        if card_index < 0 or card_index >= len(self.hand):
            print("Invalid card index.")
            return

        card = self.hand[card_index]
        if not isinstance(card, Spell):
            print("That is not a spell.")
            return

        if self.mana < card.mana_cost:
            print("Not enough mana to play this card.")
            return

        # Play the spell
        self.mana -= card.mana_cost
        print(f"{self.name} casts {card.name}.")
        card.cast(target)

        # Remove the spell from hand after casting
        self.hand.pop(card_index)

    def attack_with_minion(self, attacker_index, target, other_player):
        """Attacks with a minion on the board."""
        if attacker_index < 0 or attacker_index >= len(self.board):
            print("Invalid minion index.")
            return

        attacker = self.board[attacker_index]
        if attacker.summoned_this_turn:
            print(f"{attacker.name} cannot attack the turn it was summoned.")
            return

        if isinstance(target, Minion):
            print(f"{attacker.name} attacks {target.name}.")
            if target.take_damage(attacker.attack):
                # If target minion is destroyed, remove it from the board
                other_player.board.remove(target)
        elif isinstance(target, Player):
            print(f"{attacker.name} attacks {target.name} directly!")
            target.health -= attacker.attack
            if target.health <= 0:
                print(f"{target.name} has been defeated!")

        # After attacking, mark the minion as having attacked this turn
        attacker.summoned_this_turn = True

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
                    target_type = input("Target: (1) Minion or (2) Player: ")
                    if target_type == "1":
                        target_index = int(input("Choose the minion target (number on board): ")) - 1
                        target = other_player.board[target_index]
                    else:
                        target = other_player
                    current_player.play_spell(card_index, target, other_player)

                elif action == "3":
                    attacker_index = int(input("Choose the attacking minion (number on board): ")) - 1
                    target_type = input("Attack target: (1) Minion or (2) Player: ")
                    if target_type == "1":
                        target_index = int(input("Choose the minion target (number on board): ")) - 1
                        target = other_player.board[target_index]
                    else:
                        target = other_player
                    current_player.attack_with_minion(attacker_index, target, other_player)

                elif action == "4":
                    print("Ending turn")
                    turn_over = True
                else:
                    print("Invalid Input")

            if other_player.health <= 0:
                print(f"{other_player.name} has lost the game!")
                game_over = True

            # Switch turns
            current_player, other_player = other_player, current_player

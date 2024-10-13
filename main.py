from player import Player
from minion import Minion
from spell import Spell
from deck import Deck

class Main:
    """Main class to initialize and run the game."""
    
    def __init__(self):
        """Initialize the game with players, cards, and start the game loop."""
        # Create two players
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

        # Initialize decks for both players
        self.player1.deck = self.create_deck()
        self.player2.deck = self.create_deck()

        # Start the game loop
        self.start_game()

    def create_deck(self):
        """Creates a deck with a mix of minions and spells."""
        # Create a list of minion cards
        minions = [
            Minion("Stormwind Champion", 6, 6, 7, "Gives +1/+1 to all other minions"),
            Minion("Boulderfist Ogre", 6, 6, 7, "A tough ogre"),
            Minion("Chillwind Yeti", 4, 4, 5, "A standard minion"),
            Minion("Argent Protector", 2, 2, 2, "Gives a minion Divine Shield"),
            Minion("Bloodfen Raptor", 2, 3, 2, "A basic minion")
        ]

        # Create a list of spell cards
        Spells = [
            Spell("Fireball", 4, "Deal 6 damage"),
            Spell("Polymorph", 4, "Transform a minion into a 1/1 Sheep"),
            Spell("Flamestrike", 7, "Deal 5 damage to all enemy minions"),
            Spell("Holy Nova", 5, "Deal 2 damage to all enemies and heal allies"),
            Spell("Deadly Shot", 3, "Destroy a random enemy minion"),
            Spell("Cataclysm", 6, "Destroy all minions and discard 2 cards")
        ]

        # Combine minions and spells into the deck
        deck = Deck(minions + spells)

        return deck

    def start_game(self):
        """Start the game by initializing player hands and running the game loop."""
        print("Starting the game...")

        # Both players draw their initial hands
        self.player1.draw_initial_hand()
        self.player2.draw_initial_hand()

        # Start the game loop
        self.player1.game_loop(self.player2)

# Run the game
if __name__ == "__main__":
    main_game = Main()


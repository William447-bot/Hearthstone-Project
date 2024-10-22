class Minion:
    def __init__(self, name, attack, health, mana_cost, description, apply_effect=None):
        """
        Initializes a Minion with a name, attack, health, mana cost, and description.
        Optionally, the minion can have an effect when played or under specific conditions.
        """
        self.name = name
        self.attack = attack
        self.health = health
        self.mana_cost = mana_cost
        self.description = description
        self.summoned_this_turn = False  # Tracks if the minion was summoned this turn
        self.apply_effect = apply_effect  # New attribute to store any special effect or ability

    def __str__(self):
        return f"{self.name} ({self.attack}/{self.health})"

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} has been destroyed!")
            return True
        return False

    def trigger_effect(self, target=None):
        """
        Triggers the minion's effect if it has one.
        """
        if self.apply_effect:
            print(f"{self.name} applies its effect: {self.apply_effect}")
            if callable(self.apply_effect):
                self.apply_effect(target)  # Execute the effect if it's a function

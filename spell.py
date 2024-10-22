class Spell:
    def __init__(self, name, mana_cost, effect):
        """Initialize a spell with a name, mana cost, and effect."""
        self.name = name
        self.mana_cost = mana_cost
        self.effect = effect

    def cast(self, target=None):
        """Simulate casting the spell."""
        if target:
            print(f"{self.name} is cast on {target}, causing: {self.effect}")
        else:
            print(f"{self.name} is cast, causing: {self.effect}")

    def __str__(self):
        """Return the string representation of the spell."""
        return f"Spell: {self.name}, Mana Cost: {self.mana_cost}, Effect: {self.effect}"

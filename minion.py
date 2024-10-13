class Minion:
    def __init__(self, name, attack, health, mana_cost, description):
        self.name = name
        self.attack = attack
        self.health = health
        self.mana_cost = mana_cost
        self.description = description
        self.summoned_this_turn = False  # New attribute

    def __str__(self):
        return f"{self.name} ({self.attack}/{self.health})"

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} has been destroyed!")
            return True
        return False

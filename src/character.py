class Character:

    def __init__(self, name: str, health: int = 10):
     
        self.name = name
        self.health = health
        self.is_alive = True
        self._check_status() # Initial check for death if health is 0 or less

    def _check_status(self):
       
        if self.health <= 0:
            self.health = 0 # Health cannot go below 0
            self.is_alive = False
            print(f"{self.name} est tombé à 0 HP et est mort.")

    def take_damage(self, damage: int):
    
        if self.is_alive:
            self.health -= damage
            print(f"{self.name} subit {damage} dégâts. HP restants : {self.health}")
            self._check_status()
        else:
            print(f"{self.name} est déjà mort et ne peut plus subir de dégâts.")

    def attack(self, target: 'Character'):
        
        if self.is_alive:
            if target.is_alive:
                print(f"{self.name} attaque {target.name} !")
                target.take_damage(1)
            else:
                print(f"{target.name} est déjà mort. {self.name} ne peut pas attaquer un cadavre.")
        else:
            print(f"{self.name} est mort et ne peut pas attaquer.")

    def __str__(self):
        return f"{self.name} (HP: {self.health}, Vivant: {self.is_alive})"


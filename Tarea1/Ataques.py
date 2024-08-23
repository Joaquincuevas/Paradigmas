class Attack:
    def __init__(
        self,
        name: str,
        attack_type: str,
        objective: str,
        damage: int,
        precision: int,
        recharge: int,
    ):
        self.name = name
        self.type = attack_type
        self.objective = objective
        self.damage = damage
        self.precision = precision
        self.recharge = recharge
        self.cooldown = 0

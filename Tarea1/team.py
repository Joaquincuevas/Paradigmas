from random import randint

from attack import Attack
from opponent import Opponent
from robot import Robot


class Team(Opponent):
    def __init__(
        self, name, teammates: list[Robot], current_robot: Robot | None = None
    ) -> None:
        self.teammates = teammates
        self.current_robot: Robot = teammates[0] if not current_robot else current_robot
        self.current_index: int = 0
        super().__init__(name)

    def __repr__(self) -> str:
        return super().__repr__()

    def swap_current_robot(self):
        # Avanza el índice al siguiente robot en la lista
        self.current_index = (self.current_index + 1) % len(self.teammates)
        self.current_robot = self.teammates[self.current_index]

        return self.current_robot

    def _select_attack(self):
        attack = self.current_robot._select_attack()
        return attack

    def do_attack_to(self, opp):
        attack = self._select_attack()
        self.turn_count += 1

        if attack and randint(1, 100) <= attack.precision:
            # Apply damage
            # TODO: Apply skill effects here (e.g., shields, steroids)
            opp.receive_damage(attack.damage)

            attack._cooldown = attack.recharge

        elif attack:
            # Set attack cooldown
            attack._cooldown = attack.recharge
        self.swap_current_robot()

    def get_attacks(self) -> list[Attack]:
        attacks = []
        for robot in self.teammates:
            attacks = attacks + (robot.get_attacks())
        return attacks

    def receive_damage(self, damage: int):
        self.current_robot.receive_damage(damage)

    def is_defeated(self) -> bool:
        for robot in self.teammates:
            if robot.is_defeated():
                return True
        return False

    def activate_skills(self, trigger: str, value: int | None = None):
        self.current_robot.activate_skills(trigger, value)

    def update_skill_durations(self):
        self.current_robot.update_skill_durations()

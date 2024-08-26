from abc import ABC, abstractmethod
from random import choice, randint

from attack import Attack
from skill import Skill


class Opponent(ABC):
    def __init__(self, name) -> None:
        self.name = name
        self.turn_count = 0

    @abstractmethod
    def __repr__(self) -> str:
        return self.name

    @abstractmethod
    def _select_attack(self) -> None: ...

    @abstractmethod
    def do_attack_to(self, opp) -> None: ...

    @abstractmethod
    def get_attacks(self) -> list[Attack]: ...

    @abstractmethod
    def receive_damage(self, damage: int) -> None: ...

    @abstractmethod
    def is_defeated(self) -> bool: ...

    @abstractmethod
    def activate_skills(self, trigger: str, value: int | None = None) -> None: ...

    @abstractmethod
    def update_skill_durations(self) -> None: ...


class Robot(Opponent):
    def __init__(
        self, name: str, energy: int, attacks: list[Attack], skills: list[Skill]
    ):
        self.max_energy = energy
        self.current_energy = energy
        self.attacks = attacks
        self.skills = skills
        super().__init__(name)

    def __repr__(self) -> str:
        return super().__repr__()

    def get_attacks(self):
        return self.attacks

    def _select_attack(self) -> Attack | None:
        available_attacks = [attack for attack in self.attacks if attack._cooldown == 0]
        if not available_attacks:
            return None
        attack = choice(available_attacks)
        attack.add_use()

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

    def receive_damage(self, damage: int):
        # Activate defensive skills
        self.activate_skills("energy")
        self.current_energy = max(0, self.current_energy - damage)

    def is_defeated(self) -> bool:
        return self.current_energy <= 0

    # TODO: Implement other skill triggers
    def activate_skills(self, trigger: str, value: int | None = None):
        for skill in self.skills:
            if skill.trigger == trigger:
                if trigger == "energy" and self.current_energy <= skill.trigger_value:
                    skill.active = True
                    skill.remaining_duration = skill.duration
                elif trigger == "turns" and value == skill.trigger_value:
                    skill.active = True
                    skill.remaining_duration = skill.duration

    def update_skill_durations(self):
        for skill in self.skills:
            if skill.active:
                skill.remaining_duration -= 1
                if skill.remaining_duration == 0:
                    skill.active = False


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
        self.current_robot._select_attack()
        self.swap_current_robot()

    def do_attack_to(self, opp):
        attack = self._select_attack()

        if attack and randint(1, 100) <= attack.precision:
            # Apply damage
            # TODO: Apply skill effects here (e.g., shields, steroids)
            opp.receive_damage(attack.damage)

            attack.cooldown = attack.recharge

        elif attack:
            # Set attack cooldown
            attack.cooldown = attack.recharge
        self.swap_current_robot()

    def get_attacks(self) -> list[Attack]:
        attacks = self.current_robot.get_attacks()
        self.swap_current_robot()
        return attacks

    def receive_damage(self, damage: int):
        self.current_robot.receive_damage(damage)

    def is_defeated(self) -> bool:
        return all(map(lambda robot: robot.is_defeated(), self.teammates))

    def activate_skills(self, trigger: str, value: int | None = None):
        self.current_robot.activate_skills(trigger, value)

    def update_skill_durations(self):
        self.current_robot.update_skill_durations()

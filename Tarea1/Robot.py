from abc import abstractmethod
from attack import Attack
from typing import List
from skill import Skill
import random


class Opponent:
    def __init__(self, name) -> None:
        self.name = name

    @abstractmethod
    def select_attack(self): ...

    @abstractmethod
    def get_attacks(self) -> list[Attack]: ...

    @abstractmethod
    def receive_damage(self, damage: int): ...

    @abstractmethod
    def is_defeated(self) -> bool: ...

    @abstractmethod
    def activate_skills(self, trigger: str, value: int | None = None): ...

    @abstractmethod
    def update_skill_durations(self): ...

    @abstractmethod
    def reset_for_battle(self): ...


class Robot(Opponent):
    def __init__(
        self, name: str, energy: int, attacks: List[Attack], skills: List[Skill]
    ):
        self.max_energy = energy
        self.current_energy = energy
        self.attacks = attacks
        self.skills = skills
        super().__init__(name)

    def get_attacks(self):
        return self.attacks

    def select_attack(self) -> Attack | None:
        available_attacks = [attack for attack in self.attacks if attack.cooldown == 0]
        if not available_attacks:
            return None
        return random.choice(available_attacks)

    def receive_damage(self, damage: int):
        self.current_energy = max(0, self.current_energy - damage)

    def is_defeated(self) -> bool:
        return self.current_energy <= 0

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

    def reset_for_battle(self):
        self.current_energy = self.max_energy
        for attack in self.attacks:
            attack.cooldown = 0
        for skill in self.skills:
            skill.active = False
            skill.remaining_duration = 0


class Team(Opponent):
    def __init__(self, name, teammates: list[Robot]) -> None:
        self.teammates = teammates
        super().__init__(name)

    def select_attack(self): ...

    def get_attacks(self) -> list[Attack]: ...

    def receive_damage(self, damage: int): ...

    def is_defeated(self) -> bool: ...

    def activate_skills(self, trigger: str, value: int | None = None): ...

    def update_skill_durations(self): ...

    def reset_for_battle(self): ...

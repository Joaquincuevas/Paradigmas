from attack import Attack
from typing import List
from skill import Skill
import random


class Robot:
    def __init__(
        self, name: str, energy: int, attacks: List[Attack], skills: List[Skill]
    ):
        self.name = name
        self.max_energy = energy
        self.current_energy = energy
        self.attacks = attacks
        self.skills = skills

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

import random

from attack import Attack
from robot import Robot


class Battle:
    def __init__(self, robot1: Robot, robot2: Robot):
        self.robot1 = robot1
        self.robot2 = robot2
        self.turn_count = 0

    def conduct_battle(self):
        self.robot1.reset_for_battle()
        self.robot2.reset_for_battle()

        current_attacker, current_defender = self.robot1, self.robot2

        while not self.robot1.is_defeated() and not self.robot2.is_defeated():
            self.turn_count += 1

            # Activate turn-based skills
            current_attacker.activate_skills("turns", self.turn_count)

            attack = current_attacker.select_attack()
            if attack:
                self.perform_attack(current_attacker, current_defender, attack)

            # Update skill durations and cooldowns
            current_attacker.update_skill_durations()
            for attack in current_attacker.attacks:
                if attack.cooldown > 0:
                    attack.cooldown -= 1

            # Switch roles
            current_attacker, current_defender = current_defender, current_attacker

        winner = self.robot1 if self.robot2.is_defeated() else self.robot2
        return winner, self.turn_count

    def perform_attack(self, attacker: Robot, defender: Robot, attack: Attack):
        # Check if attack hits
        if random.randint(1, 100) <= attack.precision:
            # Apply damage
            damage = attack.damage
            # TODO: Apply skill effects here (e.g., shields, steroids)
            defender.receive_damage(damage)

            # Activate defensive skills
            defender.activate_skills("energy")
            # TODO: Implement other skill triggers

        # Set attack cooldown
        attack.cooldown = attack.recharge

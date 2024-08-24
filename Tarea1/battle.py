import random

from attack import Attack
from robot import Opponent


class Battle:
    def __init__(self, opp1: Opponent, opp2: Opponent) -> None:
        self.opp1 = opp1
        self.opp2 = opp2
        self.turn_count = 0

    def conduct_battle(self):
        self.opp1.reset_for_battle()
        self.opp2.reset_for_battle()

        current_attacker, current_defender = self.opp1, self.opp2

        while not self.opp1.is_defeated() and not self.opp2.is_defeated():
            self.turn_count += 1

            # Activate turn-based skills
            current_attacker.activate_skills("turns", self.turn_count)

            attack = current_attacker.select_attack()
            if attack:
                self.perform_attack(current_attacker, current_defender, attack)

            # Update skill durations and cooldowns
            current_attacker.update_skill_durations()
            for attack in current_attacker.get_attacks():
                if attack.cooldown > 0:
                    attack.cooldown -= 1

            # Switch roles
            current_attacker, current_defender = current_defender, current_attacker

        winner = self.opp1 if self.opp2.is_defeated() else self.opp2
        return winner, self.turn_count

    def perform_attack(self, attacker: Opponent, defender: Opponent, attack: Attack):
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

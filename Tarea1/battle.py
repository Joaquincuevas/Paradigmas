from robot import Opponent


class Battle:
    def __init__(self, opp1: Opponent, opp2: Opponent) -> None:
        self.opp1 = opp1
        self.opp2 = opp2
        self.turn_count = 0

    def conduct_battle(self):
        self.opp1.reset_for_battle()
        self.opp2.reset_for_battle()

        attacker, defender = self.opp1, self.opp2

        while not self.opp1.is_defeated() and not self.opp2.is_defeated():
            self.turn_count += 1

            # Activate turn-based skills
            attacker.activate_skills("turns", self.turn_count)

            attacker.do_attack_to(defender)

            # Update skill durations and cooldowns
            attacker.update_skill_durations()
            for attack in attacker.get_attacks():
                if attack.cooldown > 0:
                    attack.cooldown -= 1

            # Switch roles
            attacker, defender = defender, attacker

        winner = self.opp1 if self.opp2.is_defeated() else self.opp2
        return winner, self.turn_count

from copy import deepcopy
from random import shuffle

from robot import Opponent


class Battle:
    """Gestiona una batalla entre dos oponentes."""

    def __init__(self, opponents: tuple[Opponent, Opponent] | list[Opponent]) -> None:
        """Inicializa la batalla con dos oponentes."""
        self.opponents = deepcopy(opponents)
        self.turn_count = 0

    def _draw(self):
        "Elige quien comienza atacando y defendiendo al azar"
        self.opponents = list(self.opponents)
        shuffle(self.opponents)
        self.attacker, self.defender = self.opponents

    def play(self):
        """Ejecuta la batalla hasta que haya un ganador."""
        self._draw()

        while True:
            self.turn_count += 1
            # self._activate_turn_based_skills()
            self.attacker.do_attack_to(
                self.defender
            )  # Se cuenta un turno cada vez que ataca

            if self.defender.is_defeated():
                winner, loser = self.attacker, self.defender
                print(f"El Ganador es {winner}\n")
                break

            self._update_after_turn()
            self._switch_roles()

        self.log = {"winner": winner, "loser": loser}
        return winner, self.turn_count

    # def _activate_turn_based_skills(self):
    #     """Activa habilidades basadas en el turno actual."""
    #     self.attacker.activate_skills("turns", self.turn_count)

    def _update_after_turn(self):
        """Actualiza habilidades y cooldowns después del turno."""
        # self.attacker.update_skill_durations()
        for attack in self.attacker.get_attacks():
            attack._cooldown = max(0, attack._cooldown - 1)

    def _switch_roles(self):
        """Intercambia los roles de atacante y defensor."""
        self.attacker, self.defender = self.defender, self.attacker

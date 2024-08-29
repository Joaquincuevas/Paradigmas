from random import choice, randint

from attack import Attack
from opponent import Opponent
from skill import Skill


class Robot(Opponent):
    def __init__(
        self,
        name: str,
        energy: int,
        attacks: list[Attack],
    ):
        self.max_energy = energy
        self.current_energy = energy
        self.attacks = attacks
        # self.skills = skills
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

    def do_attack_to(self, opp: "Robot"):
        attack = self._select_attack()
        self.turn_count += 1

        if attack and randint(1, 100) <= attack.precision:
            # Apply damage
            # TODO: Apply skill effects here (e.g., shields, steroids)
            opp.receive_damage(attack.damage)

            attack._cooldown = attack.recharge
            print(
                f"{self.name} atacó a {opp.name} con {attack.name} e hizo {attack.damage}pt de daño a {opp.name} le quedán {opp.current_energy}pt de energía"
            )

        elif attack:
            # Set attack cooldown
            attack._cooldown = attack.recharge
            print(f"{self.name} atacó a {opp.name} con {attack.name} pero falló")
        else:
            print(f"{self.name} no tiene ataques disponibles")

    def receive_damage(self, damage: int):
        # Activate defensive skills
        # self.activate_skills("energy")
        self.current_energy = max(0, self.current_energy - damage)

    def is_defeated(self) -> bool:
        return self.current_energy <= 0

    # TODO: Implement other skill triggers
    # def activate_skills(self, trigger: str, value: int | None = None):
    #     for skill in self.skills:
    #         if skill.trigger == trigger:
    #             if trigger == "energy" and self.current_energy <= skill.trigger_value:
    #                 skill.active = True
    #                 skill.remaining_duration = skill.duration
    #             elif trigger == "turns" and value == skill.trigger_value:
    #                 skill.active = True
    #                 skill.remaining_duration = skill.duration

    # def update_skill_durations(self):
    #     for skill in self.skills:
    #         if skill.active:
    #             skill.remaining_duration -= 1
    #             if skill.remaining_duration == 0:
    #                 skill.active = False

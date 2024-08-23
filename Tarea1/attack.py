from typing import Literal
from pydantic import BaseModel, conint


class Attack(BaseModel):
    """Represent an attack in game

    Example:
        Attack(
                        name="Flame Thrower",
                        type="long",
                        objetive="robot",
                        damage=30,
                        precision=80,
                        recharge=1,
                    )
    Attributes:
        name: The name of the attack.
        type : The type of attack, either ranged ("long"), direct weapon attack ("sword"), or hand-to-hand combat ("hand").
        objective : The target of the attack, which can be a single robot ("robot") or the entire opposing team ("team").
        damage : The amount of damage the attack inflicts, represented as an integer greater than 0. This damage reduces the energy of the target.
        precision : The accuracy of the attack, represented as a percentage between 10 and 100. It indicates how often the attack hits its target.
        recharge : The number of turns required before the attack can be used again. A value of 0 means the attack can be used every turn, while a higher value indicates the number of turns to wait.
    """

    name: str
    type: Literal["long", "sword", "hand"]
    objetive: Literal["robot", "team"]
    damage: conint(gt=0)  # type: ignore
    precision: conint(gt=10, lt=100)  # type: ignore
    recharge: conint(ge=0)  # type: ignore
    cooldown: int = 0

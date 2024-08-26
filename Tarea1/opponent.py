from abc import ABC, abstractmethod
from attack import Attack


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

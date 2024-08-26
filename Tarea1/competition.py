from abc import ABC, abstractmethod
from itertools import combinations

from opponent import Opponent
from report import Report
from robot import Robot
from team import Team


class Competition(ABC):
    def __init__(self, robots: list[Robot] | list[Team] | list[Team | Robot]) -> None:
        self.robots = robots
        self.report: Report = Report()

    @property
    @abstractmethod
    def draw(self) -> list[tuple[Opponent, Opponent]]:
        return list(combinations(self.robots, 2))


class Playoff(Competition):
    # TODO: PROXIMA ENTREGA
    ...


class Tournament(Competition):
    # TODO: PROXIMA ENTREGA
    ...

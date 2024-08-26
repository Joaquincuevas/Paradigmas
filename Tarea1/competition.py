from abc import ABC, abstractmethod
from itertools import combinations

from battle import Battle
from report import Report
from robot import Opponent, Robot, Team


class Competition(ABC):
    def __init__(self, robots: list[Robot] | list[Team] | list[Team | Robot]) -> None:
        self.robots = robots
        self.report: Report = Report()

    @property
    @abstractmethod
    def draw(self) -> list[tuple[Opponent, Opponent]]:
        return list(combinations(self.robots, 2))


class League(Competition):
    def __init__(self, robots: list[Robot] | list[Team] | list[Team | Robot]) -> None:
        super().__init__(robots)

    @property
    def draw(self) -> list[tuple[Opponent, Opponent]]:
        return super().draw

    def play(self):
        for match in self.draw:
            battle = Battle(match)
            battle.play()
            self.report.battles_log.append(battle.log)


class Playoff(Competition):
    # TODO: PROXIMA ENTREGA
    ...


class Tournament(Competition):
    # TODO: PROXIMA ENTREGA
    ...

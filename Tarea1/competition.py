from abc import abstractmethod
from collections import defaultdict

from battle import Battle
from robot import Robot


class Competition:
    def __init__(self, robots: list[Robot]) -> None:
        self.robots = robots
        self.results = defaultdict(lambda: {"wins": 0, "losses": 0, "total_turns": 0})

    @abstractmethod
    def conduct_competition(self): ...

    @abstractmethod
    def get_league_standings(self): ...


class League(Competition):
    def __init__(self, robots: list[Robot]) -> None:
        super().__init__(robots)

    def conduct_competition(self):
        for i, robot1 in enumerate(self.robots):
            for robot2 in self.robots[i + 1 :]:
                battle = Battle(robot1, robot2)
                winner, turns = battle.conduct_battle()

                loser = robot2 if winner == robot1 else robot1

                self.results[winner.name]["wins"] += 1
                self.results[winner.name]["total_turns"] += turns
                self.results[loser.name]["losses"] += 1
                self.results[loser.name]["total_turns"] += turns

        return self.get_league_standings()

    def get_league_standings(self):
        standings = sorted(
            self.results.items(),
            key=lambda x: (x[1]["wins"], -x[1]["losses"]),
            reverse=True,
        )
        return standings


class Playoff(Competition):
    # TODO: PROXIMA ENTREGA
    ...


class Torneo(Competition):
    # TODO: PROXIMA ENTREGA
    ...

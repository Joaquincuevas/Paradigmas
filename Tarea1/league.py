from competition import Competition
from robot import Robot
from team import Team
from opponent import Opponent
from battle import Battle


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

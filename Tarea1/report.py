import matplotlib.pyplot as plt

from robot import Opponent


class Report:
    def __init__(self) -> None:
        self.battles_log: list[dict[str, Opponent]] = []

    def _initialize_opponent_stats(self, opponent: Opponent) -> dict:
        return {
            "wins": 0,
            "loss": 0,
            "turns": opponent.turn_count,
            "attacks": {
                attack.name: attack._usage for attack in opponent.get_attacks()
            },
        }

    def _update_opponent_stats(
        self, results: dict, opponent: Opponent, is_winner: bool
    ) -> None:
        if opponent.name not in results:
            results[opponent.name] = self._initialize_opponent_stats(opponent)

        results[opponent.name]["wins" if is_winner else "loss"] += 1
        results[opponent.name]["turns"] += opponent.turn_count
        for attack in opponent.get_attacks():
            results[opponent.name]["attacks"][attack.name] += attack._usage

    @property
    def results(self):
        results = {}
        for battle in self.battles_log:
            self._update_opponent_stats(results, battle["winner"], is_winner=True)
            self._update_opponent_stats(results, battle["loser"], is_winner=False)
        return results

    def plot(self):
        for opp, results in self.results.items():
            x = results["attacks"].keys()
            y = results["attacks"].values()
            _fig, ax = plt.subplots()
            ax.bar(x=x, height=y)
            plt.title(opp)
            plt.show()

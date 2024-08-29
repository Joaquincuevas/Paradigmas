import csv

import matplotlib.pyplot as plt

from opponent import Opponent


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

    @property
    def leaderboard(self):
        leaderboard = sorted(
            self.results.items(),
            key=lambda x: (-x[1]["wins"], x[1]["loss"], x[1]["turns"]),
        )
        n = 0
        for opp1, opp2 in zip(leaderboard, leaderboard[1:]):
            if opp1[1]["wins"] == opp2[1]["wins"]:
                for battle in self.battles_log:
                    if opp1[0] in [opp.name for opp in battle.values()] and opp2[0] in [
                        opp.name for opp in battle.values()
                    ]:
                        if battle["loser"].name == opp1[0]:
                            leaderboard[n + 1] = opp1
                            leaderboard[n] = opp2
            n += 1

        return leaderboard

    def plot(self):
        for opp, results in self.results.items():
            x = results["attacks"].keys()
            y = results["attacks"].values()
            _fig, ax = plt.subplots()
            ax.bar(x=x, height=y)
            plt.title(opp)
            plt.show()

    def show_leaderboard(self):
        sorted_teams = self.leaderboard
        # Crear la tabla de clasificación

        header = "{:^15} {:^15} {:^10} {:^10} {:^10}".format(
            "Posición", "Participante", "Victorias", "Derrotas", "Turnos"
        )

        print("-" * len(header))
        print(header)
        print("-" * len(header))

        for idx, (team, data) in enumerate(sorted_teams, start=1):
            print(
                "{:^15} {:^15} {:^10} {:^10} {:^10}".format(
                    idx, team, data["wins"], data["loss"], data["turns"]
                )
            )

    def export_leaderboard(self, filename="leaderboard.csv"):
        # Ordenar los equipos por victorias, luego por derrotas y finalmente por turnos
        leaderboard = self.leaderboard
        # Escribir la tabla en un archivo CSV
        with open(filename, mode="w", newline="", encoding="UTF-8") as file:
            writer = csv.writer(file)

            # Escribir la cabecera
            writer.writerow(["Posición", "Equipo", "Victorias", "Derrotas", "Turnos"])

            # Escribir los datos de cada equipo
            for idx, (team, data) in enumerate(leaderboard, start=1):
                writer.writerow([idx, team, data["wins"], data["loss"], data["turns"]])

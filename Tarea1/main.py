from league import League
from DataJSON import load_file, load_opponents


def main():
    data_file = load_file("./robots.json")
    opponents = load_opponents(data_file)
    league = League(opponents)
    league.play()
    league.report.show_leaderboard()
    league.report.export_leaderboard()
    league.report.plot()


if __name__ == "__main__":
    main()

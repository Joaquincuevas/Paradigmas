from league import League
from DataJSON import load_file, load_opponents


def menu(league: League):
    print("¿Desea activar el reporte de taba de victorias/derrotas? (si|no)")
    while True:
        ans = input(">>>")
        if ans == "si":
            league.report.export_leaderboard()
            break
        elif ans == "no":
            break
        else:
            print("ingrese respuesta valida")
    print(
        "¿Desea activar el reporte de graficos con la cantidad de usos de cada ataque? (si|no)"
    )
    ans = input(">>>")
    while True:
        if ans == "si":
            league.report.plot()
            break
        elif ans == "no":
            break
        else:
            print("ingrese respuesta valida")


def main():
    data_file = load_file("./robots01.json")
    opponents = load_opponents(data_file)
    league = League(opponents)
    league.play()
    league.report.show_leaderboard()
    menu(league)


if __name__ == "__main__":
    main()

from Ataques import Attack
from Habilidades import Skill
from Robot import Robot
from Competicion import League


def create_sample_robots():
    # Create sample robots with attacks and skills
    # This is a simplified version, you'd typically load this from a JSON file
    robot1 = Robot(
        "FireBot",
        100,
        [Attack("Flame Thrower", "long", "robot", 30, 80, 1)],
        [Skill("Heat Shield", "energy", 30, 2, "robot", "shield", 20)],
    )

    robot2 = Robot(
        "WaterBot",
        120,
        [Attack("Water Cannon", "long", "robot", 25, 90, 0)],
        [Skill("Steam Boost", "turns", 3, 1, "robot", "steroids", 30)],
    )

    return [robot1, robot2]


def main():
    robots = create_sample_robots()
    league = League(robots)
    standings = league.conduct_league()

    print("League Results:")
    for rank, (name, results) in enumerate(standings, 1):
        print(
            f"{rank}. {name}: Wins: {results['wins']}, Losses: {results['losses']}, Total Turns: {results['total_turns']}"
        )


if __name__ == "__main__":
    main()

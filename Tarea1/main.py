from attack import Attack
from competition import League
from robot import Robot
from skill import Skill


def create_sample_robots() -> list[Robot]:
    # Create sample robots with attacks and skills
    # This is a simplified version, you'd typically load this from a JSON file
    robot1 = Robot(
        "FireBot",
        100,
        [
            Attack(
                name="Flame Thrower",
                type="long",
                objetive="robot",
                damage=30,
                precision=80,
                recharge=1,
            )
        ],
        [Skill("Heat Shield", "energy", 30, 2, "robot", "shield", 20)],
    )

    robot2 = Robot(
        "WaterBot",
        120,
        [
            Attack(
                name="Water Cannon",
                type="long",
                objetive="robot",
                damage=25,
                precision=90,
                recharge=0,
            )
        ],
        [Skill("Steam Boost", "turns", 3, 1, "robot", "steroids", 30)],
    )

    return [robot1, robot2]


def main():
    robots = create_sample_robots()
    league = League(robots)
    standings = league.conduct_competition()

    print("League Results:")
    for rank, (name, results) in enumerate(standings, 1):
        print(
            f"{rank}. {name}: Wins: {results['wins']}, Losses: {results['losses']}, Total Turns: {results['total_turns']}"
        )


if __name__ == "__main__":
    main()

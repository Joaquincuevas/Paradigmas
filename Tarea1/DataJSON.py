import json
from robot import Robot
from robot import Team
from attack import Attack
from skill import Skill


class Tournament:
    def __init__(self):
        self.robots = []
        self.teams = []

    def load_robots(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
            robots = {}

            # Cargar robots
            for mr in data["robots"]:
                robot = Robot(mr["name"], mr["energy"])
                robots[mr["name"]] = robot

                # Cargar ataques
                for at in mr["attacks"]:
                    attack = Attack(
                        at["name"],
                        at["type"],
                        at["objective"],
                        at["damage"],
                        at["precision"],
                        at["recharge"],
                    )
                    robot.add_attack(attack)

                # Cargar habilidades
                for sk in mr["skills"]:
                    skill = Skill(
                        sk["name"],
                        sk["trigger"],
                        sk["trigger_value"],
                        sk["duration"],
                        sk["objective"],
                        sk["effect"],
                        sk["effect_value"],
                    )
                    robot.add_skill(skill)

                self.robots.append(robot)

            return robots  # Retorna el diccionario de robots

    def load_teams(self, filename, robots):
        with open(filename, "r") as f:
            data = json.load(f)
            teams = {}

            # Cargar equipos
            for team_data in data["teams"]:
                team = Team(team_data["name"])

                # Añadir robots al equipo
                for robot_data in team_data["robots"]:
                    robot_name = robot_data["name"]
                    if robot_name in robots:
                        team.add_robot(robots[robot_name])

                self.teams.append(team)
                teams[team_data["name"]] = team

            return teams  # Retorna el diccionario de equipos

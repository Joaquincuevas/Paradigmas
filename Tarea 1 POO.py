from typing import List, Dict
import random
from collections import defaultdict

class Attack:
    def __init__(self, name: str, attack_type: str, objective: str, damage: int, precision: int, recharge: int):
        self.name = name
        self.type = attack_type
        self.objective = objective
        self.damage = damage
        self.precision = precision
        self.recharge = recharge
        self.cooldown = 0

#----------------------------------------------------------------------------------------------------------------------------

class Skill:
    def __init__(self, name: str, trigger: str, trigger_value: int, duration: int, objective: str, effect: str, effect_value: int):
        self.name = name
        self.trigger = trigger
        self.trigger_value = trigger_value
        self.duration = duration
        self.objective = objective
        self.effect = effect
        self.effect_value = effect_value
        self.active = False
        self.remaining_duration = 0

#----------------------------------------------------------------------------------------------------------------------------

class Robot:
    def __init__(self, name: str, energy: int, attacks: List[Attack], skills: List[Skill]):
        self.name = name
        self.max_energy = energy
        self.current_energy = energy
        self.attacks = attacks
        self.skills = skills

    def select_attack(self) -> Attack:
        available_attacks = [attack for attack in self.attacks if attack.cooldown == 0]
        if not available_attacks:
            return None
        return random.choice(available_attacks)

    def receive_damage(self, damage: int):
        self.current_energy = max(0, self.current_energy - damage)

    def is_defeated(self) -> bool:
        return self.current_energy <= 0

    def activate_skills(self, trigger: str, value: int = None):
        for skill in self.skills:
            if skill.trigger == trigger:
                if trigger == "energy" and self.current_energy <= skill.trigger_value:
                    skill.active = True
                    skill.remaining_duration = skill.duration
                elif trigger == "turns" and value == skill.trigger_value:
                    skill.active = True
                    skill.remaining_duration = skill.duration

    def update_skill_durations(self):
        for skill in self.skills:
            if skill.active:
                skill.remaining_duration -= 1
                if skill.remaining_duration == 0:
                    skill.active = False

    def reset_for_battle(self):
        self.current_energy = self.max_energy
        for attack in self.attacks:
            attack.cooldown = 0
        for skill in self.skills:
            skill.active = False
            skill.remaining_duration = 0

#----------------------------------------------------------------------------------------------------------------------------

class Battle:
    def __init__(self, robot1: Robot, robot2: Robot):
        self.robot1 = robot1
        self.robot2 = robot2
        self.turn_count = 0

    def conduct_battle(self):
        self.robot1.reset_for_battle()
        self.robot2.reset_for_battle()
        
        current_attacker, current_defender = self.robot1, self.robot2
        
        while not self.robot1.is_defeated() and not self.robot2.is_defeated():
            self.turn_count += 1
            
            # Activate turn-based skills
            current_attacker.activate_skills("turns", self.turn_count)
            
            attack = current_attacker.select_attack()
            if attack:
                self.perform_attack(current_attacker, current_defender, attack)
            
            # Update skill durations and cooldowns
            current_attacker.update_skill_durations()
            for attack in current_attacker.attacks:
                if attack.cooldown > 0:
                    attack.cooldown -= 1
            
            # Switch roles
            current_attacker, current_defender = current_defender, current_attacker

        winner = self.robot1 if self.robot2.is_defeated() else self.robot2
        return winner, self.turn_count

    def perform_attack(self, attacker: Robot, defender: Robot, attack: Attack):
        # Check if attack hits
        if random.randint(1, 100) <= attack.precision:
            # Apply damage
            damage = attack.damage
            # TODO: Apply skill effects here (e.g., shields, steroids)
            defender.receive_damage(damage)
            
            # Activate defensive skills
            defender.activate_skills("energy")
            # TODO: Implement other skill triggers
        
        # Set attack cooldown
        attack.cooldown = attack.recharge

#----------------------------------------------------------------------------------------------------------------------------

class League:
    def __init__(self, robots: List[Robot]):
        self.robots = robots
        self.results = defaultdict(lambda: {"wins": 0, "losses": 0, "total_turns": 0})

    def conduct_league(self):
        for i, robot1 in enumerate(self.robots):
            for robot2 in self.robots[i+1:]:
                battle = Battle(robot1, robot2)
                winner, turns = battle.conduct_battle()
                
                loser = robot2 if winner == robot1 else robot1
                
                self.results[winner.name]["wins"] += 1
                self.results[winner.name]["total_turns"] += turns
                self.results[loser.name]["losses"] += 1
                self.results[loser.name]["total_turns"] += turns

        return self.get_league_standings()

    def get_league_standings(self):
        standings = sorted(self.results.items(), key=lambda x: (x[1]["wins"], -x[1]["losses"]), reverse=True)
        return standings
    
def create_sample_robots():
    # Create sample robots with attacks and skills
    # This is a simplified version, you'd typically load this from a JSON file
    robot1 = Robot("FireBot", 100, 
                   [Attack("Flame Thrower", "long", "robot", 30, 80, 1)],
                   [Skill("Heat Shield", "energy", 30, 2, "robot", "shield", 20)])
    
    robot2 = Robot("WaterBot", 120, 
                   [Attack("Water Cannon", "long", "robot", 25, 90, 0)],
                   [Skill("Steam Boost", "turns", 3, 1, "robot", "steroids", 30)])
    
    return [robot1, robot2]

def main():
    robots = create_sample_robots()
    league = League(robots)
    standings = league.conduct_league()
    
    print("League Results:")
    for rank, (name, results) in enumerate(standings, 1):
        print(f"{rank}. {name}: Wins: {results['wins']}, Losses: {results['losses']}, Total Turns: {results['total_turns']}")

if __name__ == "__main__":
    main()
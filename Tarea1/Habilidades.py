class Skill:
    def __init__(
        self,
        name: str,
        trigger: str,
        trigger_value: int,
        duration: int,
        objective: str,
        effect: str,
        effect_value: int,
    ):
        self.name = name
        self.trigger = trigger
        self.trigger_value = trigger_value
        self.duration = duration
        self.objective = objective
        self.effect = effect
        self.effect_value = effect_value
        self.active = False
        self.remaining_duration = 0

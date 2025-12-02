import random

INVADER_TYPES = {
    "alien": {
        "health": 1,
        "bullet_speed": 3,
        "fire_rate": 0.002,
        "points": 10
    },
    "squid": {
        "health": 2,
        "bullet_speed": 4,
        "fire_rate": 0.004,
        "points": 20
    },
    "invader": {
        "health": 3,
        "bullet_speed": 5,
        "fire_rate": 0.006,
        "points": 50
    }
}

def get_level_config(level):
    config = {}
    config["speed"] = 0.5  + (level * 0.00005)
    config["enemy_fire_rate"] = 0.001 + (level * 0.0003)
    config["rows"] = min(5 + level // 2, 10)
    config["cols"] = min(8 + level // 3, 12)
    return config

def pick_invader_type(level):
    prob_invader = min(0.004 + level * 0.004, 0.008)
    prob_squid = min(0.08 + level * 0.08, 0.4)
    r = random.random()
    if r < prob_invader:
        return "invader"
    elif r < prob_invader + prob_squid:
        return "squid"
    else:
        return "alien"
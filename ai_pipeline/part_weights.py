# Rough share of a vehicle's market value that each part represents,
# and the claim percentage for each severity level.


PART_WEIGHT = {
    "bumper": 0.05,
    "door": 0.08,
    "hood": 0.06,
    "windshield": 0.04,
    "headlight": 0.02,
    "tire": 0.03,
}

SEVERITY_PERCENT = {
    "no_damage": 0.0,
    "minor": 0.10,
    "moderate": 0.40,
    "major": 0.70,
}
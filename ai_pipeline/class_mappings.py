# Maps each CNN's raw output index to our internal severity keys.
# Verified directly from each training notebook's class_indices output.
# Do NOT assume these match across models - windshield's order differs.

CLASS_ORDER = {
    "bumper":     ["major", "minor", "moderate", "no_damage"],
    "tire":       ["major", "minor", "moderate", "no_damage"],
    "headlight":  ["major", "minor", "moderate", "no_damage"],
    "door":       ["major", "minor", "moderate", "no_damage"],
    "hood":       ["major", "minor", "moderate", "no_damage"],
    "windshield": ["no_damage", "major", "minor", "moderate"],
}

# YOLO outputs these exact label strings (from data.yaml) - map them
# to the lowercase keys used everywhere else (CLASS_ORDER, CNN filenames).
YOLO_LABEL_TO_PART_KEY = {
    "Bumper": "bumper",
    "Headlight": "headlight",
    "Tire": "tire",
    "Hood": "hood",
    "Door": "door",
    "Windshield": "windshield",
}
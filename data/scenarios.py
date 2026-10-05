SCENARIOS = {

    "Normal Demand": {
        "Area1": 40,
        "Area2": 50,
        "Area3": 30,
        "Area4": 60
    },

    "High Demand": {
        "Area1": 50,
        "Area2": 60,
        "Area3": 40,
        "Area4": 70
    },

    "Low Demand": {
        "Area1": 30,
        "Area2": 40,
        "Area3": 20,
        "Area4": 40
    }
}


PIPE_FAILURES = {

    "No Failure": None,

    "Source → Junction_A": (
        "Source",
        "Junction_A"
    ),

    "Source → Junction_B": (
        "Source",
        "Junction_B"
    ),

    "Junction_B → Area4": (
        "Junction_B",
        "Area4"
    )
}
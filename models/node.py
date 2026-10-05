class Node:
    def __init__(self, name, demand=0):
        self.name = name
        self.demand = demand

    def __str__(self):
        return f"{self.name} (Demand: {self.demand})"
class Pipe:
    def __init__(self, source, destination, capacity, cost):
        self.source = source
        self.destination = destination
        self.capacity = capacity
        self.cost = cost
        self.flow = 0

    def __str__(self):
        return (
            f"{self.source} -> {self.destination} "
            f"(Capacity: {self.capacity}, Cost: {self.cost})"
        )
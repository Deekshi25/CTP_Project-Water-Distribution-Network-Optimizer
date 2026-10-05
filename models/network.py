class WaterNetwork:

    def __init__(self):
        self.nodes = {}
        self.pipes = []

    def add_node(self, node):
        self.nodes[node.name] = node

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def display_nodes(self):
        print("\nWATER DISTRIBUTION NODES")
        print("-" * 40)

        for node in self.nodes.values():
            print(node)

    def display_pipes(self):
        print("\nWATER DISTRIBUTION PIPES")
        print("-" * 60)

        for pipe in self.pipes:
            print(pipe)
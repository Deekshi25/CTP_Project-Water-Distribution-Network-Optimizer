from collections import deque


class MaxFlowOptimizer:

    def __init__(self, network):
        self.network = network
        self.flow = {}

    def build_graph(self):
        """Create the residual graph."""

        graph = {}

        for node in self.network.nodes:
            graph[node] = {}

        for pipe in self.network.pipes:
            graph[pipe.source][pipe.destination] = pipe.capacity

            if pipe.source not in graph[pipe.destination]:
                graph[pipe.destination][pipe.source] = 0

        return graph

    def bfs(self, graph, source, sink, parent):
        """Find an augmenting path using BFS."""

        visited = set()
        queue = deque([source])

        visited.add(source)
        parent[source] = None

        while queue:

            current = queue.popleft()

            for neighbour, capacity in graph[current].items():

                if neighbour not in visited and capacity > 0:

                    visited.add(neighbour)
                    parent[neighbour] = current

                    if neighbour == sink:
                        return True

                    queue.append(neighbour)

        return False

    def calculate_max_flow(self, source_name):
        """Calculate maximum flow."""

        graph = self.build_graph()

        sink = "SUPER_SINK"
        graph[sink] = {}

        # Connect demand nodes to the super sink
        for node in self.network.nodes.values():

            if node.demand > 0:
                graph[node.name][sink] = node.demand
                graph[sink][node.name] = 0

        max_flow = 0

        while True:

            parent = {}

            if not self.bfs(
                graph,
                source_name,
                sink,
                parent
            ):
                break

            # Find bottleneck capacity
            path_flow = float("inf")
            current = sink

            while current != source_name:

                previous = parent[current]

                path_flow = min(
                    path_flow,
                    graph[previous][current]
                )

                current = previous

            # Update residual graph
            current = sink

            while current != source_name:

                previous = parent[current]

                graph[previous][current] -= path_flow

                if previous not in graph[current]:
                    graph[current][previous] = 0

                graph[current][previous] += path_flow

                current = previous

            max_flow += path_flow

        # Store flow for every original pipe
        self.flow = {}

        for pipe in self.network.pipes:

            original_capacity = pipe.capacity
            remaining_capacity = graph[pipe.source][pipe.destination]

            pipe.flow = original_capacity - remaining_capacity

            self.flow[
                (pipe.source, pipe.destination)
            ] = pipe.flow

        return max_flow

    def display_flow(self):
        """Display flow through every pipe."""

        print("\nPIPE FLOW ANALYSIS")
        print("-" * 75)

        print(
            f"{'Pipe':30}"
            f"{'Flow':>10}"
            f"{'Capacity':>12}"
            f"{'Utilization':>15}"
        )

        print("-" * 75)

        for pipe in self.network.pipes:

            utilization = (
                pipe.flow / pipe.capacity
            ) * 100

            pipe_name = (
                f"{pipe.source} -> {pipe.destination}"
            )

            print(
                f"{pipe_name:30}"
                f"{pipe.flow:>10.0f}"
                f"{pipe.capacity:>12}"
                f"{utilization:>14.1f}%"
            )
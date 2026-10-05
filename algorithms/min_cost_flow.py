from collections import deque


class Edge:
    def __init__(self, to, reverse, capacity, cost, pipe_index=None):
        self.to = to
        self.reverse = reverse
        self.capacity = capacity
        self.cost = cost
        self.pipe_index = pipe_index


class MinCostFlowOptimizer:

    def __init__(self, network):
        self.network = network
        self.total_flow = 0
        self.total_cost = 0

    def add_edge(
        self,
        graph,
        source,
        destination,
        capacity,
        cost,
        pipe_index=None
    ):
        """Add forward and reverse edges."""

        forward = Edge(
            destination,
            len(graph[destination]),
            capacity,
            cost,
            pipe_index
        )

        reverse = Edge(
            source,
            len(graph[source]),
            0,
            -cost,
            pipe_index
        )

        graph[source].append(forward)
        graph[destination].append(reverse)

    def build_graph(self):
        """Build residual graph."""

        graph = [[] for _ in range(
            len(self.network.nodes) + 1
        )]

        self.node_index = {
            name: index
            for index, name in enumerate(
                self.network.nodes.keys()
            )
        }

        # Add original pipes
        for index, pipe in enumerate(self.network.pipes):

            source = self.node_index[pipe.source]
            destination = self.node_index[pipe.destination]

            self.add_edge(
                graph,
                source,
                destination,
                pipe.capacity,
                pipe.cost,
                index
            )

        # Super sink
        self.sink = len(self.network.nodes)

        # Connect consumer areas to super sink
        for node in self.network.nodes.values():

            if node.demand > 0:

                node_id = self.node_index[node.name]

                self.add_edge(
                    graph,
                    node_id,
                    self.sink,
                    node.demand,
                    0
                )

        return graph

    def shortest_path(self, graph, source, sink):
        """
        Bellman-Ford shortest path.

        Used because residual graphs contain
        negative-cost reverse edges.
        """

        n = len(graph)

        distance = [float("inf")] * n
        parent = [None] * n

        distance[source] = 0

        # Relax edges
        for _ in range(n - 1):

            changed = False

            for u in range(n):

                if distance[u] == float("inf"):
                    continue

                for edge_index, edge in enumerate(graph[u]):

                    if edge.capacity <= 0:
                        continue

                    new_distance = (
                        distance[u] + edge.cost
                    )

                    if new_distance < distance[edge.to]:

                        distance[edge.to] = new_distance

                        parent[edge.to] = (
                            u,
                            edge_index
                        )

                        changed = True

            if not changed:
                break

        return distance, parent

    def optimize(self, source_name):
        """Run Successive Shortest Path algorithm."""

        graph = self.build_graph()

        source = self.node_index[source_name]

        self.total_flow = 0
        self.total_cost = 0

        # Reset pipe flows
        for pipe in self.network.pipes:
            pipe.flow = 0

        while True:

            distance, parent = self.shortest_path(
                graph,
                source,
                self.sink
            )

            # No path to sink
            if distance[self.sink] == float("inf"):
                break

            # Find bottleneck capacity
            path_flow = float("inf")

            current = self.sink

            while current != source:

                previous, edge_index = parent[current]

                edge = graph[previous][edge_index]

                path_flow = min(
                    path_flow,
                    edge.capacity
                )

                current = previous

            # Update residual graph
            current = self.sink

            while current != source:

                previous, edge_index = parent[current]

                edge = graph[previous][edge_index]

                edge.capacity -= path_flow

                reverse_edge = graph[current][edge.reverse]

                reverse_edge.capacity += path_flow

                # Update original pipe flow
                if edge.pipe_index is not None:

                    self.network.pipes[
                        edge.pipe_index
                    ].flow += path_flow

                elif reverse_edge.pipe_index is not None:

                    self.network.pipes[
                        reverse_edge.pipe_index
                    ].flow -= path_flow

                current = previous

            self.total_flow += path_flow

            self.total_cost += (
                path_flow * distance[self.sink]
            )

        return self.total_flow, self.total_cost

    def display_result(self):

        print("\n")
        print("=" * 70)
        print("MIN-COST FLOW ANALYSIS")
        print("=" * 70)

        print(
            f"{'Pipe':35}"
            f"{'Flow':>10}"
            f"{'Capacity':>12}"
            f"{'Cost':>10}"
        )

        print("-" * 70)

        for pipe in self.network.pipes:

            print(
                f"{pipe.source} -> "
                f"{pipe.destination:<20}"
                f"{pipe.flow:>10.0f}"
                f"{pipe.capacity:>12}"
                f"{pipe.cost:>10}"
            )

        print("-" * 70)

        print(
            f"Total Flow : {self.total_flow} units"
        )

        print(
            f"Minimum Cost : ₹{self.total_cost}"
        )
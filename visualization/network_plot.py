import matplotlib.pyplot as plt
import networkx as nx


def draw_network(
    network,
    title="Optimized Water Distribution Network",
    total_flow=None,
    total_cost=None
):

    graph = nx.DiGraph()

    # -----------------------------
    # Add nodes
    # -----------------------------

    for node in network.nodes.values():
        graph.add_node(
            node.name,
            demand=node.demand
        )

    # -----------------------------
    # Add pipes
    # -----------------------------

    for pipe in network.pipes:
        graph.add_edge(
            pipe.source,
            pipe.destination,
            capacity=pipe.capacity,
            flow=pipe.flow,
            cost=pipe.cost
        )

    # -----------------------------
    # Fixed positions
    # -----------------------------

    positions = {
        "Source": (0, 2),

        "Junction_A": (2, 3),
        "Junction_B": (2, 1),

        "Area1": (5, 4),
        "Area2": (5, 2.5),
        "Area3": (5, 1),
        "Area4": (5, -0.5)
    }

    # -----------------------------
    # Node categories
    # -----------------------------

    source_nodes = ["Source"]

    junction_nodes = [
        "Junction_A",
        "Junction_B"
    ]

    area_nodes = [
        "Area1",
        "Area2",
        "Area3",
        "Area4"
    ]

    # -----------------------------
    # Draw figure
    # -----------------------------

    plt.figure(figsize=(14, 8))

    # Source
    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=source_nodes,
        node_size=2600,
        node_color="lightgreen",
        node_shape="s"
    )

    # Junctions
    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=junction_nodes,
        node_size=2500,
        node_color="skyblue",
        node_shape="o"
    )

    # Consumer areas
    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=area_nodes,
        node_size=2300,
        node_color="orange",
        node_shape="o"
    )

    # Node labels
    nx.draw_networkx_labels(
        graph,
        positions,
        font_size=10
    )

    # -----------------------------
    # Edge widths based on utilization
    # -----------------------------

    edge_widths = []

    for source, destination, data in graph.edges(
        data=True
    ):

        capacity = data["capacity"]
        flow = data["flow"]

        utilization = (
            flow / capacity * 100
            if capacity > 0
            else 0
        )

        if utilization >= 80:
            width = 4

        elif utilization >= 50:
            width = 3

        else:
            width = 2

        edge_widths.append(width)

    # Draw edges
    nx.draw_networkx_edges(
        graph,
        positions,
        arrows=True,
        arrowsize=20,
        width=edge_widths,
        connectionstyle="arc3,rad=0.02"
    )

    # -----------------------------
    # Edge labels
    # -----------------------------

    edge_labels = {}

    for source, destination, data in graph.edges(
        data=True
    ):

        capacity = data["capacity"]
        flow = data["flow"]

        utilization = (
            flow / capacity * 100
            if capacity > 0
            else 0
        )

        label = (
            f"Flow: {flow}\n"
            f"Capacity: {capacity}\n"
            f"Use: {utilization:.1f}%\n"
            f"Cost: {data['cost']}"
        )

        edge_labels[
            (source, destination)
        ] = label

    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=edge_labels,
        font_size=8,
        label_pos=0.5
    )

    # -----------------------------
    # Title
    # -----------------------------

    plt.title(
        title,
        fontsize=16,
        fontweight="bold"
    )

    # -----------------------------
    # Summary box
    # -----------------------------

    if total_flow is not None and total_cost is not None:

        summary = (
            f"Total Water Flow : {total_flow} units\n"
            f"Minimum Cost     : ₹{total_cost}"
        )

        plt.text(
            0.02,
            0.02,
            summary,
            transform=plt.gca().transAxes,
            fontsize=11,
            verticalalignment="bottom",
            bbox=dict(
                boxstyle="round",
                facecolor="white",
                edgecolor="black"
            )
        )

    # -----------------------------
    # Legend
    # -----------------------------

    plt.text(
        0.82,
        0.96,
        "SOURCE",
        transform=plt.gca().transAxes,
        fontsize=10,
        fontweight="bold"
    )

    plt.text(
        0.82,
        0.92,
        "JUNCTION",
        transform=plt.gca().transAxes,
        fontsize=10
    )

    plt.text(
        0.82,
        0.88,
        "CONSUMER AREA",
        transform=plt.gca().transAxes,
        fontsize=10
    )

    plt.axis("off")

    plt.tight_layout()

    return plt.gcf()
from models.node import Node
from models.pipe import Pipe
from models.network import WaterNetwork

from algorithms.max_flow import MaxFlowOptimizer
from algorithms.min_cost_flow import MinCostFlowOptimizer

from visualization.network_plot import draw_network

from data.scenarios import SCENARIOS, PIPE_FAILURES


# ==========================================
# CREATE WATER NETWORK
# ==========================================

def create_network():

    network = WaterNetwork()

    # --------------------------------------
    # Nodes
    # --------------------------------------

    network.add_node(
        Node("Source")
    )

    network.add_node(
        Node("Junction_A")
    )

    network.add_node(
        Node("Junction_B")
    )

    network.add_node(
        Node("Area1", demand=40)
    )

    network.add_node(
        Node("Area2", demand=50)
    )

    network.add_node(
        Node("Area3", demand=30)
    )

    network.add_node(
        Node("Area4", demand=60)
    )

    # --------------------------------------
    # Pipes
    # --------------------------------------

    network.add_pipe(
        Pipe(
            "Source",
            "Junction_A",
            120,
            2
        )
    )

    network.add_pipe(
        Pipe(
            "Source",
            "Junction_B",
            100,
            3
        )
    )

    network.add_pipe(
        Pipe(
            "Junction_A",
            "Area1",
            50,
            4
        )
    )

    network.add_pipe(
        Pipe(
            "Junction_A",
            "Area2",
            60,
            3
        )
    )

    network.add_pipe(
        Pipe(
            "Junction_A",
            "Junction_B",
            40,
            1
        )
    )

    network.add_pipe(
        Pipe(
            "Junction_B",
            "Area2",
            40,
            2
        )
    )

    network.add_pipe(
        Pipe(
            "Junction_B",
            "Area3",
            50,
            3
        )
    )

    network.add_pipe(
        Pipe(
            "Junction_B",
            "Area4",
            70,
            2
        )
    )

    return network


# ==========================================
# APPLY DEMAND SCENARIO
# ==========================================

def apply_scenario(network, scenario_name):

    demands = SCENARIOS[scenario_name]

    for node_name, demand in demands.items():

        if node_name in network.nodes:

            network.nodes[node_name].demand = demand

    return network


# ==========================================
# APPLY PIPE FAILURE
# ==========================================

def apply_pipe_failure(network, failure_name):

    failure = PIPE_FAILURES[failure_name]

    # No failure
    if failure == "None":

        return network

    # Find failed pipe
    for pipe in network.pipes:

        pipe_name = (
            f"{pipe.source} -> "
            f"{pipe.destination}"
        )

        if pipe_name == failure:

            # Disable pipe
            pipe.capacity = 0

            pipe.flow = 0

            print(
                f"\n⚠️ PIPE FAILURE: {failure}"
            )

            print(
                "Pipe capacity set to 0."
            )

            break

    return network


# ==========================================
# DISPLAY SCENARIOS
# ==========================================

def select_scenario():

    print("\n")
    print("=" * 60)
    print("AVAILABLE DEMAND SCENARIOS")
    print("=" * 60)

    scenario_names = list(
        SCENARIOS.keys()
    )

    for index, name in enumerate(
        scenario_names,
        start=1
    ):

        print(
            f"{index}. {name}"
        )

    print("=" * 60)

    while True:

        try:

            choice = int(
                input(
                    "Select demand scenario "
                    "(enter number): "
                )
            )

            if 1 <= choice <= len(
                scenario_names
            ):

                return scenario_names[
                    choice - 1
                ]

            print(
                "Invalid choice. Try again."
            )

        except ValueError:

            print(
                "Please enter a number."
            )


# ==========================================
# SELECT PIPE FAILURE
# ==========================================

def select_failure():

    print("\n")
    print("=" * 60)
    print("AVAILABLE PIPE FAILURE SCENARIOS")
    print("=" * 60)

    failure_names = list(
        PIPE_FAILURES.keys()
    )

    for index, name in enumerate(
        failure_names,
        start=1
    ):

        print(
            f"{index}. {name}"
        )

    print("=" * 60)

    while True:

        try:

            choice = int(
                input(
                    "Select pipe failure "
                    "(enter number): "
                )
            )

            if 1 <= choice <= len(
                failure_names
            ):

                return failure_names[
                    choice - 1
                ]

            print(
                "Invalid choice. Try again."
            )

        except ValueError:

            print(
                "Please enter a number."
            )


# ==========================================
# MAIN
# ==========================================

def main():

    print("\n")
    print("=" * 60)
    print("WATER DISTRIBUTION NETWORK OPTIMIZER")
    print("=" * 60)

    # ======================================
    # SELECT SCENARIO
    # ======================================

    selected_scenario = select_scenario()

    selected_failure = select_failure()

    print("\n")
    print("=" * 60)
    print("SELECTED CONFIGURATION")
    print("=" * 60)

    print(
        f"Demand Scenario : {selected_scenario}"
    )

    print(
        f"Pipe Failure    : {selected_failure}"
    )

    # ======================================
    # MAX FLOW
    # ======================================

    max_network = create_network()

    # Apply demand scenario
    max_network = apply_scenario(
        max_network,
        selected_scenario
    )

    # Apply pipe failure
    max_network = apply_pipe_failure(
        max_network,
        selected_failure
    )

    # Calculate total demand
    total_demand = sum(
        node.demand
        for node in max_network.nodes.values()
    )

    print("\n")
    print("=" * 60)
    print("MAX-FLOW ANALYSIS")
    print("=" * 60)

    print(
        f"Total Water Demand : "
        f"{total_demand} units"
    )

    # Create Max Flow optimizer
    max_optimizer = MaxFlowOptimizer(
        max_network
    )

    # Calculate maximum flow
    max_flow = max_optimizer.calculate_max_flow(
        "Source"
    )

    # Display flow
    max_optimizer.display_flow()

    print(
        f"\nMaximum Water Flow : "
        f"{max_flow} units"
    )

    # Check demand
    if max_flow >= total_demand:

        print(
            "Status              : "
            "DEMAND SATISFIED"
        )

    else:

        shortage = (
            total_demand - max_flow
        )

        print(
            "Status              : "
            "WATER SHORTAGE"
        )

        print(
            f"Shortage            : "
            f"{shortage} units"
        )

    # ======================================
    # MIN-COST FLOW
    # ======================================

    cost_network = create_network()

    # Apply same demand scenario
    cost_network = apply_scenario(
        cost_network,
        selected_scenario
    )

    # Apply same pipe failure
    cost_network = apply_pipe_failure(
        cost_network,
        selected_failure
    )

    print("\n")
    print("=" * 60)
    print("MIN-COST FLOW ANALYSIS")
    print("=" * 60)

    # Create optimizer
    cost_optimizer = MinCostFlowOptimizer(
        cost_network
    )

    # Calculate minimum cost
    total_flow, total_cost = (
        cost_optimizer.optimize(
            "Source"
        )
    )

    # Display result
    cost_optimizer.display_result()

    # ======================================
    # OPTIMIZATION SUMMARY
    # ======================================

    print("\n")
    print("=" * 60)
    print("OPTIMIZATION SUMMARY")
    print("=" * 60)

    print(
        f"Demand Scenario : "
        f"{selected_scenario}"
    )

    print(
        f"Pipe Failure    : "
        f"{selected_failure}"
    )

    print(
        f"Required Water  : "
        f"{total_demand} units"
    )

    print(
        f"Delivered Water : "
        f"{total_flow} units"
    )

    print(
        f"Maximum Flow    : "
        f"{max_flow} units"
    )

    print(
        f"Minimum Cost    : "
        f"₹{total_cost}"
    )

    # ======================================
    # FINAL STATUS
    # ======================================

    if total_flow >= total_demand:

        print(
            "Status          : "
            "ALL DEMAND SATISFIED"
        )

    else:

        shortage = (
            total_demand - total_flow
        )

        print(
            "Status          : "
            "WATER SHORTAGE"
        )

        print(
            f"Shortage        : "
            f"{shortage} units"
        )

    # ======================================
    # NETWORK VISUALIZATION
    # ======================================

    print("\n")
    print(
        "Generating optimized network "
        "visualization..."
    )

    draw_network(
        cost_network,
        "Optimized Water Distribution Network",
        total_flow,
        total_cost
    )


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()
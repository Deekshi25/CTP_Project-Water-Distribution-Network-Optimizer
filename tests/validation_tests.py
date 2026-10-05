from models.node import Node
from models.pipe import Pipe
from models.network import WaterNetwork

from algorithms.max_flow import MaxFlowOptimizer
from algorithms.min_cost_flow import MinCostFlowOptimizer

from data.scenarios import SCENARIOS, PIPE_FAILURES


# ============================================================
# CREATE NETWORK
# ============================================================

def create_network():

    network = WaterNetwork()

    # Nodes
    network.add_node(Node("Source"))
    network.add_node(Node("Junction_A"))
    network.add_node(Node("Junction_B"))

    network.add_node(Node("Area1", demand=40))
    network.add_node(Node("Area2", demand=50))
    network.add_node(Node("Area3", demand=30))
    network.add_node(Node("Area4", demand=60))

    # Pipes
    network.add_pipe(
        Pipe("Source", "Junction_A", 120, 2)
    )

    network.add_pipe(
        Pipe("Source", "Junction_B", 100, 3)
    )

    network.add_pipe(
        Pipe("Junction_A", "Area1", 50, 4)
    )

    network.add_pipe(
        Pipe("Junction_A", "Area2", 60, 3)
    )

    network.add_pipe(
        Pipe("Junction_A", "Junction_B", 40, 1)
    )

    network.add_pipe(
        Pipe("Junction_B", "Area2", 40, 2)
    )

    network.add_pipe(
        Pipe("Junction_B", "Area3", 50, 3)
    )

    network.add_pipe(
        Pipe("Junction_B", "Area4", 70, 2)
    )

    return network


# ============================================================
# APPLY SCENARIO
# ============================================================

def apply_scenario(network, scenario_name):

    demands = SCENARIOS[scenario_name]

    for node_name, demand in demands.items():

        if node_name in network.nodes:

            network.nodes[node_name].demand = demand

    return network


# ============================================================
# APPLY FAILURE
# ============================================================

def apply_failure(network, failure_name):

    failure = PIPE_FAILURES[failure_name]

    if failure is None:
        return network

    failed_source, failed_destination = failure

    for pipe in network.pipes:

        if (
            pipe.source == failed_source
            and pipe.destination == failed_destination
        ):

            pipe.capacity = 0
            pipe.flow = 0

            break

    return network


# ============================================================
# RUN TEST
# ============================================================

def run_test(scenario_name, failure_name):

    network = create_network()

    network = apply_scenario(
        network,
        scenario_name
    )

    network = apply_failure(
        network,
        failure_name
    )

    total_demand = sum(
        node.demand
        for node in network.nodes.values()
    )

    # Maximum flow
    max_optimizer = MaxFlowOptimizer(network)

    max_flow = max_optimizer.calculate_max_flow(
        "Source"
    )

    # Create separate network for min-cost flow
    cost_network = create_network()

    cost_network = apply_scenario(
        cost_network,
        scenario_name
    )

    cost_network = apply_failure(
        cost_network,
        failure_name
    )

    cost_optimizer = MinCostFlowOptimizer(
        cost_network
    )

    delivered, cost = cost_optimizer.optimize(
        "Source"
    )

    return (
        total_demand,
        max_flow,
        delivered,
        cost
    )


# ============================================================
# MAIN TESTING
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 75)
    print("WATER DISTRIBUTION NETWORK - VALIDATION TEST")
    print("=" * 75)

    passed = 0
    total = 0

    # --------------------------------------------------------
    # Test every demand scenario with no failure
    # --------------------------------------------------------

    print()
    print("DEMAND SCENARIO TESTS")
    print("-" * 75)

    for scenario in SCENARIOS:

        total += 1

        demand, max_flow, delivered, cost = run_test(
            scenario,
            "No Failure"
        )

        if delivered >= demand:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"

        print()
        print(f"Scenario       : {scenario}")
        print(f"Demand         : {demand}")
        print(f"Maximum Flow   : {max_flow}")
        print(f"Delivered      : {delivered}")
        print(f"Minimum Cost   : ₹{cost}")
        print(f"Test Result    : {status}")

    # --------------------------------------------------------
    # Pipe failure tests
    # --------------------------------------------------------

    print()
    print("PIPE FAILURE TESTS")
    print("-" * 75)

    for failure in PIPE_FAILURES:

        if failure == "No Failure":
            continue

        total += 1

        demand, max_flow, delivered, cost = run_test(
            "Normal Demand",
            failure
        )

        # Validation:
        # delivered must never exceed demand
        if delivered <= demand:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"

        print()
        print(f"Failure        : {failure}")
        print(f"Demand         : {demand}")
        print(f"Maximum Flow   : {max_flow}")
        print(f"Delivered      : {delivered}")
        print(f"Minimum Cost   : ₹{cost}")
        print(f"Test Result    : {status}")

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print()
    print("=" * 75)
    print("VALIDATION SUMMARY")
    print("=" * 75)

    print(f"Total Tests    : {total}")
    print(f"Passed         : {passed}")
    print(f"Failed         : {total - passed}")

    if passed == total:
        print()
        print("ALL VALIDATION TESTS PASSED")
    else:
        print()
        print("SOME VALIDATION TESTS FAILED")

    print("=" * 75)
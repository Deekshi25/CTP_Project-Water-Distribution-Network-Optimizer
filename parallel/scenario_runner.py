from models.node import Node
from models.pipe import Pipe
from models.network import WaterNetwork

from algorithms.max_flow import MaxFlowOptimizer
from algorithms.min_cost_flow import MinCostFlowOptimizer


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


def run_scenario(scenario_name, demands):

    network = create_network()

    # Apply scenario demands
    for node_name, demand in demands.items():

        if node_name in network.nodes:
            network.nodes[node_name].demand = demand

    total_demand = sum(
        node.demand
        for node in network.nodes.values()
    )

    # Maximum Flow
    max_optimizer = MaxFlowOptimizer(network)

    max_flow = max_optimizer.calculate_max_flow(
        "Source"
    )

    # Minimum Cost
    cost_network = create_network()

    for node_name, demand in demands.items():

        if node_name in cost_network.nodes:
            cost_network.nodes[node_name].demand = demand

    cost_optimizer = MinCostFlowOptimizer(
        cost_network
    )

    total_flow, total_cost = cost_optimizer.optimize(
        "Source"
    )

    return {
        "scenario": scenario_name,
        "demand": total_demand,
        "max_flow": max_flow,
        "delivered": total_flow,
        "cost": total_cost,
        "status": (
            "SATISFIED"
            if total_flow >= total_demand
            else "SHORTAGE"
        )
    }
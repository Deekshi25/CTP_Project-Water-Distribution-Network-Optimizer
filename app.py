import time
from multiprocessing import Pool

import streamlit as st

from models.node import Node
from models.pipe import Pipe
from models.network import WaterNetwork

from algorithms.max_flow import MaxFlowOptimizer
from algorithms.min_cost_flow import MinCostFlowOptimizer

from visualization.network_plot import draw_network

from data.scenarios import SCENARIOS, PIPE_FAILURES

from parallel.scenario_runner import run_scenario


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Water Distribution Optimizer",
    page_icon="💧",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("💧 Water Distribution Network Optimizer")

st.markdown(
    """
    ### Resource-Efficient Water Distribution Optimization

    This system optimizes water distribution using:

    - Maximum Flow optimization
    - Minimum-Cost Flow optimization
    - Demand scenario analysis
    - Pipe failure simulation
    - Parallel scenario processing
    """
)

st.divider()

st.write(
    "Optimize water flow through a pipe network "
    "using Maximum Flow and Minimum-Cost Flow algorithms."
)


# ============================================================
# CREATE NETWORK
# ============================================================

def create_network():

    network = WaterNetwork()

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Pipes
    # --------------------------------------------------------

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


# ============================================================
# APPLY DEMAND SCENARIO
# ============================================================

def apply_scenario(network, scenario_name):

    demands = SCENARIOS[scenario_name]

    for node_name, demand in demands.items():

        if node_name in network.nodes:

            network.nodes[node_name].demand = demand

    return network


# ============================================================
# APPLY PIPE FAILURE
# ============================================================

def apply_pipe_failure(network, failure_name):

    failure = PIPE_FAILURES[failure_name]

    # No failure selected
    if failure is None:
        return network

    failed_source, failed_destination = failure

    # Find the failed pipe
    for pipe in network.pipes:

        if (
            pipe.source == failed_source
            and pipe.destination == failed_destination
        ):

            # Disable the pipe
            pipe.capacity = 0
            pipe.flow = 0

            break

    return network


# ============================================================
# PERFORMANCE TEST
# ============================================================

def run_performance_test():

    # --------------------------------------------------------
    # Sequential execution
    # --------------------------------------------------------

    start = time.perf_counter()

    sequential_results = []

    for scenario_name, demands in SCENARIOS.items():

        result = run_scenario(
            scenario_name,
            demands
        )

        sequential_results.append(result)

    sequential_time = time.perf_counter() - start

    # --------------------------------------------------------
    # Parallel execution
    # --------------------------------------------------------

    tasks = list(SCENARIOS.items())

    start = time.perf_counter()

    with Pool() as pool:

        parallel_results = pool.starmap(
            run_scenario,
            tasks
        )

    parallel_time = time.perf_counter() - start

    # --------------------------------------------------------
    # Calculate speedup
    # --------------------------------------------------------

    if parallel_time > 0:

        speedup = sequential_time / parallel_time

    else:

        speedup = 0

    return (
        sequential_time,
        parallel_time,
        speedup,
        parallel_results
    )


# ============================================================
# SESSION STATE
# ============================================================

if "max_flow" not in st.session_state:

    st.session_state.max_flow = None


if "total_flow" not in st.session_state:

    st.session_state.total_flow = None


if "total_cost" not in st.session_state:

    st.session_state.total_cost = None


if "optimization_completed" not in st.session_state:

    st.session_state.optimization_completed = False


# ============================================================
# SIDEBAR - SCENARIO SELECTION
# ============================================================

st.sidebar.header("⚙️ Scenario Analysis")


selected_scenario = st.sidebar.selectbox(
    "Select Demand Scenario",
    list(SCENARIOS.keys())
)


selected_failure = st.sidebar.selectbox(
    "Select Pipe Failure",
    list(PIPE_FAILURES.keys())
)


# ============================================================
# CREATE DISPLAY NETWORK
# ============================================================

network = create_network()

network = apply_scenario(
    network,
    selected_scenario
)

network = apply_pipe_failure(
    network,
    selected_failure
)


# ============================================================
# CALCULATE TOTAL DEMAND
# ============================================================

total_demand = sum(
    node.demand
    for node in network.nodes.values()
)


# ============================================================
# SIDEBAR - NETWORK INFORMATION
# ============================================================

st.sidebar.header("📊 Network Information")


st.sidebar.metric(
    "Total Water Demand",
    f"{total_demand} units"
)


st.sidebar.metric(
    "Number of Pipes",
    len(network.pipes)
)


st.sidebar.metric(
    "Number of Consumer Areas",
    4
)


# ============================================================
# SELECTED SCENARIO INFORMATION
# ============================================================

st.subheader("🔍 Current Scenario")


col1, col2 = st.columns(2)


with col1:

    st.info(
        f"**Demand Scenario:** {selected_scenario}"
    )


with col2:

    if selected_failure == "No Failure":

        st.success(
            "✅ All pipes are operational"
        )

    else:

        st.warning(
            f"⚠️ Failed Pipe: {selected_failure}"
        )


# ============================================================
# RUN OPTIMIZATION
# ============================================================

if st.button(
    "🚀 Run Water Optimization",
    use_container_width=True
):

    # ========================================================
    # MAX FLOW NETWORK
    # ========================================================

    max_network = create_network()

    max_network = apply_scenario(
        max_network,
        selected_scenario
    )

    max_network = apply_pipe_failure(
        max_network,
        selected_failure
    )

    # ========================================================
    # MAX FLOW
    # ========================================================

    max_optimizer = MaxFlowOptimizer(
        max_network
    )

    max_flow = max_optimizer.calculate_max_flow(
        "Source"
    )

    # Store result
    st.session_state.max_flow = max_flow


    # ========================================================
    # MINIMUM COST NETWORK
    # ========================================================

    cost_network = create_network()

    cost_network = apply_scenario(
        cost_network,
        selected_scenario
    )

    cost_network = apply_pipe_failure(
        cost_network,
        selected_failure
    )


    # ========================================================
    # MINIMUM COST FLOW
    # ========================================================

    cost_optimizer = MinCostFlowOptimizer(
        cost_network
    )

    total_flow, total_cost = (
        cost_optimizer.optimize("Source")
    )

    # Store results
    st.session_state.total_flow = total_flow
    st.session_state.total_cost = total_cost


    # Mark optimization as completed
    st.session_state.optimization_completed = True


    # ========================================================
    # OPTIMIZATION COMPLETED
    # ========================================================

    st.success(
        "✅ Optimization completed successfully!"
    )


    # ========================================================
    # RESULT METRICS
    # ========================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Maximum Flow",
            f"{max_flow} units"
        )


    with col2:

        st.metric(
            "Delivered Water",
            f"{total_flow} units"
        )


    with col3:

        st.metric(
            "Minimum Cost",
            f"₹{total_cost}"
        )


    # ========================================================
    # DEMAND STATUS
    # ========================================================

    if total_flow >= total_demand:

        st.success(
            "✅ All water demand is satisfied."
        )

    else:

        shortage = total_demand - total_flow

        st.error(
            f"⚠️ Water shortage: {shortage} units"
        )


    # ========================================================
    # PIPE ALLOCATION
    # ========================================================

    st.subheader(
        "📋 Optimized Pipe Allocation"
    )


    table_data = []


    for pipe in cost_network.pipes:

        utilization = (
            pipe.flow / pipe.capacity * 100
            if pipe.capacity > 0
            else 0
        )


        table_data.append({

            "Pipe":
                f"{pipe.source} → {pipe.destination}",

            "Flow":
                pipe.flow,

            "Capacity":
                pipe.capacity,

            "Utilization (%)":
                round(
                    utilization,
                    2
                ),

            "Cost / Unit":
                pipe.cost

        })


    st.dataframe(
        table_data,
        use_container_width=True
    )


    # ========================================================
    # NETWORK VISUALIZATION
    # ========================================================

    st.subheader(
        "📈 Optimized Network Visualization"
    )


    figure = draw_network(

        cost_network,

        "Optimized Water Distribution Network",

        total_flow,

        total_cost

    )


    st.pyplot(
        figure,
        clear_figure=True
    )


# ============================================================
# OVERALL PROJECT RESULTS
# ============================================================

st.header("📊 Overall Project Results")


st.write(
    "Summary of the selected water distribution scenario."
)


if st.session_state.optimization_completed:

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Demand",
        f"{total_demand} units"
    )


    col2.metric(
        "Maximum Flow",
        f"{st.session_state.max_flow} units"
    )


    col3.metric(
        "Delivered Water",
        f"{st.session_state.total_flow} units"
    )


    col4.metric(
        "Minimum Cost",
        f"₹{st.session_state.total_cost}"
    )


    st.divider()


    if st.session_state.total_flow >= total_demand:

        st.success(
            "✓ The selected scenario can satisfy "
            "the total water demand."
        )

    else:

        shortage = (
            total_demand
            - st.session_state.total_flow
        )

        st.warning(
            f"⚠ Water shortage detected: "
            f"{shortage} units."
        )

else:

    st.info(
        "Click '🚀 Run Water Optimization' "
        "to generate the project results."
    )


# ============================================================
# PERFORMANCE ANALYSIS
# ============================================================

st.header("⚡ Performance Analysis")


st.write(
    "Comparison of sequential and multiprocessing "
    "execution for different water-demand scenarios."
)


if st.button("Run Performance Test"):

    with st.spinner(
        "Running performance test..."
    ):

        (
            sequential_time,
            parallel_time,
            speedup,
            results
        ) = run_performance_test()


    # ========================================================
    # PERFORMANCE METRICS
    # ========================================================

    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Sequential Time",
        f"{sequential_time:.6f} s"
    )


    col2.metric(
        "Parallel Time",
        f"{parallel_time:.6f} s"
    )


    col3.metric(
        "Speedup",
        f"{speedup:.2f}x"
    )


    # ========================================================
    # SCENARIO PERFORMANCE RESULTS
    # ========================================================

    st.subheader(
        "Scenario Performance Results"
    )


    performance_data = []


    for result in results:

        performance_data.append({

            "Scenario":
                result["scenario"],

            "Demand":
                result["demand"],

            "Maximum Flow":
                result["max_flow"],

            "Delivered":
                result["delivered"],

            "Minimum Cost":
                result["cost"],

            "Status":
                result["status"]

        })


    st.dataframe(
        performance_data,
        use_container_width=True
    )


    # ========================================================
    # EXECUTION TIME COMPARISON
    # ========================================================

    st.subheader(
        "Execution Time Comparison"
    )


    chart_data = {

        "Execution Type": [
            "Sequential",
            "Parallel"
        ],

        "Time (seconds)": [
            sequential_time,
            parallel_time
        ]

    }


    st.bar_chart(
        chart_data,
        x="Execution Type",
        y="Time (seconds)"
    )


    # ========================================================
    # PERFORMANCE INTERPRETATION
    # ========================================================

    st.subheader(
        "Performance Interpretation"
    )


    if speedup > 1:

        st.success(
            f"Parallel execution was "
            f"{speedup:.2f}x faster for this workload."
        )


    elif speedup < 1:

        st.info(
            f"Parallel execution took longer for "
            f"this small workload "
            f"(measured speedup: {speedup:.2f}x). "
            "This can happen because multiprocessing "
            "has process-startup overhead."
        )


    else:

        st.info(
            "Both approaches had approximately "
            "the same execution time."
        )


# ============================================================
# NETWORK DETAILS
# ============================================================

st.subheader(
    "🌐 Water Distribution Network"
)


st.write(
    "The network contains one source, two junctions "
    "and four consumer areas."
)


for pipe in network.pipes:

    if pipe.capacity == 0:

        st.error(
            f"❌ **{pipe.source} → {pipe.destination}** | "
            f"FAILED | Capacity: 0"
        )

    else:

        st.write(

            f"**{pipe.source} → {pipe.destination}** | "
            f"Capacity: {pipe.capacity} | "
            f"Cost: ₹{pipe.cost}"

        )
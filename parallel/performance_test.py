import time
from multiprocessing import Pool

from data.scenarios import SCENARIOS
from parallel.scenario_runner import run_scenario


# ============================================================
# SEQUENTIAL EXECUTION
# ============================================================

def run_sequential():

    results = []

    start_time = time.perf_counter()

    for scenario_name, demands in SCENARIOS.items():

        result = run_scenario(
            scenario_name,
            demands
        )

        results.append(result)

    end_time = time.perf_counter()

    execution_time = (
        end_time - start_time
    )

    return results, execution_time


# ============================================================
# PARALLEL EXECUTION
# ============================================================

def run_parallel():

    tasks = []

    for scenario_name, demands in SCENARIOS.items():

        tasks.append(
            (
                scenario_name,
                demands
            )
        )

    start_time = time.perf_counter()

    with Pool() as pool:

        results = pool.starmap(
            run_scenario,
            tasks
        )

    end_time = time.perf_counter()

    execution_time = (
        end_time - start_time
    )

    return results, execution_time


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 65)
    print("SEQUENTIAL VS PARALLEL PERFORMANCE")
    print("=" * 65)


    # --------------------------------------------------------
    # Sequential
    # --------------------------------------------------------

    sequential_results, sequential_time = (
        run_sequential()
    )


    # --------------------------------------------------------
    # Parallel
    # --------------------------------------------------------

    parallel_results, parallel_time = (
        run_parallel()
    )


    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print("\nEXECUTION TIME")
    print("-" * 65)

    print(
        f"Sequential Execution : "
        f"{sequential_time:.6f} seconds"
    )

    print(
        f"Parallel Execution   : "
        f"{parallel_time:.6f} seconds"
    )


    # --------------------------------------------------------
    # Speedup
    # --------------------------------------------------------

    if parallel_time > 0:

        speedup = (
            sequential_time /
            parallel_time
        )

        print(
            f"Speedup              : "
            f"{speedup:.2f}x"
        )


    # --------------------------------------------------------
    # Scenario results
    # --------------------------------------------------------

    print("\nSCENARIO RESULTS")
    print("-" * 65)

    for result in parallel_results:

        print(
            f"\nScenario       : "
            f"{result['scenario']}"
        )

        print(
            f"Demand         : "
            f"{result['demand']} units"
        )

        print(
            f"Maximum Flow   : "
            f"{result['max_flow']} units"
        )

        print(
            f"Delivered      : "
            f"{result['delivered']} units"
        )

        print(
            f"Minimum Cost   : "
            f"₹{result['cost']}"
        )

        print(
            f"Status         : "
            f"{result['status']}"
        )
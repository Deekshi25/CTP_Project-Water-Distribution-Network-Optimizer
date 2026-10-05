from multiprocessing import Pool

from data.scenarios import SCENARIOS
from parallel.scenario_runner import run_scenario


def run_parallel_scenarios():

    tasks = []

    for scenario_name, demands in SCENARIOS.items():

        tasks.append(
            (scenario_name, demands)
        )

    with Pool() as pool:

        results = pool.starmap(
            run_scenario,
            tasks
        )

    return results


if __name__ == "__main__":

    results = run_parallel_scenarios()

    print("\n")
    print("=" * 70)
    print("PARALLEL SCENARIO ANALYSIS")
    print("=" * 70)

    for result in results:

        print(
            f"\nScenario       : {result['scenario']}"
        )

        print(
            f"Water Demand   : {result['demand']} units"
        )

        print(
            f"Maximum Flow   : {result['max_flow']} units"
        )

        print(
            f"Delivered Water: {result['delivered']} units"
        )

        print(
            f"Minimum Cost   : ₹{result['cost']}"
        )

        print(
            f"Status         : {result['status']}"
        )
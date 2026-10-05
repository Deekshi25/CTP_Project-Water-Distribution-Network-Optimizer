# Water Distribution Network Optimizer

## Project Description

The Water Distribution Network Optimizer is a Python-based application developed to optimize the distribution of water from a source to multiple consumer areas.

The system models the water distribution network using nodes and pipes and uses Maximum Flow and Minimum-Cost Flow algorithms to determine water delivery and distribution cost.

The application also supports different demand scenarios, pipe failure simulation, parallel scenario analysis, and network visualization using a Streamlit dashboard.

## Objectives

- Maximize water delivery to consumer areas.
- Minimize water distribution cost.
- Analyze different demand scenarios.
- Simulate pipe failures.
- Compare scenario performance.
- Visualize the water distribution network.

## Features

- Maximum Flow calculation
- Minimum-Cost Flow optimization
- Normal, High and Low demand scenarios
- Pipe failure simulation
- Parallel scenario processing
- Performance comparison
- Network visualization
- Interactive Streamlit dashboard

## Technologies Used

- Python
- Streamlit
- Multiprocessing
- Object-Oriented Programming
- Graph-based optimization
- Git and GitHub

## Project Structure

```text
WaterDistributionOptimizer/
│
├── algorithms/
│   ├── max_flow.py
│   └── min_cost_flow.py
│
├── models/
│   ├── node.py
│   ├── pipe.py
│   └── network.py
│
├── data/
│   └── scenarios.py
│
├── parallel/
│   ├── scenario_runner.py
│   ├── run_parallel.py
│   └── performance_test.py
│
├── visualization/
│   └── network_plot.py
│
├── tests/
│   └── validation_test.py
│
├── RESULT/
├── app.py
├── main.py
├── requirements.txt
└── .gitignore
```





## Algorithms-

Maximum Flow:
------------
Maximum Flow determines the maximum amount of water that can be delivered from the source through the network while respecting the capacity of each pipe.

Minimum-Cost Flow:
-----------------
Minimum-Cost Flow determines a cost-efficient way to distribute the required water by considering the capacity and cost of the pipes.

Demand Scenarios:
-----------------
The system supports three scenarios:

Scenario	Total Demand
Normal	180 units
High	220 units
Low	130 units

## Results:

Scenario	Maximum Flow	Delivered Water	Minimum Cost
Normal	180 units	180 units	₹970
High	220 units	220 units	₹1190
Low	130 units	130 units	₹700




How to Run:
-----------
1. Clone the repository --> git clone "your git_repository url"
2. Open the project folder --> cd CTP_Project-Water-Distribution-Network-Optimizer
3. Create a virtual environment --> python -m venv .venv
4. Activate the virtual environment

For Windows PowerShell:
--> .venv\Scripts\Activate.ps1
5. Install the required packages --> pip install -r requirements.txt
6. Run the application --> streamlit run app.py
The Streamlit dashboard will open in the browser.


## Conclusion:

The Water Distribution Network Optimizer provides an automated approach for analyzing and optimizing water distribution networks using Maximum Flow and Minimum-Cost Flow algorithms.

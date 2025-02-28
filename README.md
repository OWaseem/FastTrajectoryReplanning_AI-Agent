FastTrajectoryReplanning_AI-Agent
CS440 Assignment: Fast Trajectory Replanning using A* and Adaptive A* in a gridworld environment.

Overview
This project implements an AI agent that navigates a partially known gridworld. The agent:

Assumes unknown cells are free until discovered otherwise.
Uses a “shortest presumed-unblocked path” strategy.
Replans when it encounters new obstacles (like fog-of-war scenarios in RTS games).
Key algorithms:

Repeated Forward A* and Repeated Backward A*
Adaptive A* (updates heuristics after each search to speed up subsequent searches)
Features
Gridworld Generation: Automatically create 50 maze-like 101×101 grids using DFS.
Multiple A Variants*: Compare performance of different search strategies.
Tie-Breaking Experiments: Investigate how different tie-break rules affect expansions.
Statistical Significance: Potential for measuring performance differences via hypothesis testing.
Getting Started
Clone the Repository

bash
Copy
git clone https://github.com/Fillds07/FastTrajectoryReplanning_AI-Agent.git
cd FastTrajectoryReplanning_AI-Agent
Set Up Dependencies

Python 3.x (or another language, depending on your implementation)
Libraries (e.g., matplotlib, numpy for Python)
Generate Gridworlds

Run the grid_generation.py (example filename) to create 50 random maze-like grids.
Run the Agent

Execute main.py (example filename) to see the agent in action.
Configure parameters like tie-breaking rules, search direction, etc.
Usage
Command-line Arguments (if implemented):

--algorithm forward or --algorithm backward or --algorithm adaptive
--grid-size 101
--num-grids 50
etc.
Output:

The agent’s path and number of expansions.
Plots showing the agent’s trajectory (if visualization is enabled).
Project Structure
bash
Copy
FastTrajectoryReplanning_AI-Agent/
├── README.md                 # Project description
├── grid_generation.py        # Gridworld generation script
├── main.py                   # Entry point for running the agent
├── a_star.py                 # A* search algorithm
├── repeated_forward_a_star.py
├── repeated_backward_a_star.py
├── adaptive_a_star.py
├── utils/                    # Helper functions (e.g., heuristics, tie-breaking)
└── ...
Contributing
Fork this repo and create a pull request with your changes.
For significant changes, please open an issue first to discuss what you’d like to change.
License
(Optional) You can include a license, e.g., MIT, if you want to share it openly.

Contact
For questions, feel free to open an issue or reach out at [fill.ds07@gmail.com].
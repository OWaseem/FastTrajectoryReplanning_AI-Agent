Below is an updated version of your README that reflects your project's current functionality and organization:

---

# FastTrajectoryReplanning_AI-Agent

**CS440 Assignment – Fast Trajectory Replanning**  
This project implements a fast trajectory replanning system using multiple variants of A* search in a gridworld environment. The agent navigates from a starting cell to a target cell in a gridworld that is initially unknown. As it moves, the agent updates its knowledge of obstacles and replans its route if necessary.

## Overview

The system uses three algorithm variants:
- **Repeated Forward A\***
- **Repeated Backward A\***
- **Adaptive A\*** (which updates its heuristics after each search)

Key features include:
- **Gridworld Generation:**  
  Automatically generates gridworlds using a DFS-based maze generation algorithm with random obstacles.
- **Multiple Algorithm Runs:**  
  The program runs all three algorithms on each generated gridworld. By default, it generates 50 gridworlds of size 101×101.
- **Visual Output:**  
  - Plain gridworlds are saved in the `gridworlds` directory.
  - Result images (showing the agent's trajectory) are saved in the `results` directory.  
    - **Forward** paths are drawn in **blue**.
    - **Backward** paths are drawn in **orange**.
    - **Adaptive** paths are drawn in **red**.
  - If an algorithm fails to find a path, the corresponding image displays a large overlay message at the very top (e.g., “Forward - Target not reachable”).
- **Clean Runs & Logging:**  
  On each run, the program clears previous outputs from the `logs`, `results`, and `gridworlds` directories. A summary log is written to `logs/logs.txt` that shows neat, high-level messages such as:
  - **World Creation:** A summary of gridworld generation (including grid size and file paths).
  - **Algorithm Runs:** For each world, a single summary line per algorithm, e.g.:
    - “World 03: Forward – Path found in 0.1234 sec. → results/forward_world03_grid101.png”
    - “World 03: Backward – No path found (runtime: 0.2345 sec). → results/backward_world03_grid101_NOPATH.png”
    - “World 03: Adaptive – Path found in 0.3456 sec. → results/adaptive_world03_grid101.png”

## Getting Started

### Prerequisites
- Python 3.x
- Required libraries: matplotlib, numpy

### Installation
Clone the repository:
```bash
git clone https://github.com/Fillds07/FastTrajectoryReplanning_AI-Agent.git
cd FastTrajectoryReplanning_AI-Agent
```
Install required packages:
```bash
pip install matplotlib numpy
```

### Usage
To run the simulation with default parameters (50 gridworlds of size 101×101):
```bash
python main.py
```
To customize the grid size or the number of gridworlds, use:
```bash
python main.py --grid_size 21 --n_worlds 10
```
On each run, the program will:
1. Clear the `logs`, `results`, and `gridworlds` directories.
2. Generate gridworlds (plain images saved in `gridworlds/`).
3. Run all three algorithms on each gridworld, saving result images in `results/`.
4. Output a neat, high-level summary to the console and to `logs/logs.txt`.

## Project Structure
```
FastTrajectoryReplanning_AI-Agent/
├── Assignment 1 - CS440-1.pdf    # Assignment instructions and project description
├── README.md                     # Project description and usage instructions
├── a_star.py                     # A* search algorithm implementation
├── adaptive_a_star.py            # Adaptive A* implementation
├── grid_generation.py            # Gridworld generation script
├── main.py                       # Main driver for running the simulation
├── repeated_backward_a_star.py   # Repeated Backward A* implementation
├── repeated_forward_a_star.py    # Repeated Forward A* implementation
├── logs/                         # Contains logs (logs.txt)
├── gridworlds/                   # Contains plain gridworld images
├── results/                      # Contains result images (gridworlds with path overlays)
└── utils/
    └── heuristics.py             # Helper functions (e.g., Manhattan distance)
```

## Experimental Setup
- **Gridworlds:** By default, 50 gridworlds of size 101×101 are generated.
- **Algorithms:** All three A* variants are executed on each gridworld. Performance metrics (e.g., runtime) are recorded.
- **Visualization:**  
  - Successful paths are overlaid in the designated color for each algorithm.
  - If a path cannot be found, a clear overlay message is displayed at the very top of the result image.

## Report
A detailed report is provided in `Assignment 1 - CS440-1.pdf`. It includes:
- An explanation of the gridworld generation and search strategies.
- Experimental setup and performance comparisons.
- Discussion of tie-breaking, heuristic consistency, and any statistical tests used to evaluate performance.

## Contributing
Fork this repo and create a pull request with your changes. For significant modifications, please open an issue first to discuss your proposed changes.

## License
(Optional) This project is released under the MIT License.

## Contact
For questions or feedback, please open an issue or contact [fill.ds07@gmail.com].

---

This README now accurately describes your project’s current functionality, organization, and usage, and aligns with the assignment requirements. Let me know if you need further adjustments!
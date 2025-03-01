import os
import argparse
import shutil
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import time

from grid_generation import generate_grid
from repeated_forward_a_star import repeated_forward_a_star
from repeated_backward_a_star import repeated_backward_a_star
from adaptive_a_star import adaptive_a_star

# Mapping algorithms to path colors
ALGO_COLORS = {
    "forward": "blue",
    "backward": "orange",
    "adaptive": "red"
}

# Define directory names
LOGS_DIR = "logs"
RESULTS_DIR = "results"
GRIDWORLDS_DIR = "gridworlds"
LOGFILE = os.path.join(LOGS_DIR, "logs.txt")

def clear_directory(path):
    """Removes the directory at 'path' (if it exists) and recreates it empty."""
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def log_print(*args, **kwargs):
    """Print to both stdout and the log file."""
    print(*args, **kwargs)
    with open(LOGFILE, "a", encoding="utf-8") as f:
        print(*args, **kwargs, file=f)

def visualize_path(grid, path, filename="output.png", path_color="red", plot_title="Agent Path"):
    """Overlays a path on the grid in path_color and saves the figure (without displaying it)."""
    arr = np.array(grid, dtype=int)
    for (x, y) in path:
        arr[x][y] = 2

    cmap = _get_colormap(path_color)
    bounds = [0, 1, 2, 3]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    plt.figure(figsize=(6, 6))
    plt.imshow(arr, cmap=cmap, norm=norm, origin='upper')
    plt.title(plot_title)
    plt.axis('off')
    _save_figure(filename)

def visualize_no_path(grid, filename="output.png", path_color="red", plot_title="No Path Found", algo_name="Algorithm"):
    """
    Displays the grid with no path, but overlays a large text near the very top
    in the specified color, e.g., "Forward - Target not reachable".
    """
    arr = np.array(grid, dtype=int)
    
    cmap = _get_colormap(path_color)
    bounds = [0, 1, 2, 3]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    plt.figure(figsize=(6, 6))
    plt.imshow(arr, cmap=cmap, norm=norm, origin='upper')
    plt.title(plot_title)
    plt.axis('off')

    center_x = arr.shape[1] / 2.0
    top_y = arr.shape[0] * -0.10  # Position text 10% above the top edge
    message = f"{algo_name.capitalize()} - Target not reachable"
    plt.text(center_x, top_y, message,
             color=path_color, fontsize=16,
             ha='center', va='bottom', alpha=0.9)
    
    _save_figure(filename)

def _get_colormap(path_color):
    """Returns a ListedColormap for the given path_color."""
    path_color = path_color.lower()
    if path_color == "blue":
        return colors.ListedColormap(['white', 'black', 'blue'])
    elif path_color == "orange":
        return colors.ListedColormap(['white', 'black', 'orange'])
    elif path_color == "red":
        return colors.ListedColormap(['white', 'black', 'red'])
    else:
        return colors.ListedColormap(['white', 'black', 'red'])

def _save_figure(filename):
    """Helper to save the current plt figure, logging the output path."""
    out_dir = os.path.dirname(filename)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
    plt.savefig(filename)
    # log_print(f"Saved image to {filename}")
    plt.close()

def run_multi_worlds(args):
    """Generates args.n_worlds gridworlds (size args.grid_size), saves them in GRIDWORLDS_DIR,
       then runs all 3 algorithms on each, storing results in RESULTS_DIR.
    """
    n_worlds = args.n_worlds
    grid_size = args.grid_size

    log_print("\n==================== WORLD CREATION ====================")
    log_print(f"Generating gridworlds of size {grid_size}×{grid_size}...\n")
    
    grid_list = []
    for i in range(1, n_worlds + 1):
        grid = generate_grid(grid_size)
        grid[0][0] = 0
        grid[grid_size - 1][grid_size - 1] = 0
        grid_list.append(grid)

        plain_filename = os.path.join(GRIDWORLDS_DIR, f"gridworld_{i:02d}.png")
        plt.figure(figsize=(6, 6))
        plt.imshow(np.array(grid), cmap='binary', origin='upper')
        plt.title(f"Gridworld {i:02d}")
        plt.axis('off')
        _save_figure(plain_filename)
        log_print(f"World {i:02d}: {plain_filename}")
    
    log_print("\n==================== ALGORITHM RUNS ====================")
    for idx, grid in enumerate(grid_list, start=1):
        log_print(f"\n-------- WORLD {idx:02d} --------")
        start = (0, 0)
        goal = (grid_size - 1, grid_size - 1)
        algorithms = ["forward", "backward", "adaptive"]
        for algo in algorithms:
            t0 = time.time()
            if algo == "forward":
                path, success = repeated_forward_a_star(grid, start, goal)
            elif algo == "backward":
                path, success = repeated_backward_a_star(grid, start, goal)
            elif algo == "adaptive":
                path, success = adaptive_a_star(grid, start, goal)
            t1 = time.time()
            runtime = t1 - t0

            if success:
                log_print(f"World {idx:02d}: {algo.capitalize()} – Path found in {runtime:.4f} sec. → {RESULTS_DIR}/{algo}_world{idx:02d}_grid{grid_size}.png")
                result_filename = os.path.join(RESULTS_DIR, f"{algo}_world{idx:02d}_grid{grid_size}.png")
                plot_title = f"{algo.capitalize()} Path - World {idx:02d}"
                visualize_path(grid, path, filename=result_filename,
                               path_color=ALGO_COLORS[algo],
                               plot_title=plot_title)
            else:
                log_print(f"World {idx:02d}: {algo.capitalize()} – No path found (runtime: {runtime:.4f} sec). → {RESULTS_DIR}/{algo}_world{idx:02d}_grid{grid_size}_NOPATH.png")
                result_filename = os.path.join(RESULTS_DIR, f"{algo}_world{idx:02d}_grid{grid_size}_NOPATH.png")
                plot_title = f"No Path - World {idx:02d}"
                visualize_no_path(grid, filename=result_filename,
                                  path_color=ALGO_COLORS[algo],
                                  plot_title=plot_title,
                                  algo_name=algo)
    log_print("\n==================== SUMMARY ====================")
    log_print(f"Finished processing {n_worlds} gridworlds.")

def run_single_world(args):
    """Generate one gridworld (size args.grid_size) and run all 3 algorithms."""
    log_print("\n==================== SINGLE GRID MODE ====================")
    grid = generate_grid(args.grid_size)
    grid[0][0] = 0
    grid[args.grid_size - 1][args.grid_size - 1] = 0

    start = (0, 0)
    goal = (args.grid_size - 1, args.grid_size - 1)
    algorithms = ["forward", "backward", "adaptive"]

    for algo in algorithms:
        t0 = time.time()
        if algo == "forward":
            path, success = repeated_forward_a_star(grid, start, goal)
        elif algo == "backward":
            path, success = repeated_backward_a_star(grid, start, goal)
        elif algo == "adaptive":
            path, success = adaptive_a_star(grid, start, goal)
        t1 = time.time()
        runtime = t1 - t0

        if success:
            log_print(f"World: {algo.capitalize()} – Path found in {runtime:.4f} sec. → {RESULTS_DIR}/{algo}_single_grid{args.grid_size}.png")
            filename = os.path.join(RESULTS_DIR, f"{algo}_single_grid{args.grid_size}.png")
            plot_title = f"{algo.capitalize()} Path - Single Grid"
            visualize_path(grid, path, filename=filename,
                           path_color=ALGO_COLORS[algo],
                           plot_title=plot_title)
        else:
            log_print(f"World: {algo.capitalize()} – No path found (runtime: {runtime:.4f} sec). → {RESULTS_DIR}/{algo}_single_grid{args.grid_size}_NOPATH.png")
            filename = os.path.join(RESULTS_DIR, f"{algo}_single_grid{args.grid_size}_NOPATH.png")
            plot_title = f"No Path - Single Grid"
            visualize_no_path(grid, filename=filename,
                              path_color=ALGO_COLORS[algo],
                              plot_title=plot_title,
                              algo_name=algo)

def main():
    parser = argparse.ArgumentParser(description="Fast Trajectory Replanning Simulation")
    parser.add_argument('--grid_size', type=int, default=101, help="Size of the gridworld (n x n).")
    parser.add_argument('--n_worlds', type=int, default=50, help="Number of gridworlds to generate and test.")
    args = parser.parse_args()

    # 1) Clear out directories: logs, results, and gridworlds
    clear_directory(LOGS_DIR)
    clear_directory(RESULTS_DIR)
    clear_directory(GRIDWORLDS_DIR)

    # 2) Create a fresh logs file
    with open(LOGFILE, "w", encoding="utf-8") as f:
        f.write("")

    # 3) Run single or multi-world mode
    if args.n_worlds == 1:
        run_single_world(args)
    else:
        run_multi_worlds(args)

if __name__ == '__main__':
    main()

import os
import argparse
from grid_generation import generate_grid
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import time

# Import algorithm implementations.
from repeated_forward_a_star import repeated_forward_a_star
from repeated_backward_a_star import repeated_backward_a_star
from adaptive_a_star import adaptive_a_star

def visualize_path(grid, path, filename="output.png"):
    """
    Visualize the grid using a custom colormap:
      0 -> white (unblocked)
      1 -> black (blocked)
      2 -> red   (path)
    
    The image is saved in the 'images' directory and then displayed.
    """
    # Convert the grid to a NumPy array (int) so we can modify values.
    arr = np.array(grid, dtype=int)
    
    # Mark each cell in the path with a 2 (for red).
    for (x, y) in path:
        arr[x][y] = 2

    # Create a custom colormap: white for free, black for blocked, red for path.
    cmap = colors.ListedColormap(['white', 'black', 'red'])
    bounds = [0, 1, 2, 3]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    plt.figure(figsize=(6, 6))
    plt.imshow(arr, cmap=cmap, norm=norm, origin='upper')
    plt.title("Agent Path")
    plt.axis('off')

    # Always save the image when a path is found.
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    filepath = os.path.join(images_dir, filename)
    plt.savefig(filepath)
    print(f"Saved image to {filepath}")

    plt.show()

def main():
    while(True):
        parser = argparse.ArgumentParser(description="Fast Trajectory Replanning Simulation")
        parser.add_argument('--algorithm', type=str, choices=['forward', 'backward', 'adaptive'], default='forward',
                            help='Algorithm to use: forward, backward, or adaptive')
        parser.add_argument('--grid_size', type=int, default=21,
                            help='Size of the gridworld (n x n)')
        args = parser.parse_args()
        
        grid = generate_grid(args.grid_size)
        
        # Ensure that the start and goal cells are unblocked.
        grid[0][0] = 0
        grid[args.grid_size - 1][args.grid_size - 1] = 0

        start = (0, 0)
        goal = (args.grid_size - 1, args.grid_size - 1)

        start_time = time.time()
    
        if args.algorithm == 'forward':
            path, success = repeated_forward_a_star(grid, start, goal)
        elif args.algorithm == 'backward':
            path, success = repeated_backward_a_star(grid, start, goal)
        elif args.algorithm == 'adaptive':
            path, success = adaptive_a_star(grid, start, goal)

        end_time = time.time()
        total_time = end_time - start_time
        if success:
            print("Path found!")
            # Create a filename based on the algorithm and grid size.
            filename = f"{args.algorithm}_grid{args.grid_size}.png"
            visualize_path(grid, path, filename=filename)
            print(f"Total runtime: {total_time:.6f} seconds")
            break
        else:
            continue
    
if __name__ == '__main__':
    main()

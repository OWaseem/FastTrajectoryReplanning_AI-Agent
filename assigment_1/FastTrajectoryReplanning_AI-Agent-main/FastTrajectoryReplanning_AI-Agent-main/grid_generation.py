import random
import matplotlib.pyplot as plt
import numpy as np

def generate_grid(n):
    """
    Generate a single n x n gridworld using DFS.
    0 = unblocked, 1 = blocked.
    """
    grid = [[None for _ in range(n)] for _ in range(n)]
    visited = [[False for _ in range(n)] for _ in range(n)]

    grid[0][0] = 0
    grid[n-1][n-1] = 0
    
    def get_neighbors(x, y):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                neighbors.append((nx, ny))
        return neighbors

    def dfs(x, y):
        stack = [(x, y)]
        visited[x][y] = True
        grid[x][y] = 0  # unblocked
        while stack:
            cx, cy = stack[-1]
            neighbors = get_neighbors(cx, cy)
            if neighbors:
                nx, ny = random.choice(neighbors)
                visited[nx][ny] = True
                # With 30% probability, mark the cell as blocked.
                if random.random() < 0.3:
                    grid[nx][ny] = 1
                else:
                    grid[nx][ny] = 0
                    stack.append((nx, ny))
            else:
                stack.pop()
    
    # Start DFS from a random cell.
    start_x, start_y = random.randint(0, n - 1), random.randint(0, n - 1)
    dfs(start_x, start_y)
    
    # Ensure all cells are visited (if DFS didn’t cover the whole grid).
    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                dfs(i, j)
    
    return grid

def generate_grids(num, n):
    """Generate a list of 'num' gridworlds each of size n x n."""
    return [generate_grid(n) for _ in range(num)]

def visualize_grid(grid):
    """Display a grid using matplotlib."""
    plt.figure(figsize=(6, 6))
    plt.imshow(np.array(grid), cmap='binary')
    plt.title("Generated Gridworld")
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    # For demonstration: generate and show one 101x101 gridworld.
    grids = generate_grids(50, 101)
    visualize_grid(grids[0])

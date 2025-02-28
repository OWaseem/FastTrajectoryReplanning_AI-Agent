from a_star import a_star_search
from utils.heuristics import manhattan_distance

def repeated_forward_a_star(grid, start, goal):
    """
    Repeated Forward A*:
    The agent uses a known grid that is updated as it observes adjacent cells.
    Returns the full path taken and a boolean indicating success.
    """
    n = len(grid)
    # Initially, assume all cells are unblocked.
    known_grid = [[0 for _ in range(n)] for _ in range(n)]
    current = start
    full_path = [current]
    
    while current != goal:
        path, cost = a_star_search(known_grid, current, goal, heuristic=manhattan_distance)
        if path is None:
            print("Target not reachable with current knowledge.")
            return full_path, False
        # Follow the computed path step by step.
        for next_cell in path[1:]:
            # Update knowledge: reveal status of adjacent cells.
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                adj = (current[0] + dx, current[1] + dy)
                if 0 <= adj[0] < n and 0 <= adj[1] < n:
                    known_grid[adj[0]][adj[1]] = grid[adj[0]][adj[1]]
            # If the next cell is blocked in the real grid, replan.
            if grid[next_cell[0]][next_cell[1]] == 1:
                break
            current = next_cell
            full_path.append(current)
            if current == goal:
                return full_path, True
    return full_path, True

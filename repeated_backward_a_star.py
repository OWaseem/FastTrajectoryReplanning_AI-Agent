from a_star import a_star_search
from utils.heuristics import manhattan_distance

def repeated_backward_a_star(grid, start, goal):
    """
    Repeated Backward A*:
    Searches from the goal to the current agent position and then reverses the found path.
    Returns the full path taken and a boolean indicating success.
    """
    n = len(grid)
    known_grid = [[0 for _ in range(n)] for _ in range(n)]
    current = start
    full_path = [current]
    
    while current != goal:
        # Search from goal to current.
        path, cost = a_star_search(known_grid, goal, current, heuristic=manhattan_distance)
        if path is None:
            print("Target not reachable with current knowledge.")
            return full_path, False
        path = list(reversed(path))
        for next_cell in path[1:]:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                adj = (current[0] + dx, current[1] + dy)
                if 0 <= adj[0] < n and 0 <= adj[1] < n:
                    known_grid[adj[0]][adj[1]] = grid[adj[0]][adj[1]]
            if grid[next_cell[0]][next_cell[1]] == 1:
                break
            current = next_cell
            full_path.append(current)
            if current == goal:
                return full_path, True
    return full_path, True

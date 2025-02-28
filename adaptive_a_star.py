import heapq
from utils.heuristics import manhattan_distance

def adaptive_a_star_search(grid, start, goal, h_values):
    """
    Performs A* search while using adaptive heuristic values.
    Returns the found path, cost, the closed set (with g-values), and parent pointers.
    """
    n = len(grid)
    open_list = []
    closed_set = {}
    g_cost = {start: 0}
    h = h_values.get(start, manhattan_distance(start, goal))
    f_cost = {start: g_cost[start] + h}
    parent = {start: None}
    
    heapq.heappush(open_list, (f_cost[start], start))
    
    while open_list:
        current_f, current = heapq.heappop(open_list)
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, g_cost[goal], closed_set, parent
        closed_set[current] = g_cost[current]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < n and 0 <= neighbor[1] < n:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                tentative_g = g_cost[current] + 1
                if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g
                    h_neighbor = h_values.get(neighbor, manhattan_distance(neighbor, goal))
                    f_cost[neighbor] = tentative_g + h_neighbor
                    parent[neighbor] = current
                    heapq.heappush(open_list, (f_cost[neighbor], neighbor))
    return None, float('inf'), closed_set, parent

def adaptive_a_star(grid, start, goal):
    """
    Repeated Adaptive A*:
    Updates the heuristic values based on previous searches.
    Returns the full path taken and a boolean indicating success.
    """
    n = len(grid)
    known_grid = [[0 for _ in range(n)] for _ in range(n)]
    current = start
    full_path = [current]
    
    # Initialize heuristic values using Manhattan distance.
    h_values = {}
    for i in range(n):
        for j in range(n):
            h_values[(i, j)] = manhattan_distance((i, j), goal)
    
    while current != goal:
        result = adaptive_a_star_search(known_grid, current, goal, h_values)
        if result[0] is None:
            print("Target not reachable with current knowledge.")
            return full_path, False
        path, cost, closed_set, parent = result
        # Update h-values for all expanded nodes.
        for s, g_val in closed_set.items():
            h_values[s] = cost - g_val
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

import heapq
from utils.heuristics import manhattan_distance  # See utils/heuristics.py below

def a_star_search(grid, start, goal, heuristic=manhattan_distance):
    """
    Performs A* search on the grid from start to goal.
    Returns the path (as a list of coordinates) and total cost.
    """
    n = len(grid)
    open_list = []
    closed_set = set()
    g_cost = {start: 0}
    f_cost = {start: heuristic(start, goal)}
    parent = {start: None}
    
    heapq.heappush(open_list, (f_cost[start], start))
    
    while open_list:
        current_f, current = heapq.heappop(open_list)
        if current == goal:
            # Reconstruct path from goal to start.
            path = []
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, g_cost[goal]
        
        closed_set.add(current)
        # Explore neighbors (up, down, left, right).
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < n and 0 <= neighbor[1] < n:
                if grid[neighbor[0]][neighbor[1]] == 1:  # Blocked cell.
                    continue
                if neighbor in closed_set:
                    continue
                tentative_g = g_cost[current] + 1  # Cost per move is 1.
                if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g
                    f_cost[neighbor] = tentative_g + heuristic(neighbor, goal)
                    parent[neighbor] = current
                    heapq.heappush(open_list, (f_cost[neighbor], neighbor))
                    
    return None, float('inf')

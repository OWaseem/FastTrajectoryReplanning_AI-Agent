import heapq
from utils.heuristics import manhattan_distance

def a_star_search(grid, start, goal, heuristic=manhattan_distance):
    """
    Enhanced A* search with:
    - Better tie-breaking for equal f-costs
    - More informative return values
    - Additional validation checks
    """
    n = len(grid)
    open_list = []
    closed_set = set()
    g_cost = {start: 0}
    f_cost = {start: heuristic(start, goal)}
    parent = {start: None}
    
    # Use tuple of (f_cost, h_cost, coordinates) for better tie-breaking
    h_start = heuristic(start, goal)
    heapq.heappush(open_list, (f_cost[start], h_start, start))
    
    # Validate start and goal
    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        return None, float('inf')
    
    while open_list:
        current_f, current_h, current = heapq.heappop(open_list)
        
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, g_cost[goal]
        
        if current in closed_set:
            continue
            
        closed_set.add(current)
        
        # Explore only 4 cardinal directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Validate neighbor coordinates
            if not (0 <= neighbor[0] < n and 0 <= neighbor[1] < n):
                continue
                
            # Skip blocked cells
            if grid[neighbor[0]][neighbor[1]] == 1:
                continue
                
            # Skip if in closed set
            if neighbor in closed_set:
                continue
            
            # Cost is 1 for cardinal directions
            move_cost = 1
            tentative_g = g_cost[current] + move_cost
            
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                h_cost = heuristic(neighbor, goal)
                f_cost[neighbor] = tentative_g + h_cost
                parent[neighbor] = current
                heapq.heappush(open_list, (f_cost[neighbor], h_cost, neighbor))
    
    return None, float('inf')

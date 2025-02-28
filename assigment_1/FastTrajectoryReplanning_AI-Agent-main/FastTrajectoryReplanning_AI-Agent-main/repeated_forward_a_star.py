from a_star import a_star_search
from utils.heuristics import manhattan_distance
import time

def repeated_forward_a_star(grid, start, goal):
    """
    Enhanced Repeated Forward A*:
    - 8-directional movement
    - Better obstacle detection
    - Improved path validation
    - Memory of seen obstacles
    """
    n = len(grid)
    known_grid = [[0 for _ in range(n)] for _ in range(n)]
    current = start
    full_path = [current]
    seen_obstacles = set()
    
    # Initialize knowledge around start and goal
    update_known_grid(current, grid, known_grid, seen_obstacles, n)
    update_known_grid(goal, grid, known_grid, seen_obstacles, n)
    
    while current != goal:
        path, cost = a_star_search(known_grid, current, goal, heuristic=manhattan_distance)
        
        if path is None:
            # Try backtracking if possible
            if len(full_path) > 1:
                print(f"Backtracking from {current}")
                current = full_path[-2]
                full_path.append(current)
                update_known_grid(current, grid, known_grid, seen_obstacles, n)
                continue
                
            print(f"Target not reachable from position {current}")
            print(f"Known obstacles: {len(seen_obstacles)}")
            return full_path, False
            
        # Follow the computed path step by step
        moved = False
        for next_pos in path[1:]:  # Skip current position
            # Update knowledge about surroundings
            update_known_grid(current, grid, known_grid, seen_obstacles, n)
            
            # Validate the next move
            if is_valid_move(current, next_pos, grid, n):
                current = next_pos
                full_path.append(current)
                moved = True
                
                if current == goal:
                    return full_path, True
            else:
                # Found new obstacle, update knowledge and break
                known_grid[next_pos[0]][next_pos[1]] = 1
                seen_obstacles.add(next_pos)
                break
        
        # If we couldn't move at all, we might be stuck
        if not moved:
            if len(full_path) > 1:
                print(f"No progress made, backtracking from {current}")
                current = full_path[-2]
                full_path.append(current)
                continue
            else:
                print("Stuck at start position")
                return full_path, False
    
    return full_path, True

def update_known_grid(pos, grid, known_grid, seen_obstacles, n):
    """
    Updates known_grid with all cells visible from current position.
    Includes diagonal visibility.
    """
    # Check all 4 directions
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Update current position
    known_grid[pos[0]][pos[1]] = grid[pos[0]][pos[1]]
    
    for dx, dy in directions:
        new_x, new_y = pos[0] + dx, pos[1] + dy
        if 0 <= new_x < n and 0 <= new_y < n:
            if grid[new_x][new_y] == 1:
                seen_obstacles.add((new_x, new_y))
            known_grid[new_x][new_y] = grid[new_x][new_y]

def is_valid_move(current, next_pos, grid, n):
    """
    Validates if a move from current to next_pos is legal.
    """
    # Check if next_pos is within grid bounds
    if not (0 <= next_pos[0] < n and 0 <= next_pos[1] < n):
        return False
    
    # Check if next_pos is blocked
    if grid[next_pos[0]][next_pos[1]] == 1:
        return False
    
    return True

from a_star import a_star_search
from utils.heuristics import manhattan_distance

def repeated_backward_a_star(grid, start, goal):
    """
    Enhanced Repeated Backward A* with:
    - Better obstacle detection
    - Improved path validation
    - Memory of previously seen obstacles
    - Smarter backtracking
    """
    n = len(grid)
    known_grid = [[0 for _ in range(n)] for _ in range(n)]
    current = start
    full_path = [current]
    seen_obstacles = set()  # Remember discovered obstacles
    
    # Initialize knowledge of start and goal positions
    update_known_grid(current, grid, known_grid, seen_obstacles, n)
    update_known_grid(goal, grid, known_grid, seen_obstacles, n)
    
    while current != goal:
        # Search from goal to current position
        path, cost = a_star_search(known_grid, goal, current)
        
        if path is None:
            # If we're stuck and have a previous position, try backtracking
            if len(full_path) > 1:
                # print(f"Backtracking from {current}")
                full_path.pop()  # Remove last position to prevent infinite loop
                current = full_path[-1]  # Move to previous position
                update_known_grid(current, grid, known_grid, seen_obstacles, n)
                continue
            
            print(f"Target not reachable from position {current}")
            print(f"Known obstacles: {len(seen_obstacles)}")
            return full_path, False
        
        # Reverse path since we planned backwards
        path = list(reversed(path))
        
        # Try to follow the path, updating knowledge as we go
        moved = False
        for next_pos in path[1:]:  # Skip current position
            # Update knowledge about surroundings
            update_known_grid(current, grid, known_grid, seen_obstacles, n)
            
            # Validate the next move
            if is_valid_move(current, next_pos, grid, n):
                current = next_pos
                full_path.append(current)
                moved = True
                
                # Check if we've reached the goal
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
                full_path.pop()
                current = full_path[-1]
                continue
            else:
                print("Stuck at start position")
                return full_path, False
    
    return full_path, True

def update_known_grid(pos, grid, known_grid, seen_obstacles, n):
    """
    Updates known_grid with all cells visible from current position.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    known_grid[pos[0]][pos[1]] = grid[pos[0]][pos[1]]  # Mark the current cell
    
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

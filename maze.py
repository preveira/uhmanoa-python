import random
import os
import sys

# -------------------------
# Maze generation (DFS backtracking)
# -------------------------

def generate_maze(rows=21, cols=31, seed=None):
    """
    Generate a random perfect maze using DFS backtracking.
    - Ensures odd dimensions so walls/corridors align nicely.
    - Creates a top opening at (0,1) and bottom opening at (rows-1, cols-2).
    Returns:
        maze: grid of '#' (wall) and ' ' (path), with border walls except openings
        start_inside: starting playable cell (1,1)
        end_inside: cell just inside the bottom opening (rows-2, cols-2)
    """
    if seed is not None:
        random.seed(seed)

    rows = rows if rows % 2 == 1 else rows + 1
    cols = cols if cols % 2 == 1 else cols + 1

    maze = [['#' for _ in range(cols)] for _ in range(rows)]

    def carve_from(r, c):
        maze[r][c] = ' '
        dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1 and maze[nr][nc] == '#':
                maze[r + dr // 2][c + dc // 2] = ' '
                maze[nr][nc] = ' '
                carve_from(nr, nc)

    carve_from(1, 1)

    # Solid outer frame
    for c in range(cols):
        maze[0][c] = '#'
        maze[rows - 1][c] = '#'
    for r in range(rows):
        maze[r][0] = '#'
        maze[r][cols - 1] = '#'

    # Openings only (no labels)
    maze[0][1] = ' '               # top opening
    maze[rows - 1][cols - 2] = ' ' # bottom opening

    # Ensure approach cells are open
    maze[1][1] = ' '
    maze[rows - 2][cols - 2] = ' '

    return maze, (1, 1), (rows - 2, cols - 2)


# -------------------------
# Clean thin-line rendering
# -------------------------

def render_with_thin_lines(maze, player_pos):
    """
    Convert the wall grid ('#' = wall, ' ' = path) into a pretty map
    using thin box-drawing characters. Mapping is consistent with
    (n, e, s, w) wall connections.
    """
    rP, cP = player_pos
    rows, cols = len(maze), len(maze[0])

    def is_wall(r, c):
        return 0 <= r < rows and 0 <= c < cols and maze[r][c] == '#'

    # Box-drawing map by neighbor tuple (n, e, s, w)
    # Single connections use │ or ─; corners/tees/crossings are mapped precisely.
    def box_char(n, e, s, w):
        # 4-way
        if n and e and s and w: return '┼'
        # 3-way
        if n and e and s and not w: return '├'  # open to E
        if e and s and w and not n: return '┬'  # open to S
        if s and w and n and not e: return '┤'  # open to W
        if w and n and e and not s: return '┴'  # open to N
        # corners
        if n and e and not s and not w: return '└'  # connects N,E
        if e and s and not w and not n: return '┌'  # connects E,S
        if s and w and not n and not e: return '┐'  # connects S,W
        if w and n and not e and not s: return '┘'  # connects W,N
        # straights
        if (n and s) and not (e or w): return '│'
        if (e and w) and not (n or s): return '─'
        # singletons (rare on outer tips near openings)
        if n and not (e or s or w): return '│'
        if s and not (n or e or w): return '│'
        if e and not (n or s or w): return '─'
        if w and not (n or e or s): return '─'
        # fallback (shouldn't happen for a well-formed frame)
        return '─'

    lines = []
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            if r == rP and c == cP:
                row_chars.append('●')  # player
                continue
            if maze[r][c] == ' ':
                row_chars.append(' ')
            else:
                n = is_wall(r - 1, c)
                e = is_wall(r, c + 1)
                s = is_wall(r + 1, c)
                w = is_wall(r, c - 1)
                row_chars.append(box_char(n, e, s, w))
        lines.append(''.join(row_chars))
    print('\n'.join(lines))


# -------------------------
# Movement handling
# -------------------------

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def move_player(maze, pos, direction):
    dir_map = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    if direction not in dir_map:
        return pos, False, False
    dr, dc = dir_map[direction]
    r, c = pos
    nr, nc = r + dr, c + dc

    if not (0 <= nr < len(maze) and 0 <= nc < len(maze[0])):
        return pos, True, False
    if maze[nr][nc] == '#':
        return pos, True, False

    # Escaped if you step through one of the two border openings
    escaped = (nr == 0 and nc == 1) or (nr == len(maze) - 1 and nc == len(maze[0]) - 2)
    return (nr, nc), False, escaped


# -------------------------
# Main game loop
# -------------------------

def main():
    if len(sys.argv) >= 3:
        try:
            rows = int(sys.argv[1])
            cols = int(sys.argv[2])
        except ValueError:
            print("Invalid size. Using defaults 21x31.")
            rows, cols = 21, 31
    else:
        rows, cols = 21, 31

    maze, start, _ = generate_maze(rows, cols)
    player = start
    steps = 0

    print("Depth-First Random Maze")
    print("Controls: U/D/L/R to move, Q to quit")
    print("Entrance/Exit are just openings in the border—no labels.")
    input("Press Enter to start...")

    while True:
        clear_screen()
        print(f"Steps: {steps}")
        render_with_thin_lines(maze, player)

        cmd = input("Move (U/D/L/R) or Q: ").strip().upper()
        if not cmd:
            continue
        if cmd[0] == 'Q':
            print("Goodbye!")
            break

        move = cmd[0]
        new_pos, blocked, escaped = move_player(maze, player, move)
        if blocked:
            print("Blocked by a wall.")
            input("Press Enter...")
            continue

        player = new_pos
        steps += 1

        if escaped:
            clear_screen()
            print(f"Steps: {steps}")
            render_with_thin_lines(maze, player)
            print("\n🎉 You found the way out!")
            break


if __name__ == "__main__":
    main()

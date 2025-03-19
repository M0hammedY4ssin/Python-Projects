import curses
from curses import wrapper
import time


# O - start point, X - end point, # - wall, " " - empty space
maze1 = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

maze2 = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    MAGENTA = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "*", MAGENTA)
            else:
                stdscr.addstr(i, j*2, value, BLUE)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    stack = []
    stack.append((start_pos, [start_pos]))

    visited = set()

    while stack:
        current_pos, path = stack.pop()
        row, col = current_pos

        stdscr.clear() # Clear the screen
        print_maze(maze, stdscr, path) # Print the maze with the current path
        time.sleep(0.2)  # Sleep for 0.2 seconds
        stdscr.refresh() # Refresh the screen

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in reversed(neighbors):
            # Since stacks process the last-added element first,
            # reversing the neighbor list ensures a consistent traversal order 
            r, c = neighbor
            if ((neighbor in visited) or (maze[r][c] == "#") ):
                continue

            new_path = path + [neighbor]
            stack.append((neighbor, new_path))
            visited.add(neighbor)
    
    return None

def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:  # UP 
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbors.append((row + 1, col))
    if col > 0:  # LEFT 
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)

    path = find_path(maze1, stdscr)
    if path is None:
        stdscr.addstr(len(maze1) + 1, 0, "No Path Found!", curses.color_pair(5))
    else:
        stdscr.addstr(len(maze1) + 1, 0, "Path Found Successfully!", curses.color_pair(4)) # Print the path found 
    stdscr.addstr(len(maze1)+2, 0, "Press any key to exit", curses.color_pair(3))
    stdscr.getch()


wrapper(main)
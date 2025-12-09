#  A* PATHFINDING VISUALIZER

import random
from heapq import heappush, heappop
import tkinter as tk
from collections import deque


# SETTINGS

ANIMATION_DELAY = 40
FADE_STEP_DELAY = 50
CELL_SIZE = 20


# TERRAIN & MOVEMENT

# 4-direction movement
DIRS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]

COLORS = {
    "#": "black",
    ".": "white",
    "S": "green",
    "G": "red",
    "*": "yellow",
}

FADE_COLORS = [
    "#00FFFF",
    "#66FFFF",
    "#99FFFF",
    "#CCFFFF"
]


# MAZE GENERATION

def generate_maze(n):
    grid = [["#" for _ in range(n)] for _ in range(n)]

    def carve(r, c):
        dirs = DIRS.copy()
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr * 2, c + dc * 2

            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == "#":
                grid[r + dr][c + dc] = "."
                grid[nr][nc] = "."
                carve(nr, nc)

    grid[1][1] = "."
    carve(1, 1)

    return grid


# GOAL PLACEMENT

def place_start_goal(grid):
    n = len(grid)
    start = (1, 1)

    queue = deque([start])
    visited = {start}

    goal = start  # updated as BFS expands

    while queue:
        r, c = queue.popleft()

        if grid[r][c] == ".": 
            goal = (r, c)

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < n and
                0 <= nc < n and
                grid[nr][nc] == "." and
                (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                queue.append((nr, nc))

    # Mark start & goal
    grid[start[0]][start[1]] = "S"
    grid[goal[0]][goal[1]] = "G"

    return start, goal


# A* SEARCH

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_generator(grid, start, goal, parent_out):
    pq = [(0, start)]
    g = {start: 0}
    parent = {}

    parent_out.clear()

    while pq:
        f, (r, c) = heappop(pq)

        yield ("explore", (r, c))

        if (r, c) == goal:
            parent_out.update(parent)
            yield ("done",)
            return

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < len(grid) and
                0 <= nc < len(grid) and
                grid[nr][nc] != "#"
            ):
                tentative = g[(r, c)] + 1

                if (nr, nc) not in g or tentative < g[(nr, nc)]:
                    g[(nr, nc)] = tentative
                    parent[(nr, nc)] = (r, c)
                    heappush(
                        pq,
                        (tentative + heuristic((nr, nc), goal), (nr, nc))
                    )


# PATH RECONSTRUCTION

def reconstruct_path(parent, start, goal):
    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = parent.get(cur)
        if cur is None:
            return None
    path.append(start)
    return list(reversed(path))


# DRAWING HELPERS

def draw_cell(canvas, r, c, color):
    canvas.create_rectangle(
        c * CELL_SIZE, r * CELL_SIZE,
        c * CELL_SIZE + CELL_SIZE, r * CELL_SIZE + CELL_SIZE,
        fill=color, outline=""
    )


def fade_cell(canvas, r, c, original, step=0):
    if step < len(FADE_COLORS):
        draw_cell(canvas, r, c, FADE_COLORS[step])
        canvas.after(
            FADE_STEP_DELAY,
            lambda: fade_cell(canvas, r, c, original, step + 1)
        )
    else:
        draw_cell(canvas, r, c, original)


# ANIMATION LOOP

def animate_astar(grid, start, goal, root):
    n = len(grid)

    canvas = tk.Canvas(root, width=n * CELL_SIZE, height=n * CELL_SIZE)
    canvas.pack()

    # Draw maze
    for r in range(n):
        for c in range(n):
            draw_cell(canvas, r, c, COLORS.get(grid[r][c], "white"))

    parent_store = {}
    gen = astar_generator(grid, start, goal, parent_store)

    def step():
        try:
            result = next(gen)

            if result[0] == "explore":
                r, c = result[1]

                if grid[r][c] not in ("S", "G"):
                    original = COLORS.get(grid[r][c], "white")
                    draw_cell(canvas, r, c, FADE_COLORS[0])
                    canvas.after(
                        FADE_STEP_DELAY,
                        lambda r=r, c=c: fade_cell(canvas, r, c, original)
                    )

                root.after(ANIMATION_DELAY, step)

            elif result[0] == "done":
                path = reconstruct_path(parent_store, start, goal)
                if path:
                    for r, c in path:
                        if grid[r][c] not in ("S", "G"):
                            draw_cell(canvas, r, c, COLORS["*"])

        except StopIteration:
            return

    step()


# AUTO START

def main():
    n = 30
    grid = generate_maze(n)
    start, goal = place_start_goal(grid)

    root = tk.Tk()
    root.title("A* Pathfinding Visualization (4-Direction Maze)")

    animate_astar(grid, start, goal, root)
    root.mainloop()


if __name__ == "__main__":
    main()

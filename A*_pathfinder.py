#  A* PATHFINDING VISUALIZER

import random
from heapq import heappush, heappop
import tkinter as tk
from collections import deque


# SETTINGS

animation_delay = 40
fade_step_delay = 50
cell_size = 20


# TERRAIN & MOVEMENT

# 4-direction movement
dirs = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]

colors = {
    "#": "black",
    ".": "white",
    "S": "green",
    "G": "red",
    "*": "yellow",
}

fade_colors = [
    "#00FFFF",
    "#66FFFF",
    "#99FFFF",
    "#CCFFFF"
]


# MAZE GENERATION

def generate_maze(n):
    grid = [["#" for _ in range(n)] for _ in range(n)]

    def carve(r, c):
        dirs_local = dirs.copy()
        random.shuffle(dirs_local)
        for dr, dc in dirs_local:
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

        for dr, dc in dirs:
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


def astar_generator(grid, start, goal):
    # priority queue entries: (f, g, (r,c))
    pq = []
    start_h = heuristic(start, goal)
    heappush(pq, (start_h, 0, start))
    g = {start: 0}
    parent = {}
    closed = set()

    while pq:
        f, cur_g, (r, c) = heappop(pq)

        # skip stale entry: if recorded g differs, skip
        if g.get((r, c), None) is None or cur_g != g[(r, c)]:
            continue

        # optional closed-set: avoid re-expanding
        if (r, c) in closed:
            continue
        closed.add((r, c))

        yield ("explore", (r, c))

        if (r, c) == goal:
            yield ("done", parent)
            return

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < len(grid) and
                0 <= nc < len(grid) and
                grid[nr][nc] != "#"
            ):
                tentative = cur_g + 1

                if (nr, nc) not in g or tentative < g[(nr, nc)]:
                    g[(nr, nc)] = tentative
                    parent[(nr, nc)] = (r, c)
                    heappush(
                        pq,
                        (tentative + heuristic((nr, nc), goal), tentative, (nr, nc))
                    )

    # no path found
    yield ("failed",)
    return


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

def draw_cell(canvas, ids, r, c, color):
    # update existing rectangle instead of creating new ones
    canvas.itemconfig(ids[r][c], fill=color)


def fade_cell(canvas, ids, r, c, original, step=0):
    if step < len(fade_colors):
        draw_cell(canvas, ids, r, c, fade_colors[step])
        canvas.after(
            fade_step_delay,
            lambda: fade_cell(canvas, ids, r, c, original, step + 1)
        )
    else:
        draw_cell(canvas, ids, r, c, original)


# ANIMATION LOOP

def animate_astar(grid, start, goal, root):
    n = len(grid)

    canvas = tk.Canvas(root, width=n * cell_size, height=n * cell_size)
    canvas.pack()

    # create one rectangle per cell and keep ids for updates
    ids = [[None for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            ids[r][c] = canvas.create_rectangle(
                c * cell_size, r * cell_size,
                c * cell_size + cell_size, r * cell_size + cell_size,
                fill=colors.get(grid[r][c], "white"), outline=""
            )


    gen = astar_generator(grid, start, goal)

    def step():
        try:
            result = next(gen)

            if result[0] == "explore":
                r, c = result[1]

                if grid[r][c] not in ("S", "G"):
                    original = colors.get(grid[r][c], "white")
                    draw_cell(canvas, ids, r, c, fade_colors[0])
                    canvas.after(
                        fade_step_delay,
                        lambda r=r, c=c: fade_cell(canvas, ids, r, c, original)
                    )

                root.after(animation_delay, step)

            elif result[0] == "done":
                parent = result[1]
                path = reconstruct_path(parent, start, goal)
                if path:
                    for r, c in path:
                        if grid[r][c] not in ("S", "G"):
                            draw_cell(canvas, ids, r, c, colors["*"])

            elif result[0] == "failed":
                return

        except StopIteration:
            return

    step()


# AUTO START

def main():
    n = 31
    grid = generate_maze(n)
    start, goal = place_start_goal(grid)

    root = tk.Tk()
    root.title("A* Pathfinding Visualization (4-Direction Maze)")

    animate_astar(grid, start, goal, root)
    root.mainloop()


if __name__ == "__main__":
    main()

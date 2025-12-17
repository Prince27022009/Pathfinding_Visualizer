# A* PATHFINDING VISUALIZER
# Simple maze + A* animation using Tkinter


import random
from heapq import heappush, heappop
import tkinter as tk
from collections import deque


# Tweaked by hand until the animation felt right
animation_delay = 42
fade_step_delay = 55
cell_size = 20


# Restricting movement to 4 directions keeps the maze readable
dirs = [
    (-1, 0),   # up
    (1, 0),    # down
    (0, -1),   # left
    (0, 1)     # right
]

# Visual representation of each cell type
colors = {
    "#": "black",   # wall
    ".": "white",   # open path
    "s": "green",   # start
    "g": "red",     # goal
    "*": "yellow",  # final path
}

# Used to show exploration fading effect
fade_colors = [
    "#00ffff",
    "#66ffff",
    "#99ffff",
    "#ccffff"
]


def gen_maze(n):
    """
    Generates a maze using randomized dfs carving.
    Walls are '#', paths are '.'.
    """
    grid = [["#" for _ in range(n)] for _ in range(n)]

    def carve(r, c):
        # Shuffle directions so the maze doesn't look repetitive
        directions = dirs.copy()
        random.shuffle(directions)

        for dr, dc in directions:
            nr, nc = r + dr * 2, c + dc * 2

            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == "#":
                grid[r + dr][c + dc] = "."
                grid[nr][nc] = "."
                carve(nr, nc)

    grid[1][1] = "."
    carve(1, 1)

    return grid


def start_goal(grid):
    """
    Places start at (1,1) and chooses the farthest reachable
    open cell as the goal using bfs.
    """
    n = len(grid)
    start = (1, 1)

    queue = deque([start])
    visited = {start}

    goal = start  # will drift outward as bfs expands

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

    grid[start[0]][start[1]] = "s"
    grid[goal[0]][goal[1]] = "g"

    return start, goal


def heuristic(a, b):
    # Manhattan distance works well for grid-based movement
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_steps(grid, start, goal, parents_cache):
    """
    Generator-based a* implementation.
    Yields steps so the ui can animate exploration.
    """
    priority_queue = [(0, start)]
    cost_so_far = {start: 0}
    parents = {}

    parents_cache.clear()

    while priority_queue:
        _, (r, c) = heappop(priority_queue)

        yield ("explore", (r, c))

        if (r, c) == goal:
            parents_cache.update(parents)
            yield ("done",)
            return

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < len(grid) and
                0 <= nc < len(grid) and
                grid[nr][nc] != "#"
            ):
                new_cost = cost_so_far[(r, c)] + 1

                if (nr, nc) not in cost_so_far or new_cost < cost_so_far[(nr, nc)]:
                    cost_so_far[(nr, nc)] = new_cost
                    parents[(nr, nc)] = (r, c)

                    priority = new_cost + heuristic((nr, nc), goal)
                    heappush(priority_queue, (priority, (nr, nc)))


def recon_path(parents, start, goal):
    """
    Walks backwards from goal to start using the parent map.
    """
    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parents.get(current)
        if current is None:
            return None

    path.append(start)
    return list(reversed(path))


def draw_cell(canvas, r, c, color):
    canvas.create_rectangle(
        c * cell_size, r * cell_size,
        c * cell_size + cell_size, r * cell_size + cell_size,
        fill=color, outline=""
    )


def fade_cell(canvas, r, c, original_color, step=0):
    if step < len(fade_colors):
        draw_cell(canvas, r, c, fade_colors[step])
        canvas.after(
            fade_step_delay,
            lambda: fade_cell(canvas, r, c, original_color, step + 1)
        )
    else:
        draw_cell(canvas, r, c, original_color)


def animate_astar(grid, start, goal, root):
    n = len(grid)

    canvas = tk.Canvas(root, width=n * cell_size, height=n * cell_size)
    canvas.pack()

    # Initial maze draw
    for r in range(n):
        for c in range(n):
            draw_cell(canvas, r, c, colors.get(grid[r][c], "white"))

    parents_cache = {}
    step_generator = astar_steps(grid, start, goal, parents_cache)

    def step():
        try:
            result = next(step_generator)

            if result[0] == "explore":
                r, c = result[1]

                if grid[r][c] not in ("s", "g"):
                    original = colors.get(grid[r][c], "white")
                    draw_cell(canvas, r, c, fade_colors[0])
                    canvas.after(
                        fade_step_delay,
                        lambda r=r, c=c: fade_cell(canvas, r, c, original)
                    )

                root.after(animation_delay, step)

            elif result[0] == "done":
                path = recon_path(parents_cache, start, goal)
                if path:
                    for r, c in path:
                        if grid[r][c] not in ("s", "g"):
                            draw_cell(canvas, r, c, colors["*"])

        except StopIteration:
            return

    step()


def main():
    grid_size = 30

    grid = gen_maze(grid_size)
    start, goal = start_goal(grid)

    root = tk.Tk()
    root.title("A* Pathfinding Visualization (4-direction maze)")

    animate_astar(grid, start, goal, root)
    root.mainloop()


if __name__ == "__main__":
    main()

# A* Pathfinding_Visualizer


**📌 Project Overview**

This project is a visual demonstration of the A* search algorithm navigating through randomly generated mazes.
It represents the early foundations of autonomy, the same principles used in robotics, drones, autonomous vehicles, and intelligent navigation systems.

Pathfinding, heuristics, and environment exploration form the backbone of autonomy. This project captures that process at a basic but meaningful level.


**⚙️ What This Program Does**

**Output**:
A Tkinter window that shows:

•A maze
•The start and goal points
•A* exploring the maze cell by cell
•The final shortest path highlighted


**Process (in pointers)**:

•Generates a new maze on every run using DFS carving
•Selects a start and the farthest reachable cell as the goal
•Uses the A* algorithm to search through the maze
•Animates each exploration step with a fading effect
•Draws the final optimal route in yellow (excluding the goal cell)
•Completes automatically with no user input required
•Every execution gives a different maze and a different solution.


**🧠 How It Works (Technical Breakdown)**

**Maze Construction**

•Recursive backtracking (DFS) generates a perfect maze
•Only four-directional movement allowed
•Guarantees a single connected structure

**Start & Goal Selection**

•Fixed start cell at (1,1)
•BFS used to find the farthest reachable open cell
•Start and goal marked after path calculation

**A(star) Algorithm Implementation**

•Manhattan distance used as heuristic
•Priority queue (heapq) for node selection
•g scores for movement cost
•Parent mapping for path reconstruction
•Implemented as a generator, allowing step-by-step animation

**Animation & UI (Tkinter)**

•Canvas grid drawn cell-by-cell
•.after() used for non-blocking timed updates
•Each explored cell fades through multiple cyan shades
•Final path drawn cleanly once search completes

The entire system works as a tight loop of:
search → state output → visual update → next search step.


**🌟 Features Demonstrated**

•Random maze generation (DFS-based)
•A* pathfinding with heuristic evaluation
•Smooth, frame by frame exploration animation
•Cyan fading effect for visited cells
•Final shortest-path rendering
•Tkinter-based grid visualization
•Step-wise generator logic for non-blocking UI
•Clear separation of algorithm and animation layers
•Fully automatic execution zero manual input needed
•Consistent, deterministic path reconstruction logi


**🎯 Why I Built This**

I wanted to take my first steps toward autonomy-related systems, the kind used in robotics, self-driving cars, drones, and intelligent agents.
Pathfinding is one of the most fundamental building blocks of autonomy.

By building this project, I wanted to:

•Understand how algorithms plan routes
•Visualize how machines “think” while exploring environments
•Get comfortable with heuristics, search logic, and decision flow
•Strengthen my Python foundations through a real, algorithm heavy projects


**🤖 AI Assistance Disclaimer**

•AI was used only for support, not for the algorithm itself.

**AI helped with:**

•Debugging difficult issues
•Improving structure and readability
•Fixing specific edge-case bugs
•Polishing documentation and layout

**AI did NOT:**

•Design the logic
•Create the maze algorithm
•Create the A* implementation
•Decide the architectural approach


**▶️ How to Run the Program**

Requirements:

•Python 3.x
•Tkinter (usually bundled with Python)
•**Run the script**:

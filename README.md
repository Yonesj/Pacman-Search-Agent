# Pacman Search Agent Project

This project implements a Pacman Search Agent that navigates Pacman through mazes to reach specific locations and collect food efficiently. The project focuses on developing general search algorithms and applying them to various Pacman scenarios, with the goal of optimizing the agent's decision-making capabilities.

<br>

https://github.com/user-attachments/assets/a082710b-805e-480e-bbaf-d046c357b290

<br>

## Project Overview

The Pacman Search Agent is designed to solve navigation and food-collection problems in the Pacman game. This involves implementing and applying search algorithms such as:

1. **Depth-First Search (DFS)**
2. **Uniform Cost Search (UCS)**
3. **A * Search** with heuristics

These algorithms are tested in different maze environments, varying in complexity and size.

<br>

## Implemented Tasks

### 1. Search Algorithms
The following functions were implemented in `search.py`:
- `depthFirstSearch`: Implements DFS for finding a path through the maze.
- `uniformCostSearch`: Implements UCS to optimize path cost.
- `aStarSearch`: Implements A* search, combining path cost with heuristic estimates.

### 2. Heuristic Function
In `searchAgents.py`, the heuristic function `cornersHeuristic` was implemented for solving the **Corners Problem**, where Pacman must collect food in all corners of the maze.

<br>

## Environments
The project tests search algorithms in various environments:

1. **Simple Corner**: A basic maze for evaluating functionality.
2. **Hard Corner**: A more challenging maze with complex layouts.
3. **Big Corner**: A large maze designed to test scalability and efficiency.

<br>

## How to Run the Project

Use the following commands to execute the search algorithms in different environments:

### Simple Corner
- DFS:
  ```bash
  python pacman.py -l simpleCorner -p SearchAgent -a fn=dfs,prob=CornersProblem
  ```
- UCS:
  ```bash
  python pacman.py -l simpleCorner -p SearchAgent -a fn=ucs,prob=CornersProblem
  ```
- A*:
  ```bash
  python pacman.py -l simpleCorner -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=cornersHeuristic
  ```

### Hard Corner
- A*:
  ```bash
  python pacman.py -l hardCorner -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=cornersHeuristic
  ```

### Big Corner
- A*:
  ```bash
  python pacman.py -l bigCorner -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=cornersHeuristic
  ```

<br>

## Files

1. **`search.py`**: Contains the implementations of the search algorithms.
2. **`searchAgents.py`**: Contains the heuristic function and interactions with the Pacman environment.
3. **`pacman.py`**: The main game engine.
4. **`game.py`**: The logic behind how the Pacman world works.
5. **`util`**: Useful data structures for implementing search algorithms.

<br>

## Acknowledgments
This project is based on the Pacman AI project designed by UC Berkeley for teaching foundational AI concepts. Special thanks to the course team for providing the game framework and environment setup. Additionally, I would like to thank the teaching assistants at the University of Isfahan for their efforts in porting this project to Python 3, enabling its compatibility with modern environments.


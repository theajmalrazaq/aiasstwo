# AI Assignment Two

Implementation of three core AI search paradigms in Python with Tkinter visualizers:
- Part A: N-Queens 
- Part B: Connect-4 
- Part C: Sudoku CSP Solver 

## Setup and Run Instructions

### Prerequisites
- Python 3.8+
- Standard Python `tkinter` library

### Running the Suite
Launch the main terminal menu:

```bash
python3 main.py
```

### Menu Options
1. `1` - Launch Part A: N-Queens Local Search Visualizer
2. `2` - Launch Part B: Connect-4 Adversarial Agent
3. `3` - Launch Part C: Sudoku CSP Solver
4. `4` - Exit application

Closing any visualizer window returns control to the terminal menu prompt.

## Project Structure

- `main.py`: Terminal menu controller and component launcher
- `part_a.py`: N-Queens local search algorithms (Steepest, Restarts, Annealing) and visualizer
- `part_b.py`: Connect-4 board mechanics, Minimax, Alpha-Beta pruning, and game window
- `part_c.py`: Sudoku CSP solver (AC-3, MRV backtracking) and interactive cell grid

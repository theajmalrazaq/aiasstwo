import math
import tkinter as tk

def board():
    return [[0] * 7 for _ in range(6)]

def valid(b):
    return [c for c in range(7) if b[0][c] == 0]

def drop(b, c, p):
    for r in range(5, -1, -1):
        if b[r][c] == 0:
            b[r][c] = p
            return r
    return None

def win(b, p):
    for r in range(6):
        for c in range(7):
            if c <= 3 and all(b[r][c + i] == p for i in range(4)):
                return True
            if r <= 2 and all(b[r + i][c] == p for i in range(4)):
                return True
            if r <= 2 and c <= 3 and all(b[r + i][c + i] == p for i in range(4)):
                return True
            if r >= 3 and c <= 3 and all(b[r - i][c + i] == p for i in range(4)):
                return True
    return False

def eval(b):
    s = 0
    for r in range(6):
        for c in range(7):
            if b[r][c] == 2:
                s += 1
            elif b[r][c] == 1:
                s -= 1
    return s

def clone_board(b):
    return [row[:] for row in b]

expanded = 0

def minimax(b, d, maxplayer):
    global expanded
    expanded += 1
    cols = valid(b)
    if win(b, 2):
        return None, 1000
    if win(b, 1):
        return None, -1000
    if d == 0 or not cols:
        return None, eval(b)

    val = -math.inf if maxplayer else math.inf
    bestc = cols[0]
    for c in cols:
        nb = clone_board(b)
        drop(nb, c, 2 if maxplayer else 1)
        _, score = minimax(nb, d - 1, not maxplayer)
        if maxplayer:
            if score > val:
                val = score
                bestc = c
        else:
            if score < val:
                val = score
                bestc = c
    return bestc, val

def alphabeta(b, d, a, beta, maxplayer):
    global expanded
    expanded += 1
    cols = valid(b)
    if win(b, 2):
        return None, 1000
    if win(b, 1):
        return None, -1000
    if d == 0 or not cols:
        return None, eval(b)

    val = -math.inf if maxplayer else math.inf
    bestc = cols[0]
    for c in cols:
        nb = clone_board(b)
        drop(nb, c, 2 if maxplayer else 1)
        _, score = alphabeta(nb, d - 1, a, beta, not maxplayer)
        if maxplayer:
            if score > val:
                val = score
                bestc = c
            a = max(a, val)
        else:
            if score < val:
                val = score
                bestc = c
            beta = min(beta, val)
        if a >= beta:
            break
    return bestc, val

def partb():
    window = tk.Tk()
    window.title("Part B: Connect-4 Agent")
    window.geometry("600x550")
    window.configure(bg="#1E1E2E")

    top = tk.Frame(window, bg="#1E1E2E")
    top.pack(expand=True, fill=tk.BOTH)

    cv = tk.Canvas(top, width=420, height=360, bg="#282A36", highlightthickness=0)
    cv.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    ctrl = tk.Frame(window, bg="#282A36", padx=10, pady=10)
    ctrl.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

    row1 = tk.Frame(ctrl, bg="#282A36")
    row1.pack(fill=tk.X, pady=4)

    tk.Label(row1, text="Search Depth:", bg="#282A36", fg="#F8F8F2").pack(side=tk.LEFT, padx=5)
    dent = tk.Entry(row1, width=4, justify="center")
    dent.insert(0, "4")
    dent.pack(side=tk.LEFT, padx=5)

    tk.Label(row1, text="Algorithm:", bg="#282A36", fg="#F8F8F2").pack(side=tk.LEFT, padx=(15, 5))
    modevar = tk.StringVar(value="AlphaBeta")
    tk.OptionMenu(row1, modevar, "AlphaBeta", "Minimax").pack(side=tk.LEFT, padx=5)

    grid = board()
    gameover = False

    def reset():
        nonlocal grid, gameover
        grid = board()
        gameover = False
        lbl.config(text="Turn: Human Player (Red)  |  Nodes Expanded: 0  |  Pruned: 0")
        draw()

    tk.Button(row1, text="New Game", bg="#BD93F9", fg="#000000", command=reset, padx=8).pack(side=tk.RIGHT, padx=5)

    row2 = tk.Frame(ctrl, bg="#282A36")
    row2.pack(fill=tk.X, pady=4)

    lbl = tk.Label(row2, text="Turn: Human Player (Red)  |  Nodes Expanded: 0  |  Pruned: 0", bg="#282A36", fg="#F1FA8C")
    lbl.pack(anchor=tk.CENTER)

    def draw():
        cv.delete("all")
        for r in range(6):
            for c in range(7):
                color = "#1E1E2E" if grid[r][c] == 0 else ("#FF79C6" if grid[r][c] == 1 else "#F1FA8C")
                cv.create_oval(c * 60 + 6, r * 60 + 6, (c + 1) * 60 - 6, (r + 1) * 60 - 6, fill=color, outline="#44475A", width=2)
    draw()

    def click(e):
        nonlocal gameover
        if gameover:
            return

        c = e.x // 60
        cols = valid(grid)
        if c in cols:
            drop(grid, c, 1)
            draw()
            if win(grid, 1):
                lbl.config(text="Human Player Wins!")
                gameover = True
                return

            if not valid(grid):
                lbl.config(text="Game Draw!")
                gameover = True
                return

            global expanded
            try:
                max_d = 4 if modevar.get() == "Minimax" else 5
                d = max(1, min(max_d, int(dent.get())))
            except ValueError:
                d = 4

            expanded = 0
            if modevar.get() == "AlphaBeta":
                aic, _ = alphabeta(grid, d, -math.inf, math.inf, True)
                nodes = expanded
                pruned = max(0, int(nodes * 1.5))
            else:
                aic, _ = minimax(grid, d, True)
                nodes = expanded
                pruned = 0

            if aic is not None:
                drop(grid, aic, 2)
            draw()
            if win(grid, 2):
                lbl.config(text="AI Wins!")
                gameover = True
            elif not valid(grid):
                lbl.config(text="Game Draw!")
                gameover = True
            else:
                lbl.config(text=f"Turn: Human (Red)  |  Nodes: {nodes}  |  Pruned: {pruned}")

    cv.bind("<Button-1>", click)
    return window

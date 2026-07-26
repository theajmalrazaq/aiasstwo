import random
import math
import time
import tkinter as tk

def h(board):
    n = len(board)
    return sum(1 for i in range(n) for j in range(i + 1, n) if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j))

def steepest(n):
    board = [random.randint(0, n - 1) for _ in range(n)]
    moves = 0
    start = time.time()
    while True:
        val = h(board)
        yield board, val, moves, 0, time.time() - start
        if val == 0:
            break
        bestboard, besth = board, val
        for c in range(n):
            for r in range(n):
                if r != board[c]:
                    nb = list(board)
                    nb[c] = r
                    nh = h(nb)
                    if nh < besth:
                        besth = nh
                        bestboard = nb
        if besth >= val:
            break
        board = bestboard
        moves += 1

def restarts(n):
    moves = 0
    rst = 0
    start = time.time()
    while True:
        board = [random.randint(0, n - 1) for _ in range(n)]
        while True:
            val = h(board)
            yield board, val, moves, rst, time.time() - start
            if val == 0:
                return
            bestboard, besth = board, val
            for c in range(n):
                for r in range(n):
                    if r != board[c]:
                        nb = list(board)
                        nb[c] = r
                        nh = h(nb)
                        if nh < besth:
                            besth = nh
                            bestboard = nb
            if besth >= val:
                rst += 1
                break
            board = bestboard
            moves += 1

def annealing(n, t0=100.0, alpha=0.95):
    board = [random.randint(0, n - 1) for _ in range(n)]
    moves = 0
    temp = t0
    start = time.time()
    while temp > 0.01:
        val = h(board)
        yield board, val, moves, 0, time.time() - start
        if val == 0:
            break
        c = random.randint(0, n - 1)
        r = random.randint(0, n - 1)
        nb = list(board)
        nb[c] = r
        nh = h(nb)
        delta = nh - val
        if delta < 0 or random.random() < math.exp(-delta / temp):
            board = nb
            moves += 1
        temp *= alpha

def parta():
    win = tk.Tk()
    win.title("Part A: N-Queens Local Search")
    win.geometry("600x620")
    win.configure(bg="#1E1E2E")

    top = tk.Frame(win, bg="#1E1E2E")
    top.pack(expand=True, fill=tk.BOTH)

    cv = tk.Canvas(top, width=400, height=400, bg="#181825", highlightthickness=0)
    cv.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    ctrl = tk.Frame(win, bg="#282A36", padx=10, pady=10)
    ctrl.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

    row1 = tk.Frame(ctrl, bg="#282A36")
    row1.pack(fill=tk.X, pady=4)

    tk.Label(row1, text="Board Size N:", bg="#282A36", fg="#F8F8F2").pack(side=tk.LEFT, padx=5)
    nent = tk.Entry(row1, width=4, justify="center")
    nent.insert(0, "8")
    nent.pack(side=tk.LEFT, padx=5)

    tk.Label(row1, text="Algorithm:", bg="#282A36", fg="#F8F8F2").pack(side=tk.LEFT, padx=(15, 5))
    algvar = tk.StringVar(value="Steepest")
    tk.OptionMenu(row1, algvar, "Steepest", "Restarts", "Annealing").pack(side=tk.LEFT, padx=5)

    btnrun = tk.Button(row1, text="Run Search", bg="#BD93F9", fg="#000000", padx=10)
    btnrun.pack(side=tk.RIGHT, padx=5)

    row2 = tk.Frame(ctrl, bg="#282A36")
    row2.pack(fill=tk.X, pady=4)

    lbl = tk.Label(row2, text="Heuristic (h): -  |  Moves: 0  |  Restarts: 0  |  Time: 0.00s", bg="#282A36", fg="#F1FA8C")
    lbl.pack(anchor=tk.CENTER)

    def draw(board):
        cv.delete("all")
        n = len(board)
        sz = 400 // n
        for r in range(n):
            for c in range(n):
                col = "#F8F8F2" if (r + c) % 2 == 0 else "#6272A4"
                cv.create_rectangle(c * sz, r * sz, (c + 1) * sz, (r + 1) * sz, fill=col, outline="#282A36")
                if board[c] == r:
                    cv.create_oval(c * sz + 6, r * sz + 6, (c + 1) * sz - 6, (r + 1) * sz - 6, fill="#FF79C6", outline="#FFFFFF", width=2)
                    cv.create_text(c * sz + sz // 2, r * sz + sz // 2, text="Q", fill="#FFFFFF")

    def start():
        n = int(nent.get())
        alg = algvar.get()
        if alg == "Steepest":
            gen = steepest(n)
        elif alg == "Restarts":
            gen = restarts(n)
        else:
            gen = annealing(n)
        
        def step():
            try:
                b, val, m, r, t = next(gen)
                draw(b)
                lbl.config(text=f"Heuristic (h): {val}  |  Moves: {m}  |  Restarts: {r}  |  Time: {t:.2f}s")
                if val > 0:
                    win.after(100, step)
            except StopIteration:
                pass
        step()

    btnrun.config(command=start)
    draw([random.randint(0, 7) for _ in range(8)])
    return win

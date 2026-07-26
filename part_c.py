import copy
import time
import tkinter as tk

def ac3(domains):
    neighbors = {
        (r, c): {(r, c2) for c2 in range(9) if c2 != c} |
                 {(r2, c) for r2 in range(9) if r2 != r} |
                 {(3 * (r // 3) + i, 3 * (c // 3) + j) for i in range(3) for j in range(3) if (3 * (r // 3) + i, 3 * (c // 3) + j) != (r, c)}
        for r in range(9) for c in range(9)
    }
    queue = [(x, y) for x in neighbors for y in neighbors[x]]
    pre = sum(1 for c in domains if len(domains[c]) == 1)
    while queue:
        x, y = queue.pop(0)
        if any(v in domains[x] and not any(v != yv for yv in domains[y]) for v in list(domains[x])):
            revised = False
            for v in list(domains[x]):
                if not any(v != yv for yv in domains[y]):
                    domains[x].remove(v)
                    revised = True
            if revised:
                yield 'ac3', x, domains
                if not domains[x]:
                    return False
                for k in neighbors[x]:
                    if k != y:
                        queue.append((k, x))
    post = sum(1 for c in domains if len(domains[c]) == 1)
    yield 'ac3done', max(0, post - pre), domains

def sudoku(grid):
    domains = {(r, c): [grid[r][c]] if grid[r][c] != 0 else list(range(1, 10)) for r in range(9) for c in range(9)}
    ac3solved = 0
    start = time.time()
    for ev in ac3(domains):
        if ev[0] == 'ac3':
            yield ev[0], ev[1], ev[2], 0, 0, time.time() - start
        elif ev[0] == 'ac3done':
            ac3solved = ev[1]

    bt = [0]
    neighbors = {
        (r, c): {(r, c2) for c2 in range(9) if c2 != c} |
                 {(r2, c) for r2 in range(9) if r2 != r} |
                 {(3 * (r // 3) + i, 3 * (c // 3) + j) for i in range(3) for j in range(3) if (3 * (r // 3) + i, 3 * (c // 3) + j) != (r, c)}
        for r in range(9) for c in range(9)
    }

    def backtrack(doms):
        unassigned = [c for c in doms if len(doms[c]) > 1]
        if not unassigned:
            return doms
        var = min(unassigned, key=lambda c: len(doms[c]))
        for val in list(doms[var]):
            ndoms = copy.deepcopy(doms)
            ndoms[var] = [val]
            valid = True
            for n in neighbors[var]:
                if val in ndoms[n]:
                    ndoms[n].remove(val)
                    if not ndoms[n]:
                        valid = False
                        break
            if valid:
                yield 'assigned', var, ndoms, bt[0], ac3solved, time.time() - start
                res = yield from backtrack(ndoms)
                if res:
                    return res
            bt[0] += 1
            yield 'backtrack', var, doms, bt[0], ac3solved, time.time() - start
        return None

    res = yield from backtrack(domains)
    yield 'complete', None, res if res else domains, bt[0], ac3solved, time.time() - start

def partc():
    win = tk.Tk()
    win.title("Part C: Sudoku CSP Solver")
    win.geometry("580x620")
    win.configure(bg="#1E1E2E")

    top = tk.Frame(win, bg="#1E1E2E")
    top.pack(expand=True, fill=tk.BOTH)

    gridframe = tk.Frame(top, bg="#6272A4", bd=2)
    gridframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    sample = [
        [5,3,0,0,7,0,0,0,0], [6,0,0,1,9,5,0,0,0], [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3], [4,0,0,8,0,3,0,0,1], [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0], [0,0,0,4,1,9,0,0,5], [0,0,0,0,8,0,0,7,9]
    ]

    entries: list[list[tk.Entry]] = []
    for r in range(9):
        rowentries: list[tk.Entry] = []
        for c in range(9):
            topp = 3 if r % 3 == 0 else 1
            leftp = 3 if c % 3 == 0 else 1
            e = tk.Entry(gridframe, width=3, justify="center", bg="#282A36", fg="#F8F8F2", bd=0)
            e.grid(row=r, column=c, padx=(leftp, 1), pady=(topp, 1))
            if sample[r][c] != 0:
                e.insert(0, str(sample[r][c]))
                e.config(fg="#FF79C6")
            rowentries.append(e)
        entries.append(rowentries)

    ctrl = tk.Frame(win, bg="#282A36", padx=10, pady=10)
    ctrl.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

    row1 = tk.Frame(ctrl, bg="#282A36")
    row1.pack(fill=tk.X, pady=4)

    lbl = tk.Label(row1, text="AC-3 Solved: 0  |  Backtracks: 0  |  Time: 0.00s", bg="#282A36", fg="#F1FA8C")
    lbl.pack(side=tk.LEFT, padx=10)

    def solve():
        grid = [[int(entries[r][c].get()) if entries[r][c].get().isdigit() else 0 for c in range(9)] for r in range(9)]
        gen = sudoku(grid)
        def step():
            try:
                ev, cell, doms, bt, ac3s, t = next(gen)
                if doms:
                    for (r, c), dom in doms.items():
                        if len(dom) == 1:
                            entries[r][c].delete(0, tk.END)
                            entries[r][c].insert(0, str(dom[0]))
                lbl.config(text=f"AC-3 Solved: {ac3s}  |  Backtracks: {bt}  |  Time: {t:.2f}s")
                if ev != 'complete':
                    win.after(20, step)
            except StopIteration:
                pass
        step()

    tk.Button(row1, text="Solve CSP", bg="#BD93F9", fg="#000000", command=solve, padx=10).pack(side=tk.RIGHT, padx=5)

    return win

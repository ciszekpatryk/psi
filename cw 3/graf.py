import tkinter as tk
from tkinter import filedialog
import math
import heapq

# Zmienne globalne trzymające stan grafu i algorytmu
coords = {}
adj = {}
start_node, end_node = None, None
pq = []
g_cost = {}
parent = {}
visited = set()
path = []
finished = False

def dist(u, v):
    return math.hypot(coords[u][0] - coords[v][0], coords[u][1] - coords[v][1])

def load_graph(filename):
    global coords, adj, start_node, end_node
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    coords = {i + 1: tuple(map(int, lines[i + 1].split())) for i in range(n)}
    adj = {i + 1: list(map(int, lines[n + 1 + i].split()[1:])) for i in range(n)}
    start_node, end_node = 1, n
    reset_search()

def reset_search():
    global pq, g_cost, parent, visited, path, finished
    if not coords:
        return
    pq = [(0.0, start_node)]
    g_cost = {start_node: 0.0}
    parent = {start_node: None}
    visited = set()
    path = []
    finished = False
    lbl_status.config(text=f"Start: {start_node} (LPM) | Cel: {end_node} (PPM)")
    draw()

def step():
    global finished, path
    if finished or not pq:
        return

    # Wyciągamy z kolejki pierwszy nieodwiedzony wierzchołek
    while pq:
        _, curr = heapq.heappop(pq)
        if curr not in visited:
            break
    else:
        lbl_status.config(text="Brak ścieżki!")
        finished = True
        return

    visited.add(curr)

    # Jeśli dotarliśmy do celu, odtwarzamy ścieżkę ze słownika parent
    if curr == end_node:
        finished = True
        curr_p = end_node
        while curr_p:
            path.append(curr_p)
            curr_p = parent[curr_p]
        lbl_status.config(text=f"Znaleziono! Koszt drogi: {g_cost[end_node]:.2f}")
        draw()
        return

    algo = algo_var.get()
    for nxt in adj[curr]:
        if nxt in visited:
            continue
        new_g = g_cost[curr] + dist(curr, nxt)
        
        if nxt not in g_cost or new_g < g_cost[nxt]:
            g_cost[nxt] = new_g
            parent[nxt] = curr
            h = dist(nxt, end_node)
            
            # Wybór funkcji kosztu f(n) zależnie od algorytmu
            if algo == "BFS":
                f = h
            elif algo == "Dijkstra":
                f = new_g
            else: # A*
                f = new_g + h
                
            heapq.heappush(pq, (f, nxt))
    draw()

def run_all():
    while not finished and pq:
        step()

def get_screen_pos(x, y):
    # Przeliczanie współrzędnych siatki na piksele (odwrócona oś Y jak na stronie)
    return 40 + x * 45, 520 - y * 45

def on_click(event, is_start):
    global start_node, end_node
    for u, (x, y) in coords.items():
        sx, sy = get_screen_pos(x, y)
        if math.hypot(event.x - sx, event.y - sy) <= 15:
            if is_start:
                start_node = u
            else:
                end_node = u
            reset_search()
            break

def draw():
    canvas.delete("all")
    # Krawędzie
    for u, neighbors in adj.items():
        x1, y1 = get_screen_pos(*coords[u])
        for v in neighbors:
            if u < v:
                x2, y2 = get_screen_pos(*coords[v])
                in_path = u in path and v in path and abs(path.index(u) - path.index(v)) == 1
                color = "red" if in_path else "#cccccc"
                width = 4 if in_path else 1.5
                canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

    # Wierzchołki
    in_pq = {u for _, u in pq}
    for u, (x, y) in coords.items():
        sx, sy = get_screen_pos(x, y)
        color = "white"
        if u in in_pq: color = "#fff2cc"      # W kolejce (żółty)
        if u in visited: color = "#cfe2f3"    # Odwiedzony (niebieski)
        if u in path: color = "#ea9999"       # Ścieżka (czerwony)
        if u == start_node: color = "#93c47d" # Start (zielony)
        if u == end_node: color = "#e06666"   # Cel (ciemnoczerwony)

        canvas.create_oval(sx - 14, sy - 14, sx + 14, sy + 14, fill=color, outline="black", width=1.5)
        canvas.create_text(sx, sy, text=str(u), font=("Arial", 9, "bold"))

# --- Konfiguracja okna Tkinter ---
root = tk.Tk()
root.title("Lab 3 - Best First Search / Dijkstra / A*")

frame = tk.Frame(root, pady=5)
frame.pack()

tk.Button(frame, text="Wczytaj plik", command=lambda: load_graph(filedialog.askopenfilename())).pack(side=tk.LEFT, padx=5)

algo_var = tk.StringVar(value="A*")
for name in ["BFS", "Dijkstra", "A*"]:
    tk.Radiobutton(frame, text=name, variable=algo_var, value=name, command=reset_search).pack(side=tk.LEFT)

tk.Button(frame, text="Krok", command=step, bg="#d9ead3").pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Do końca", command=run_all).pack(side=tk.LEFT, padx=2)
tk.Button(frame, text="Reset", command=reset_search).pack(side=tk.LEFT, padx=5)

lbl_status = tk.Label(root, text="Wczytaj graf", font=("Arial", 11, "bold"))
lbl_status.pack()

canvas = tk.Canvas(root, width=600, height=550, bg="white")
canvas.pack()
canvas.bind("<Button-1>", lambda e: on_click(e, True))  # LPM ustawia Start
canvas.bind("<Button-3>", lambda e: on_click(e, False)) # PPM ustawia Cel

# Automatyczne wczytanie graf1.txt na start (jeśli jest w folderze)
try:
    load_graph("graf1.txt")
except:
    pass

root.mainloop()
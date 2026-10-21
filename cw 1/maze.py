import os
import sys
import time

# Słownik możliwych ruchów: (zmiana_wiersza, zmiana_kolumny)
# Góra: (-1, 0), Dół: (1, 0), Prawo: (0, 1), Lewo: (0, -1)
MOVES = {
    '┼': [(-1, 0), (1, 0), (0, 1), (0, -1)],
    '│': [(-1, 0), (1, 0)],
    '─': [(0, 1), (0, -1)],
    ' ': [],
    '┐': [(1, 0), (0, -1)],
    '┘': [(-1, 0), (0, -1)],
    '└': [(-1, 0), (0, 1)],
    '┌': [(1, 0), (0, 1)],
    '┤': [(-1, 0), (1, 0), (0, -1)],
    '┴': [(-1, 0), (0, 1), (0, -1)],
    '├': [(-1, 0), (1, 0), (0, 1)],
    '┬': [(1, 0), (0, 1), (0, -1)],
    '╵': [(-1, 0)],
    '╷': [(1, 0)],
    '╴': [(0, -1)],
    '╶': [(0, 1)],
}


def render_map(maze_map, start_pos, target_pos, visited_nodes, frontier_nodes):
  os.system('cls' if os.name == 'nt' else 'clear')
  for row_idx in range(len(maze_map)):
    line = ''
    for col_idx in range(len(maze_map[0])):
      current_point = (row_idx, col_idx)
      char = maze_map[row_idx][col_idx]
      if current_point == start_pos:
        line += f'\033[1;31m{char}\033[0m'  # Red
      elif current_point == target_pos:
        line += f'\033[1;34m{char}\033[0m'  # Blue
      elif current_point in visited_nodes:
        line += f'\033[1;32m{char}\033[0m'  # Green
      elif current_point in frontier_nodes:
        line += f'\033[1;33m{char}\033[0m'  # Yellow
      else:
        line += char
    print(line)


# 1. Wczytanie mapy z pliku podanego jako argument
if len(sys.argv) < 2:
  print('Użycie: python3 labirynt.py <ścieżka_do_mapy>')
  sys.exit()

with open(sys.argv[1], 'r', encoding='utf-8') as file_obj:
  raw_lines = [line.rstrip('\r\n') for line in file_obj.readlines()]

# Automatyczne wykrycie rozmiaru i wyrównanie linii spacjami
height = len(raw_lines)
width = max(len(line) for line in raw_lines)
maze_map = [line.ljust(width, ' ') for line in raw_lines]

# 2. Wyświetlenie mapy i pobranie danych od użytkownika
render_map(maze_map, None, None, [], [])
print(f'Rozmiar mapy: {height} wierszy x {width} kolumn')

start_row, start_col = map(
    int, input('Współrzędne startowe (wiersz kolumna): ').replace(',', ' ').split()
)
target_row, target_col = map(
    int, input('Współrzędne końcowe (wiersz kolumna): ').replace(',', ' ').split()
)
algorithm = input('Rodzaj algorytmu (BFS / DFS): ').strip().upper()

start = (start_row, start_col)
target = (target_row, target_col)

# 3. Algorytm przeszukiwania
frontier = [start]
visited = []
steps = 0
found = False

while len(frontier) > 0:
  # FIFO dla BFS (pobieramy pierwszy element), LIFO dla DFS (pobieramy ostatni)
  if algorithm == 'BFS':
    current = frontier.pop(0)
  else:
    current = frontier.pop()

  if current in visited:
    continue

  visited.append(current)
  steps += 1

  render_map(maze_map, start, target, visited, frontier)
  time.sleep(0.1)  # 100 ms

  if current == target:
    found = True
    break

  # Dodawanie sąsiadów do kolejki
  r, c = current
  char = maze_map[r][c]

  for dr, dc in MOVES.get(char, []):
    neighbor_row, neighbor_col = r + dr, c + dc
    if 0 <= neighbor_row < height and 0 <= neighbor_col < width:
      if (
          (neighbor_row, neighbor_col) not in visited
          and (neighbor_row, neighbor_col) not in frontier
      ):
        frontier.append((neighbor_row, neighbor_col))

# 4. Podsumowanie
if found:
  print('Znaleziono ścieżkę!')
else:
  print('Brak ścieżki między wybranymi polami.')
print(f'Ilość wykonanych kroków: {steps}')

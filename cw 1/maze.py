import os
import sys
import time

# Słownik możliwych ruchów: (zmiana_wiersza, zmiana_kolumny)
# Góra: (-1, 0), Dół: (1, 0), Prawo: (0, 1), Lewo: (0, -1)
RUCHY = {
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


def rysuj(mapa, start, cel, odwiedzone, kolejka):
  os.system('cls' if os.name == 'nt' else 'clear')
  for r in range(len(mapa)):
    linia = ''
    for c in range(len(mapa[0])):
      pkt = (r, c)
      znak = mapa[r][c]
      if pkt == start:
        linia += f'\033[1;31m{znak}\033[0m'  # Czerwony
      elif pkt == cel:
        linia += f'\033[1;34m{znak}\033[0m'  # Niebieski
      elif pkt in odwiedzone:
        linia += f'\033[1;32m{znak}\033[0m'  # Zielony
      elif pkt in kolejka:
        linia += f'\033[1;33m{znak}\033[0m'  # Żółty
      else:
        linia += znak
    print(linia)


# 1. Wczytanie mapy z pliku podanego jako argument
if len(sys.argv) < 2:
  print('Użycie: python3 labirynt.py <ścieżka_do_mapy>')
  sys.exit()

with open(sys.argv[1], 'r', encoding='utf-8') as f:
  linie = [l.rstrip('\r\n') for l in f.readlines()]

# Automatyczne wykrycie rozmiaru i wyrównanie linii spacjami
wys = len(linie)
szer = max(len(l) for l in linie)
mapa = [l.ljust(szer, ' ') for l in linie]

# 2. Wyświetlenie mapy i pobranie danych od użytkownika
rysuj(mapa, None, None, [], [])
print(f'Rozmiar mapy: {wys} wierszy x {szer} kolumn')

sr, sc = map(
    int, input('Współrzędne startowe (wiersz kolumna): ').replace(',', ' ').split()
)
kr, kc = map(
    int, input('Współrzędne końcowe (wiersz kolumna): ').replace(',', ' ').split()
)
algorytm = input('Rodzaj algorytmu (BFS / DFS): ').strip().upper()

start = (sr, sc)
cel = (kr, kc)

# 3. Algorytm przeszukiwania
kolejka = [start]
odwiedzone = []
kroki = 0
znaleziono = False

while len(kolejka) > 0:
  # FIFO dla BFS (pobieramy pierwszy element), LIFO dla DFS (pobieramy ostatni)
  if algorytm == 'BFS':
    obecny = kolejka.pop(0)
  else:
    obecny = kolejka.pop()

  if obecny in odwiedzone:
    continue

  odwiedzone.append(obecny)
  kroki += 1

  rysuj(mapa, start, cel, odwiedzone, kolejka)
  time.sleep(0.1)  # 100 ms

  if obecny == cel:
    znaleziono = True
    break

  # Dodawanie sąsiadów do kolejki
  r, c = obecny
  znak = mapa[r][c]

  for dr, dc in RUCHY.get(znak, []):
    nr, nc = r + dr, c + dc
    if 0 <= nr < wys and 0 <= nc < szer:
      if (nr, nc) not in odwiedzone and (nr, nc) not in kolejka:
        kolejka.append((nr, nc))

# 4. Podsumowanie
if znaleziono:
  print('Znaleziono ścieżkę!')
else:
  print('Brak ścieżki między wybranymi polami.')
print(f'Ilość wykonanych kroków: {kroki}')
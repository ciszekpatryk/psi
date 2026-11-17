import math

# start z domyslnymi wartosciami
N = int(input("Rozmiar planszy (domyślnie 3): ") or 3)
MAX_DEPTH = int(input("Maks. głębokość (domyślnie 4): ") or 4)
turn = (
    input("Kto zaczyna? [U]żytkownik (O) / [K]omputer (X) (domyślnie U): ")
    .strip()
    .upper()
    or "U"
)

board = [" "] * (N * N)


def print_board():
    for i in range(N):
        print(" | ".join(board[i * N : (i + 1) * N]))
        if i < N - 1:
            print("-" * (4 * N - 3))
    print()


def check_winner():
    lines = []
    for i in range(N):
        lines.append(board[i * N : (i + 1) * N])  # wiersze
        lines.append(board[i::N])  # kolumny
    lines.append(board[0 :: N + 1])  # przekątna \
    lines.append(board[N - 1 : N * N - 1 : N - 1])  # przekątna /

    for line in lines:
        if len(set(line)) == 1 and line[0] != " ":
            return line[0]
    return "Tie" if " " not in board else None


def minimax(depth, is_max):
    res = check_winner()
    if res == "X":
        return 100 - depth  # komputer wygrywa (szybciej = lepiej)
    if res == "O":
        return -100 + depth  # gracz wygrywa
    if res == "Tie" or depth == MAX_DEPTH:
        return 0  # remis lub limit głębokości

    best = -math.inf if is_max else math.inf
    for i in range(N * N):
        if board[i] == " ":
            board[i] = "X" if is_max else "O"
            score = minimax(depth + 1, not is_max)
            board[i] = " "
            best = max(best, score) if is_max else min(best, score)
    return best


def best_move():
    best_score, move = -math.inf, -1
    for i in range(N * N):
        if board[i] == " ":
            board[i] = "X"
            score = minimax(1, False)
            board[i] = " "
            if score > best_score:
                best_score, move = score, i
    return move


# glowna petla gierki
while not check_winner():
    print_board()
    if turn == "U":
        try:
            m = int(input(f"Twój ruch (0-{N*N-1}): "))
            if board[m] != " ":
                continue
            board[m], turn = "O", "K"
        except (ValueError, IndexError):
            print("Błędny indeks!")
    else:
        print("Ruch komputera...")
        board[best_move()], turn = "X", "U"

print_board()
w = check_winner()
print("Remis!" if w == "Tie" else f"Wygrywa: {w}!")
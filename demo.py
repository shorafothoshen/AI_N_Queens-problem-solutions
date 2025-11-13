def is_safe(board, row, col, n):
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True


def solve_n_queens(board, row, n, solutions):
    if row == n:
        solutions.append(board[:])
        return
    for col in range(8):  # fixed 8x8 board
        if is_safe(board, row, col, n):
            board[row] = col
            solve_n_queens(board, row + 1, n, solutions)
            board[row] = -1


def print_board(board, n):
    for i in range(8):
        row = ""
        for j in range(8):
            if i < n and board[i] == j:
                row += " Q "
            else:
                row += " . "
        print(row)
    print("-" * 24)


def all_n_queens_fixed_board(n):
    board = [-1] * n
    solutions = []
    solve_n_queens(board, 0, n, solutions)
    return solutions


# --- Main ---
if __name__ == "__main__":
    print("=== All Valid Placements of N Queens on an 8x8 Board ===")
    n = int(input("Enter number of queens (1–8): "))

    if not (1 <= n <= 8):
        print("Please enter a number between 1 and 8.")
    else:
        print("\nSearching for all valid combinations...\n")
        solutions = all_n_queens_fixed_board(n)
        print(f"✅ Total valid solutions found: {len(solutions)}\n")

        show = input("Do you want to display all solutions? (y/n): ").lower() == 'y'
        if show:
            for i, sol in enumerate(solutions, start=1):
                print(f"\nSolution #{i}: {sol}")
                print_board(sol, n)
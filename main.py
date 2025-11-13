import tkinter as tk
from tkinter import messagebox

# --- N-Queens Solver (Backtracking) ---
def is_safe(board, row, col, n):
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True

def solve_n_queens(board, row, n, solutions):
    if row == n:
        solutions.append(board[:])
        return
    for col in range(8):  
        if is_safe(board, row, col, n):
            board[row] = col
            solve_n_queens(board, row + 1, n, solutions)
            board[row] = -1

def all_n_queens_fixed_board(n):
    board = [-1] * n
    solutions = []
    solve_n_queens(board, 0, n, solutions)
    return solutions

# --- GUI Functions ---
class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens on 8x8 Board")

        # User input
        tk.Label(root, text="Number of Queens (1-8):").grid(row=0, column=0, padx=5, pady=5)
        self.n_entry = tk.Entry(root)
        self.n_entry.grid(row=0, column=1, padx=5, pady=5)

        self.solve_btn = tk.Button(root, text="Find Solutions", command=self.find_solutions)
        self.solve_btn.grid(row=0, column=2, padx=5, pady=5)

        # Canvas for drawing board
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.grid(row=1, column=0, columnspan=3, pady=10)

        # Navigation buttons
        self.prev_btn = tk.Button(root, text="<< Previous", command=self.prev_solution)
        self.prev_btn.grid(row=2, column=0, pady=5)
        self.next_btn = tk.Button(root, text="Next >>", command=self.next_solution)
        self.next_btn.grid(row=2, column=2, pady=5)
        self.status_label = tk.Label(root, text="Solution: 0 / 0")
        self.status_label.grid(row=2, column=1)

        self.solutions = []
        self.current_index = 0
        self.n = 0

    def draw_board(self, board):
        self.canvas.delete("all")
        cell_size = 50
        for row in range(8):
            for col in range(8):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        for row in range(len(board)):
            col = board[row]
            if col != -1:
                x = col * cell_size + cell_size // 2
                y = row * cell_size + cell_size // 2
                self.canvas.create_text(x, y, text="♛", font=("Arial", 30), fill="red")

        self.status_label.config(text=f"Solution: {self.current_index + 1} / {len(self.solutions)}")

    def find_solutions(self):
        try:
            self.n = int(self.n_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number (1-8)")
            return

        if not (1 <= self.n <= 8):
            messagebox.showerror("Error", "Number of queens must be 1-8")
            return

        self.solutions = all_n_queens_fixed_board(self.n)
        self.current_index = 0

        if len(self.solutions) == 0:
            messagebox.showinfo("Result", f"No solutions for {self.n} queens on 8x8 board.")
        else:
            self.draw_board(self.solutions[self.current_index])
            messagebox.showinfo("Result", f"Total solutions found: {len(self.solutions)}")

    def prev_solution(self):
        if not self.solutions:
            return
        self.current_index = (self.current_index - 1) % len(self.solutions)
        self.draw_board(self.solutions[self.current_index])

    def next_solution(self):
        if not self.solutions:
            return
        self.current_index = (self.current_index + 1) % len(self.solutions)
        self.draw_board(self.solutions[self.current_index])


# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    gui = NQueensGUI(root)
    root.mainloop()
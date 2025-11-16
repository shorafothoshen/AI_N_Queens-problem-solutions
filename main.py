import tkinter as tk
from tkinter import messagebox
import random


# ---------------- GENETIC ALGORITHM ---------------- #

def fitness(ind, n):
    clashes = 0
    for i in range(n):
        for j in range(i + 1, n):
            if ind[i] == ind[j] or abs(ind[i] - ind[j]) == abs(i - j):
                clashes += 1
    return 1 / (1 + clashes)


def mutate(ind, n):
    pos = random.randint(0, n - 1)
    ind[pos] = random.randint(0, 7)
    return ind


def crossover(p1, p2, n):
    cp = random.randint(1, n - 2)
    return p1[:cp] + p2[cp:]


def random_individual(n):
    return [random.randint(0, 7) for _ in range(n)]


def is_unique(sol, solutions):
    return sol not in solutions


def run_single_ga(n):
    """ Run GA 1 time and try to find 1 solution """
    pop_size = 200
    pop = [random_individual(n) for _ in range(pop_size)]

    for _ in range(2000):
        pop = sorted(pop, key=lambda x: fitness(x, n), reverse=True)

        if fitness(pop[0], n) == 1:
            return pop[0][:]

        new_pop = pop[:30]  # elitism

        while len(new_pop) < pop_size:
            p1 = random.choice(pop[:60])
            p2 = random.choice(pop[:60])
            child = crossover(p1, p2, n)
            if random.random() < 0.3:
                mutate(child, n)
            new_pop.append(child)

        pop = new_pop

    return None  # No solution this run


def genetic_multi_solutions(n, target_count=10):
    """ Run GA multiple times to collect many unique solutions """
    final_solutions = []

    tries = 0
    while len(final_solutions) < target_count and tries < target_count * 20:
        sol = run_single_ga(n)
        if sol and is_unique(sol, final_solutions):
            final_solutions.append(sol)
        tries += 1

    return final_solutions


# ---------------------- GUI ---------------------- #

class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Genetic Algorithm N-Queens (Multiple Solutions)")

        tk.Label(root, text="Number of Queens (1-8):").grid(row=0, column=0)
        self.n_entry = tk.Entry(root)
        self.n_entry.grid(row=0, column=1)

        tk.Button(root, text="Find Solutions", command=self.find_solutions).grid(row=0, column=2)

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.grid(row=1, column=0, columnspan=3)

        tk.Button(root, text="<< Previous", command=self.prev_solution).grid(row=2, column=0)
        self.status_label = tk.Label(root, text="Solution 0/0")
        self.status_label.grid(row=2, column=1)
        tk.Button(root, text="Next >>", command=self.next_solution).grid(row=2, column=2)

        self.solutions = []
        self.current_index = 0

    def draw_board(self, board):
        self.canvas.delete("all")
        cell = 50

        # draw chessboard
        for r in range(8):
            for c in range(8):
                x1, y1 = c * cell, r * cell
                x2, y2 = x1 + cell, y1 + cell
                color = "white" if (r + c) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # draw queens
        for r in range(len(board)):
            c = board[r]
            x = c * cell + cell // 2
            y = r * cell + cell // 2
            self.canvas.create_text(x, y, text="♛", font=("Arial", 28), fill="red")

        self.status_label.config(text=f"Solution {self.current_index + 1}/{len(self.solutions)}")

    def find_solutions(self):
        try:
            n = int(self.n_entry.get())
        except:
            messagebox.showerror("Error", "Invalid number")
            return

        if not (1 <= n <= 8):
            messagebox.showerror("Error", "Queens must be 1-8")
            return

        self.solutions = genetic_multi_solutions(n, target_count=10)

        if not self.solutions:
            messagebox.showinfo("Result", "No solutions found.")
            return

        self.current_index = 0
        self.draw_board(self.solutions[0])
        messagebox.showinfo("Done", f"Found {len(self.solutions)} unique solutions!")

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


# ---------------------- MAIN ---------------------- #
root = tk.Tk()
gui = NQueensGUI(root)
root.mainloop()

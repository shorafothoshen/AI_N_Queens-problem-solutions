import random


# ------------------------ FITNESS ------------------------ #

def fitness(ind, n):
    """ Higher fitness = fewer clashes """
    clashes = 0
    for i in range(n):
        for j in range(i + 1, n):
            if ind[i] == ind[j] or abs(ind[i] - ind[j]) == abs(i - j):
                clashes += 1
    return 1 / (1 + clashes)


# ------------------------ MUTATION ------------------------ #

def mutate(ind, n):
    pos = random.randint(0, n - 1)
    ind[pos] = random.randint(0, 7)
    return ind


# ------------------------ CROSSOVER ------------------------ #

def crossover(p1, p2, n):
    point = random.randint(1, n - 2)
    return p1[:point] + p2[point:]


# ------------------------ RANDOM INDIVIDUAL ------------------------ #

def random_individual(n):
    return [random.randint(0, 7) for _ in range(n)]


# ------------------------ UNIQUE CHECK ------------------------ #

def is_unique(solution, solution_list):
    return solution not in solution_list


# ------------------------ SINGLE GA RUN ------------------------ #

def run_single_ga(n):
    """
    Runs GA one time and returns ONE valid N-Queens solution.
    """

    population_size = 200
    population = [random_individual(n) for _ in range(population_size)]

    for _ in range(2000):  # number of generations
        population = sorted(population, key=lambda x: fitness(x, n), reverse=True)

        # If perfect solution found
        if fitness(population[0], n) == 1:
            return population[0][:]

        new_population = population[:30]  # elitism

        while len(new_population) < population_size:
            parent1 = random.choice(population[:60])
            parent2 = random.choice(population[:60])

            child = crossover(parent1, parent2, n)

            if random.random() < 0.3:
                mutate(child, n)

            new_population.append(child)

        population = new_population

    return None  # no solution found in this run


# ------------------------ MULTIPLE SOLUTIONS ------------------------ #

def genetic_multi_solutions(n, target_solutions=10):
    """
    Runs GA multiple times to collect multiple UNIQUE N-Queens solutions.
    """

    solutions = []
    attempts = 0

    while len(solutions) < target_solutions and attempts < target_solutions * 20:
        sol = run_single_ga(n)

        if sol and is_unique(sol, solutions):
            solutions.append(sol)

        attempts += 1

    return solutions


# ------------------------ MAIN TEST ------------------------ #

if __name__ == "__main__":
    n = 8  # number of queens

    print("Running Genetic Algorithm...")
    sols = genetic_multi_solutions(n, target_solutions=10)

    print(f"\nTotal unique solutions found: {len(sols)}\n")

    for i, sol in enumerate(sols, 1):
        print(f"Solution {i}:", sol)

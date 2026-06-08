"""
Genetic Algorithm - Complete Educational Code
==============================================
Problem: Find an 8-bit string with the maximum number of 1s
Target: [1, 1, 1, 1, 1, 1, 1, 1]  →  Fitness = 8
"""

import random

# ─── Main Settings ───────────────────────────────────────────────
CHROMOSOME_LENGTH = 8     # Number of genes
POPULATION_SIZE  = 6      # Number of individuals in each generation
CROSSOVER_RATE   = 0.8    # Probability of crossover
MUTATION_RATE    = 0.1    # Probability of each gene mutating
MAX_GENERATIONS  = 20     # Number of generations


# ─── Step 1: Create Random Chromosome ────────────────────────────
def create_chromosome():
    """Creates a random solution (list of 0s and 1s)"""
    return [random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)]


# ─── Step 2: Create Initial Population ────────────────────────────────
def create_population():
    """Multiple random solutions together = initial population"""
    return [create_chromosome() for _ in range(POPULATION_SIZE)]


# ─── Step 3: Fitness Function ─────────────────────────────────────
def fitness(chromosome):
    """
    The more 1s, the better.
    Fitness = number of 1s in chromosome
    """
    return sum(chromosome)


# ─── Step 4: Selection ───────────────────────────────────────────
def roulette_wheel_selection(population):
    """
    Roulette wheel selection: Better individuals have higher chances.
    Like a lottery where each person has tickets equal to their score.
    """
    fitness_scores = [fitness(individual) for individual in population]
    total = sum(fitness_scores)

    # If all scores are zero, select randomly
    if total == 0:
        return random.choice(population)

    # Random number between 0 and total
    target = random.uniform(0, total)
    running_sum = 0
    for individual, score in zip(population, fitness_scores):
        running_sum += score
        if running_sum >= target:
            return individual

    return population[-1]  # Fallback


# ─── Step 5: Crossover ────────────────────────────────────────────
def crossover(parent_1, parent_2):
    """
    Single-point crossover:
    A random cut point is selected.
    Child 1 = first half of parent 1 + second half of parent 2
    Child 2 = first half of parent 2 + second half of parent 1
    """
    if random.random() > CROSSOVER_RATE:
        # No crossover: parents are copied directly
        return parent_1[:], parent_2[:]

    point = random.randint(1, CHROMOSOME_LENGTH - 1)
    child_1 = parent_1[:point] + parent_2[point:]
    child_2 = parent_2[:point] + parent_1[point:]
    return child_1, child_2


# ─── Step 6: Mutation ──────────────────────────────────────────────
def mutate(chromosome):
    """
    Each gene flips with low probability: 0→1 or 1→0
    Mutation creates diversity and prevents getting stuck in local optima.
    """
    return [
        1 - gene if random.random() < MUTATION_RATE else gene
        for gene in chromosome
    ]


# ─── Display Tools ─────────────────────────────────────────────
def display_chromosome(chromosome, label=""):
    """Displays chromosome in readable format"""
    bar = "█" * fitness(chromosome) + "░" * (CHROMOSOME_LENGTH - fitness(chromosome))
    print(f"  {label:<12} {chromosome}  [{bar}]  Score: {fitness(chromosome)}/{CHROMOSOME_LENGTH}")


def display_population(population, generation_number):
    """Displays entire population status"""
    print(f"\n{'═'*60}")
    print(f"  Generation {generation_number}")
    print(f"{'─'*60}")
    for i, individual in enumerate(population):
        display_chromosome(individual, f"Individual {i+1}:")
    fitness_scores = [fitness(ind) for ind in population]
    print(f"{'─'*60}")
    print(f"  Best: {max(fitness_scores)}/{CHROMOSOME_LENGTH}  |  Average: {sum(fitness_scores)/len(fitness_scores):.1f}/{CHROMOSOME_LENGTH}")


# ─── Main Algorithm ──────────────────────────────────────────────
def genetic_algorithm():
    print("🧬 Genetic Algorithm — Educational")
    print(f"   Target: finding {[1]*CHROMOSOME_LENGTH}")
    print(f"   Population: {POPULATION_SIZE} individuals  |  Generations: {MAX_GENERATIONS}")

    # Step 1: Create initial population
    population = create_population()
    display_population(population, 0)

    history = []

    for generation_number in range(1, MAX_GENERATIONS + 1):

        # Step 2: Evaluate and check termination condition
        best = max(population, key=fitness)
        if fitness(best) == CHROMOSOME_LENGTH:
            print(f"\n🎉 Optimal solution found in generation {generation_number - 1}!")
            display_chromosome(best, "Best:")
            break

        # Step 3: Create new generation
        new_generation = []

        # Elitism: Top 2 individuals go directly to next generation
        sorted_population = sorted(population, key=fitness, reverse=True)
        new_generation.extend([sorted_population[0][:], sorted_population[1][:]])

        # Remaining individuals created through crossover and mutation
        while len(new_generation) < POPULATION_SIZE:
            parent_1 = roulette_wheel_selection(population)
            parent_2 = roulette_wheel_selection(population)
            child_1, child_2 = crossover(parent_1, parent_2)
            child_1 = mutate(child_1)
            child_2 = mutate(child_2)
            new_generation.extend([child_1, child_2])

        # Trim population to correct size
        population = new_generation[:POPULATION_SIZE]

        # Store statistics for final display
        fitness_scores = [fitness(ind) for ind in population]
        history.append({
            "generation": generation_number,
            "best": max(fitness_scores),
            "average": round(sum(fitness_scores) / len(fitness_scores), 1)
        })

        # Display every 3 generations
        if generation_number % 3 == 0 or generation_number == 1:
            display_population(population, generation_number)

    # Display progress trend
    print(f"\n{'═'*60}")
    print("  📈 Progress Trend:")
    print(f"{'─'*60}")
    for stats in history[::3] or history:
        bar = "█" * stats["best"] + "░" * (CHROMOSOME_LENGTH - stats["best"])
        print(f"  Generation {stats['generation']:>2}:  [{bar}]  best={stats['best']}  average={stats['average']}")

    # Display final best result
    final_best = max(population, key=fitness)
    print(f"\n{'═'*60}")
    print("  ✅ Final Result:")
    display_chromosome(final_best, "Best:")
    print(f"{'═'*60}\n")

    return final_best


# ─── Execute ───────────────────────────────────────────────────────
if __name__ == "__main__":
    random.seed(42)   # For reproducible results (remove for randomness)
    genetic_algorithm()

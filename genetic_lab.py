import random
# Constants
POP_SIZE = 6
GENOME_LENGTH = 5  # 5 bits for values 0-31
GENERATIONS = 5
MUTATION_RATE = 10  # Percentage

class Individual:
    def __init__(self):
        self.genome = [random.randint(0, 1) for _ in range(GENOME_LENGTH)]
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        x = self.genome_to_int()
        return x * x

    def genome_to_int(self):
        value = 0
        for bit in self.genome:
            value = (value << 1) | bit
        return value

    def mutate(self):
        for i in range(GENOME_LENGTH):
            if random.randint(0, 99) < MUTATION_RATE:
                self.genome[i] ^= 1  # Flip the bit
        self.fitness = self.calculate_fitness()

    def __str__(self):
        return f"Genome: {''.join(map(str, self.genome))} (x={self.genome_to_int()}), Fitness={self.fitness}"

def initialize_population():
    return [Individual() for _ in range(POP_SIZE)]

def selection(population):
    total_fitness = sum(ind.fitness for ind in population)
    pick = random.randint(0, total_fitness - 1)
    current = 0
    for ind in population:
        current += ind.fitness
        if current > pick:
            return ind
    return population[-1]

def crossover(parent1, parent2):
    point = random.randint(1, GENOME_LENGTH - 1)
    child1 = Individual()
    child2 = Individual()
    child1.genome = parent1.genome[:point] + parent2.genome[point:]
    child2.genome = parent2.genome[:point] + parent1.genome[point:]
    child1.fitness = child1.calculate_fitness()
    child2.fitness = child2.calculate_fitness()
    return child1, child2

def best_individual(population):
    return max(population, key=lambda ind: ind.fitness)

def main():
    random.seed()
    population = initialize_population()

    for gen in range(GENERATIONS):
        # Sort by fitness (descending)
        population.sort(key=lambda ind: ind.fitness, reverse=True)

        print(f"Generation {gen}: Best fitness = {population[0].fitness}, {population[0]}")

        # Elitism: keep top 2
        new_population = [population[0], population[1]]

        while len(new_population) < POP_SIZE:
            parent1 = selection(population)
            parent2 = selection(population)
            child1, child2 = crossover(parent1, parent2)
            child1.mutate()
            child2.mutate()
            new_population.append(child1)
            if len(new_population) < POP_SIZE:
                new_population.append(child2)

        population = new_population

    best = best_individual(population)
    print("\nBest solution found:")
    print(best)

if __name__ == "__main__":
    main()

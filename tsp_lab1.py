import random
import math

# Constants
POP_SIZE = 100               # Population size (number of routes)
CITIES = [(0, 0), (1, 3), (4, 3), (6, 1), (2, 7), (8, 8)]  # Example city coordinates (x, y)
GENOME_LENGTH = len(CITIES)  # Number of cities (or genes)
GENERATIONS = 500            # Number of generations
MUTATION_RATE = 0.1          # Mutation rate (probability of changing a gene)

# Helper Function: Calculate distance between two cities
def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Class: Individual (Represents a route)
class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        """Calculate the total distance of the route (fitness)."""
        total_distance = 0
        for i in range(len(self.genome) - 1):
            total_distance += distance(CITIES[self.genome[i]], CITIES[self.genome[i + 1]])
        total_distance += distance(CITIES[self.genome[-1]], CITIES[self.genome[0]])  # Return to the start
        return total_distance

# Function: Initialize Population
def initialize_population():
    """Generate the initial population of random routes."""
    population = []
    for _ in range(POP_SIZE):
        genome = list(range(GENOME_LENGTH))  # Create a list of city indices [0, 1, ..., n-1]
        random.shuffle(genome)              # Randomly shuffle the cities
        population.append(Individual(genome))  # Add individual with calculated fitness
    return population

# Function: Selection (Roulette Wheel Selection)
def selection(population):
    """Select an individual based on fitness proportionate selection."""
    total_fitness = sum(1 / ind.fitness for ind in population)  # Inverse of fitness (minimizing distance)
    pick = random.uniform(0, total_fitness)
    current = 0
    for ind in population:
        current += 1 / ind.fitness
        if current > pick:
            return ind

# Function: Crossover (Order Crossover)
def crossover(p1, p2):
    """Create two children using order crossover."""
    point1, point2 = sorted([random.randint(0, GENOME_LENGTH - 1), random.randint(0, GENOME_LENGTH - 1)])
    child1_genome = [-1] * GENOME_LENGTH
    child2_genome = [-1] * GENOME_LENGTH

    # Copy part of parent1’s genome to child1 and part of parent2’s genome to child2
    for i in range(point1, point2):
        child1_genome[i] = p1.genome[i]
        child2_genome[i] = p2.genome[i]

    # Fill in remaining cities from parent2 and parent1 to child1 and child2
    index1, index2 = 0, 0
    for i in range(GENOME_LENGTH):
        if child1_genome[i] == -1:
            while p2.genome[index2] in child1_genome:
                index2 += 1
            child1_genome[i] = p2.genome[index2]
        
        if child2_genome[i] == -1:
            while p1.genome[index1] in child2_genome:
                index1 += 1
            child2_genome[i] = p1.genome[index1]

    return Individual(child1_genome), Individual(child2_genome)

# Function: Mutation (Swap Mutation)
def mutate(individual):
    """Randomly swap two cities in the route with a given probability (mutation rate)."""
    if random.random() < MUTATION_RATE:
        i, j = random.randint(0, GENOME_LENGTH - 1), random.randint(0, GENOME_LENGTH - 1)
        individual.genome[i], individual.genome[j] = individual.genome[j], individual.genome[i]
    individual.fitness = individual.calculate_fitness()  # Recalculate fitness after mutation

# Function: Main Genetic Algorithm
def genetic_algorithm():
    # Initialize the population
    population = initialize_population()

    # Evolve population over generations
    for generation in range(GENERATIONS):
        # Sort population by fitness (ascending order, because we are minimizing distance)
        population.sort(key=lambda ind: ind.fitness)

        # Output the best solution in current generation
        print(f"Generation {generation + 1}: Best Route: {population[0].genome}, Distance: {population[0].fitness}")

        # Elitism: Keep the best 2 individuals
        new_population = population[:2]

        # Generate new individuals until we reach the desired population size
        while len(new_population) < POP_SIZE:
            parent1 = selection(population)
            parent2 = selection(population)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.append(child1)
            if len(new_population) < POP_SIZE:
                new_population.append(child2)

        # Replace old population with new one
        population = new_population

    # Return the best solution found
    return population[0]

# Run the Genetic Algorithm
best_solution = genetic_algorithm()

# Output the best route found
print(f"\nBest Route Found: {best_solution.genome}")
print(f"Total Distance: {best_solution.fitness}")

# Constants and Parameters
POP_SIZE = 50  # Population size
NUM_INTERSECTIONS = 10  # Number of intersections in the network
SIGNAL_TIMING_GENES = 3  # [Green, Yellow, Red] for each intersection
GENERATIONS = 100  # Number of generations
MUTATION_RATE = 0.05  # Mutation rate
CROSSOVER_RATE = 0.7  # Crossover rate

# Helper Function: Generate Random Traffic Signal Schedule
Function generate_random_schedule():
    schedule = []
    For each intersection in NUM_INTERSECTIONS:
        green_time = random.randint(30, 120)  # Random green light duration
        yellow_time = random.randint(5, 15)  # Random yellow light duration
        red_time = random.randint(30, 120)  # Random red light duration
        schedule.append([green_time, yellow_time, red_time])
    Return schedule

# Helper Function: Evaluate Fitness of a Schedule
Function evaluate_fitness(schedule):
    total_congestion = 0
    total_waiting_time = 0
    total_flow_efficiency = 0

    For each intersection in schedule:
        # Simulate congestion and waiting time based on signal timings and traffic data
        congestion, waiting_time, flow_efficiency = simulate_traffic_flow(intersection)
        total_congestion += congestion
        total_waiting_time += waiting_time
        total_flow_efficiency += flow_efficiency

    fitness = total_congestion + total_waiting_time + (1 / total_flow_efficiency)  # Lower is better
    Return fitness

# Helper Function: Crossover Between Two Schedules
Function crossover(parent1, parent2):
    If random number > CROSSOVER_RATE:
        Return parent1, parent2  # No crossover
    point = random integer between 1 and NUM_INTERSECTIONS - 1
    child1 = parent1[0:point] + parent2[point:]
    child2 = parent2[0:point] + parent1[point:]
    Return child1, child2

# Helper Function: Mutation of a Schedule
Function mutate(schedule):
    For each intersection in schedule:
        If random number < MUTATION_RATE:
            Randomly mutate the green, yellow, or red light duration
    Return mutated schedule

# Main Genetic Algorithm Function for Traffic Optimization
Function genetic_algorithm():
    population = [generate_random_schedule() for i in range(POP_SIZE)]  # Initial population

    For generation in 1 to GENERATIONS:
        fitness_scores = [evaluate_fitness(schedule) for schedule in population]

        # Sort population based on fitness (ascending order)
        population = sort(population based on fitness_scores)

        # Elitism: Keep the best 10% of the population
        new_population = population[0 to 10% of POP_SIZE]

        # Crossover and Mutation to generate new schedules
        While len(new_population) < POP_SIZE:
            parent1, parent2 = select_two_parents_based_on_fitness(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            If len(new_population) < POP_SIZE:
                new_population.append(mutate(child2))

        population = new_population  # Update population for next generation

    # Output the best schedule found
    best_schedule = population[0]
    Return best_schedule, evaluate_fitness(best_schedule)

# Run the genetic algorithm for traffic signal optimization
best_schedule, best_fitness = genetic_algorithm()
Print("Best Traffic Signal Schedule:", best_schedule)
Print("Best Fitness (Congestion and Travel Time):", best_fitness)

import random

# 0: Pomidor, 1: Ogórek, 2: Marchew, 3: Cebula, 4: Ziemniak, 5: Fasola, 6: Sałata, 7: Czosnek
PLANTS = ["Pomidor", "Ogórek", "Marchew", "Cebula", "Ziemniak", "Fasola", "Sałata", "Czosnek"]
N = len(PLANTS)

# Macierz niekompatybilności (1 = złe sąsiedztwo, 0 = dobre sąsiedztwo)
BAD_NEIGHBORS = [
    [0, 1, 0, 0, 1, 0, 0, 0], # 0: Pomidor - nie lubi ogórka i ziemniaka
    [1, 0, 0, 1, 1, 0, 0, 1], # 1: Ogórek
    [0, 0, 0, 0, 1, 0, 0, 0], # 2: Marchew
    [0, 1, 0, 0, 0, 1, 0, 1], # 3: Cebula
    [1, 1, 1, 0, 0, 1, 0, 1], # 4: Ziemniak
    [0, 0, 0, 1, 1, 0, 0, 1], # 5: Fasola
    [0, 0, 0, 0, 0, 0, 0, 0], # 6: Sałata
    [0, 1, 0, 1, 1, 1, 0, 0]  # 7: Czosnek
]

# Parametry algorytmu
POPULATION_SIZE = 50
MAX_ITERATIONS = 1000
CROSSOVER_RATE = 0.6
MUTATION_RATE = 0.3

def calculate_fitness(garden):
    errors = 0
    # Kara za duplikaty roślin
    duplicates = N - len(set(garden))
    errors += duplicates * 2

    # Kara za złych sąsiadów obok siebie
    for i in range(N - 1):
        plant_a = garden[i]
        plant_b = garden[i + 1]
        if BAD_NEIGHBORS[plant_a][plant_b] == 1:
            errors += 1

    return errors

# 1. Inicjalizacja losowej populacji
population = [[random.randint(0, N - 1) for _ in range(N)] for _ in range(POPULATION_SIZE)]

# Główna pętla algorytmu
for iteration in range(MAX_ITERATIONS):
    # 2. Krzyżowanie
    crossover_count = int(POPULATION_SIZE * CROSSOVER_RATE)
    for _ in range(crossover_count // 2):
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        split_point = random.randint(1, N - 1)
        
        child1 = parent1[:split_point] + parent2[split_point:]
        child2 = parent2[:split_point] + parent1[split_point:]
        population.extend([child1, child2])

    # 3. Mutacja
    mutation_count = int(POPULATION_SIZE * MUTATION_RATE)
    for _ in range(mutation_count):
        individual = random.choice(population).copy()
        bed_index = random.randint(0, N - 1)
        individual[bed_index] = random.randint(0, N - 1)
        population.append(individual)

    # 4. Ocena i Selekcja
    population.sort(key=calculate_fitness)
    population = population[:POPULATION_SIZE]

    # Sprawdzenie warunku stopu
    best_individual = population[0]
    if calculate_fitness(best_individual) == 0:
        print(f"Znaleziono optymalny ogródek w iteracji: {iteration}")
        break
else:
    print("Osiągnięto limit iteracji.")

# Wyświetlenie wyników
best_individual = population[0]
print("Reprezentacja wektorowa:", best_individual)
print("Liczba błędów:", calculate_fitness(best_individual))
print("Układ grządek:", " | ".join([PLANTS[i] for i in best_individual]))
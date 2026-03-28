#!/usr/bin/env python3
"""genetic_algo2 - Genetic algorithm framework."""
import argparse, random, math

def onemax_fitness(individual): return sum(individual)
def target_string_fitness(individual, target):
    return sum(1 for a, b in zip(individual, target) if a == b)

def tournament_select(pop, fitness, k=3):
    candidates = random.sample(list(zip(pop, fitness)), k)
    return max(candidates, key=lambda x: x[1])[0]

def roulette_select(pop, fitness):
    total = sum(fitness)
    if total == 0: return random.choice(pop)
    r = random.uniform(0, total)
    cumsum = 0
    for ind, f in zip(pop, fitness):
        cumsum += f
        if cumsum >= r: return ind
    return pop[-1]

def crossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]

def mutate(individual, rate=0.01):
    return [1 - g if random.random() < rate else g for g in individual]

def run_ga(pop_size=100, gene_length=50, generations=200, mut_rate=0.01, selection="tournament"):
    pop = [[random.randint(0, 1) for _ in range(gene_length)] for _ in range(pop_size)]
    select = tournament_select if selection == "tournament" else roulette_select
    for gen in range(generations):
        fitness = [onemax_fitness(ind) for ind in pop]
        best_fit = max(fitness); best_ind = pop[fitness.index(best_fit)]
        if gen % (generations // 10) == 0:
            print(f"Gen {gen:4d}: best={best_fit}/{gene_length} avg={sum(fitness)/len(fitness):.1f}")
        if best_fit == gene_length: print(f"Solved at generation {gen}!"); return best_ind
        new_pop = [best_ind]  # elitism
        while len(new_pop) < pop_size:
            p1 = select(pop, fitness); p2 = select(pop, fitness)
            c1, c2 = crossover(p1, p2)
            new_pop.extend([mutate(c1, mut_rate), mutate(c2, mut_rate)])
        pop = new_pop[:pop_size]
    return max(pop, key=onemax_fitness)

def main():
    p = argparse.ArgumentParser(description="Genetic algorithm")
    p.add_argument("-p", "--pop-size", type=int, default=100)
    p.add_argument("-g", "--generations", type=int, default=200)
    p.add_argument("-l", "--length", type=int, default=50)
    p.add_argument("-m", "--mutation", type=float, default=0.02)
    p.add_argument("-s", "--selection", choices=["tournament", "roulette"], default="tournament")
    args = p.parse_args()
    best = run_ga(args.pop_size, args.length, args.generations, args.mutation, args.selection)
    print(f"\nBest fitness: {onemax_fitness(best)}/{args.length}")

if __name__ == "__main__":
    main()

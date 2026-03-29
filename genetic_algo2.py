#!/usr/bin/env python3
"""Genetic algorithm framework — selection, crossover, mutation."""
import sys, random

class GeneticAlgorithm:
    def __init__(self, pop_size=50, gene_length=20, mutation_rate=0.01):
        self.pop_size = pop_size
        self.gene_length = gene_length
        self.mutation_rate = mutation_rate
        self.population = [[random.randint(0,1) for _ in range(gene_length)] for _ in range(pop_size)]
    def fitness(self, individual):
        return sum(individual)  # default: maximize ones
    def select(self):
        tournament = random.sample(self.population, min(3, len(self.population)))
        return max(tournament, key=self.fitness)
    def crossover(self, p1, p2):
        pt = random.randint(1, self.gene_length - 1)
        return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]
    def mutate(self, individual):
        return [g if random.random() > self.mutation_rate else 1-g for g in individual]
    def evolve(self, generations=100):
        for gen in range(generations):
            new_pop = []
            best = max(self.population, key=self.fitness)
            new_pop.append(best)  # elitism
            while len(new_pop) < self.pop_size:
                p1, p2 = self.select(), self.select()
                c1, c2 = self.crossover(p1, p2)
                new_pop.extend([self.mutate(c1), self.mutate(c2)])
            self.population = new_pop[:self.pop_size]
        return max(self.population, key=self.fitness)

def test():
    random.seed(42)
    ga = GeneticAlgorithm(pop_size=30, gene_length=20, mutation_rate=0.02)
    best = ga.evolve(50)
    assert ga.fitness(best) >= 15  # should get close to all 1s
    assert len(best) == 20
    print("  genetic_algo2: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Genetic algorithm framework")

#!/usr/bin/env python3
"""Genetic algorithm optimizer. Zero dependencies."""
import random

class GeneticAlgorithm:
    def __init__(self, pop_size=50, mutation_rate=0.1, crossover_rate=0.7, elitism=2, seed=42):
        self.pop_size = pop_size; self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate; self.elitism = elitism
        random.seed(seed)

    def optimize(self, fitness_fn, create_fn, crossover_fn, mutate_fn, generations=100):
        pop = [create_fn() for _ in range(self.pop_size)]
        best = None; best_fit = float("-inf"); history = []
        for gen in range(generations):
            scored = [(ind, fitness_fn(ind)) for ind in pop]
            scored.sort(key=lambda x: x[1], reverse=True)
            if scored[0][1] > best_fit:
                best = scored[0][0]; best_fit = scored[0][1]
            history.append(best_fit)
            new_pop = [s[0] for s in scored[:self.elitism]]
            while len(new_pop) < self.pop_size:
                p1 = self._tournament(scored)
                p2 = self._tournament(scored)
                child = crossover_fn(p1, p2) if random.random() < self.crossover_rate else p1[:]
                if random.random() < self.mutation_rate: child = mutate_fn(child)
                new_pop.append(child)
            pop = new_pop
        return best, best_fit, history

    def _tournament(self, scored, k=3):
        candidates = random.sample(scored, min(k, len(scored)))
        return max(candidates, key=lambda x: x[1])[0]

def onemax_example(length=20, generations=50):
    ga = GeneticAlgorithm(pop_size=30, seed=42)
    return ga.optimize(
        fitness_fn=sum,
        create_fn=lambda: [random.randint(0,1) for _ in range(length)],
        crossover_fn=lambda a,b: [a[i] if random.random()<0.5 else b[i] for i in range(len(a))],
        mutate_fn=lambda a: [1-a[i] if random.random()<0.1 else a[i] for i in range(len(a))],
        generations=generations
    )

if __name__ == "__main__":
    best, fit, hist = onemax_example()
    print(f"Best fitness: {fit}/{len(best)}")

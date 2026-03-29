from genetic_algo2 import GeneticAlgorithm, onemax_example
best, fit, hist = onemax_example(20, 100)
assert fit >= 15  # should get close to all 1s
assert len(hist) == 100
assert hist[-1] >= hist[0]  # should improve
best2, fit2, _ = onemax_example(10, 50)
assert fit2 >= 7
print("genetic_algo2 tests passed")

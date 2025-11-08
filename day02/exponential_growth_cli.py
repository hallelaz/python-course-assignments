"""
Calculates cell number and generation time during exponential growth.

Parameters:
- N0: initial number of cells
- t:  total time (hours)
- n:  number of generations

Formulas:
Nt = N0 * 2^n
g  = t / n
"""

import sys

def exponential_growth_phase(N0, n):
    Nt = N0 * (2 ** n)
    return Nt

def generation_time(t, n):
    return t / n

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 4:
        print("Usage: python growth.py <N0> <t> <n>")
        sys.exit(1)

    N0 = float(sys.argv[1])
    t = float(sys.argv[2])
    n = float(sys.argv[3])

    Nt = exponential_growth_phase(N0, n)
    g = generation_time(t, n)

    print(f"\nNumber of cells at time t: Nt = {Nt:.2e}")
    print(f"Generation time (g) = {g:.2f} hours")

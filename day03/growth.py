#!/usr/bin/env python3

"""
Calculates cell number and generation time during exponential growth.

Usage:
    python growth.py <N0> <t> <n>

Parameters:
- N0: initial number of cells
- t:  total time (hours)
- n:  number of generations
"""

import sys
import bio_growth_logic as logic

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python growth.py <N0> <t> <n>")
        sys.exit(1)

    N0 = float(sys.argv[1])
    t = float(sys.argv[2])
    n = float(sys.argv[3])

    Nt = logic.exponential_growth_phase(N0, n)
    g = logic.generation_time(t, n)

    print(f"\nNumber of cells at time t: Nt = {Nt:.2e}")
    print(f"Generation time (g) = {g:.2f} hours")

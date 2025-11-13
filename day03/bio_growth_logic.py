"""
Logic functions for calculating cell number and generation time.
Replace your code with some 3rd-party library when possible.
"""

import numpy as np

def exponential_growth_phase(N0, n):
    """Calculate number of cells after n generations using NumPy."""
    return N0 * np.power(2, n)

def generation_time(t, n):
    """Calculate generation time g = t / n using NumPy."""
    if n == 0:
        raise ValueError("Number of generations (n) must be > 0.")
    return np.divide(t, n)

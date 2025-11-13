import math
import bio_growth_logic as logic

def test_exponential_growth_phase_basic():
    # N0 = 100 cells, n = 3 generations → 100 * 2^3 = 800
    assert logic.exponential_growth_phase(100, 3) == 800


def test_exponential_growth_phase_zero_generations():
    # No divisions → Nt = N0
    assert logic.exponential_growth_phase(500, 0) == 500



def test_exponential_growth_phase_large():
    # Test large exponent without overflow
    Nt = logic.exponential_growth_phase(1e6, 10)
    assert math.isclose(Nt, 1e6 * 1024)

def test_generation_time_basic():
    # total time = 10 hours, generations = 5 → g = 2h
    assert logic.generation_time(10, 5) == 2

def test_generation_time_fraction():
    # fractional output → should support floats
    assert math.isclose(logic.generation_time(7.5, 3), 2.5)

def test_generation_time_invalid_n():
    # n must not be zero (division by zero)
    try:
        logic.generation_time(10, 0)
        assert False, "Expected ValueError"
    except ValueError:
        assert True

import numpy as np

def get_coeffs(n, dx, t_pml, omega, m=3.5, sigma=4):
    x = np.arange(n) + dx 
    l = pos(t_pml - x) + pos(x - (n - t_pml))
    return (1 - 1j * (sigma / omega) * (l / t_pml)**m)**-1
    # return (1 - 0j * (sigma / omega) * (l / t_pml)**m)**-1

def pos(x):
    return x * (x > 0)

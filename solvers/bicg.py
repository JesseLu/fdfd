import pycuda.gpuarray as ga
import numpy as np

def solve(multA, multAT, b, x, max_iters=100):
    """
    Solve the system.
    """

    r = b - multA(x)
    print r, b
    r_hat = r
    rho = np.zeros(max_iters).astype(np.float32)
    rho[0] = 1
    print rho
    p = ga.zeros_like(r)
    p_hat = ga.zeros_like(r)

    for k in range(1, max_iters):
        print k, ga.dot(r, r).get()
        rho[k] = ga.dot(r_hat, r).get()
        beta = rho[k] / rho[k-1]
        p = r + beta * p
        p_hat = r_hat + beta * p_hat
        v = multA(p)
        alpha = rho[k] / ga.dot(p_hat, v).get()
        # print ga.dot(p_hat, v).get()
        x = x + alpha * p
        r = r - alpha * v
        r_hat = r_hat - alpha * multAT(p_hat)
        # print beta, p, p_hat, v, alpha, x, r, r_hat

    return x, rho

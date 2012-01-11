# import pycuda.gpuarray as ga
import numpy as np

def solve2(multA, multAT, b, b_star, x, x_star, eps=1e-6, max_iters=100):
    """
    Solve the system.
    """

    rho = np.zeros(max_iters).astype(np.complex128)
    err = np.zeros(max_iters).astype(np.float64)

    r = b - multA(x)
    r_star = b_star - multAT(x_star)
    p = r
    p_star = r_star

    term_val = eps * np.linalg.norm(b)
    print 'Termination error value:', term_val
    for k in range(max_iters):
        err[k] = np.linalg.norm(r)
        if err[k] < term_val:
            return x, err[:k+1]
        
        rho[k] = np.dot(r_star, r)
        alpha = rho[k] / np.dot(p_star, multA(p))

        x = x + alpha * p
        x_star = x_star + alpha * p_star

        r = r - alpha * multA(p)
        r_star = r_star - alpha * multAT(p_star)

        beta = np.dot(r_star, r) / rho[k]

        p = r + beta * p
        p_star = r_star + beta * p_star

    return x, err 


def solve1(multA, multAT, b, x, eps=1e-6, max_iters=100):
    """
    Solve the system.
    """

    r = b - multA(x)
    r_hat = r
    rho = np.zeros(max_iters).astype(np.float32)
    rho[0] = 1
    p = np.zeros_like(r)
    p_hat = np.zeros_like(r)

    term_val = eps**2 * np.dot(b, b)
    for k in range(1, max_iters):
        print k, np.dot(r, r), term_val
        rho[k] = np.dot(r_hat, r)
        if np.dot(r, r) < term_val:
            return x, rho[:k+1]
        beta = rho[k] / rho[k-1]
        p = r + beta * p
        p_hat = r_hat + beta * p_hat
        v = multA(p)
        alpha = rho[k] / np.dot(p_hat, v)
        x = x + alpha * p
        r = r - alpha * v
        r_hat = r_hat - alpha * multAT(p_hat)
    return x, rho

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

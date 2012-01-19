import numpy as np

def _axby(a, x, b, y):
    """Default axby routine."""
    y[:] = a * x + b * y

def _nochange(x):
    _axby(1, x, 0, y)

def solve_asymm(b, x=None, x_hat=None, multA=_nochange, multAT=_nochange, 
                dot=np.dot, axby=_axby, copy=np.copy, \
                eps=1e-6, max_iters=1000):
    """Bi-conjugate gradient solve of square, non-symmetric system.

    Input variables:
    multA -- multA(x) calculates A * x and returns the result.
    multAT -- multAT(x) calculates A^T * x and returns the result.
    b -- the problem to be solved is A * x = b.

    Keyword variables:
    x -- initial guess of x, default value is 0.
    x_hat -- initial guess for x_hat, default value is 0.
    dot -- dot(x, y) calculates xT * y and returns the result, 
           default: numpy.dot().
    axby -- axby(a, x, b, y) calculates a * x + b * y and 
            stores the result in y, default y[:] = a * x + b * y.
    copy -- copy(x) returns a copy of x, default numpy.copy().
    eps -- the termination error is determined by eps * ||b|| (2-norm),
           default 1e-6.
    max_iters -- maximum number of iterations allowed, default 1000.

    Output variables:
    x -- the apprximate answer of A * x = b.
    err -- a numpy array with the error value at every iteration.

    Examples:
    """

    # TODO
    # ----
    # *   Check for breakdown condition.
    # *   Notify user if we weren't able to beat term_err.

    if x is None: # Default value of x is 0.
        x = copy(b)
        axby(0, b, 0, x)

    if x_hat is None: # Default value for x_hat is 0.
        x_hat = copy(b)
        axby(0, b, 0, x_hat)

    # r = b - A * x.
    r = copy(b)
    multA(x, r)
    axby(1, b, -1, r)

    # r_hat = b - A * x_hat
    r_hat = copy(b)
    multAT(x, r_hat)
    axby(1, b, -1, r_hat)

    # p = r, p_hat = r_hat.
    p = copy(r)
    p_hat = copy(r_hat)

    # Initialize v, v_hat. Used to store A * p, AT * p_hat.
    v = copy(p) # Don't need the values, this is an "empty" copy.
    v_hat = copy(p_hat)

    rho = np.zeros(max_iters).astype(np.complex128) # Related to error.
    err = np.zeros(max_iters).astype(np.float64) # Error.
    term_err = eps * np.sqrt(dot(b, b)) # Termination error value.

    for k in range(max_iters):

        # Compute error and check termination condition.
        err[k] = np.sqrt(np.abs(dot(r, r)))
        # print k, err[k]
        if err[k] < term_err:
            break
        
        # rho = r_hatT * r.
        rho[k] = dot(r_hat, r)

        # v = A * p, v_hat = AT * p_hat.
        multA(p, v)
        multAT(p_hat, v_hat)

        # alpha = rho / (p_hatT * v).
        alpha = rho[k] / dot(p_hat, v)

        # x += alpha * p, x_hat += alpha * p_hat.
        axby(alpha, p, 1, x)
        axby(alpha, p_hat, 1, x_hat)

        # r -= alpha * v, r -= alpha * v_hat. 
        axby(-alpha, v, 1, r)
        axby(-alpha, v_hat, 1, r_hat)

        # beta = (r_hatT * r) / rho.
        beta = dot(r_hat, r) / rho[k]

        # p = r + beta * p, p_hat = r_hat + beta * p_hat.
        axby(1, r, beta, p)
        axby(1, r_hat, beta, p_hat)

    # Return the answer, and the progress we made.
    return x, err[:k+1] 
        

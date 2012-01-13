import numpy as np
from solvers import bicg
import matplotlib.pyplot as plt
import stretched_coords


N = 10
omega = 0.5
s0 = stretched_coords.get_coeffs(N, 0.0, 1, omega)
s1 = stretched_coords.get_coeffs(N, 0.5, 1, omega)
A = np.zeros((N, N))
for k in range(N):
    A[k,k] = 1
    if k == 0:
        A[k,N-1] = -1
    else:
        A[k,k-1] = -1
A1 = np.dot(np.diag(s0), A)
A2 = np.dot(np.diag(s1), A.T)
A = np.dot(A2, A1) - omega**2 * (1 - 0.j) * np.eye(N)
# A = np.dot(A.T, A) - omega**2 * (1 - 0.j) * np.eye(N)
print A
print A.T
def mA(x):
    return np.dot(A, x) 

def mAT(x):
    return np.dot(A.T, x)

b = np.zeros(N).astype(np.complex128)
b[N/2+2] = 1 + 0j
# print mAT(b)

# Find "exact" solution.
x = np.linalg.solve(A, b)
print 'error from "exact" solution', np.linalg.norm(mA(x) - b)

# Solve using bi-cg.
x = np.zeros_like(b)
x, err = bicg.solve2(mA, mAT, b, b, x, x, max_iters=1000)
print len(err), 'iterations'
print 'ending in:'
for err_val in err[-5:]:
    print err_val

print 'error is', np.linalg.norm(mA(x) - b)
# plt.plot(np.abs(x), 'b.-')
# plt.show()

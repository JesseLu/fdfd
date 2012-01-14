import numpy as np
from my_math import bicg
from my_phys import stretched_coords


N = 100 
omega = 0.3
s0 = stretched_coords.get_coeffs(N, 0.0, 10, omega)
s1 = stretched_coords.get_coeffs(N, 0.5, 10, omega)
A = np.zeros((N, N))
for k in range(N):
    A[k,k] = 1
    if k == 0:
        A[k,N-1] = -1
    else:
        A[k,k-1] = -1
A1 = np.dot(np.diag(s0), A)
A2 = np.dot(np.diag(s1), A.T)
A = np.dot(A2, A1) - omega**2 * np.eye(N)

def mA(x, y):
    y[:] = np.dot(A, x) 
    return

def mAT(x, y):
    y[:] = np.dot(A.T, x)
    return

b = np.zeros(N).astype(np.complex128)
b[N/2] = 1 + 0j

# print mAT(b)

# Find "exact" solution.
x = np.linalg.solve(A, b)
print 'error from "exact" solution', np.linalg.norm(np.dot(A, x) - b)

# Solve using bi-cg.
x = np.zeros_like(b)
x, err  = bicg.solve_asymm(mA, mAT, b)
print len(err), 'iterations'
print 'ending in:'
for err_val in err[-5:]:
    print err_val

print 'error is', np.linalg.norm(np.dot(A, x) - b)
# plt.plot(np.abs(x), 'b.-')
# plt.show()

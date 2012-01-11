import numpy as np
from solvers import bicg
import matplotlib.pyplot as plt

N = 200
A = np.zeros((N, N))
for k in range(N):
    A[k,k] = 1
    if k == 0:
        A[N-1,k] = -1
    else:
        A[k-1,k] = -1
A = np.dot(A.T, A) - 0.03 * (1 - 0.j) * np.eye(N)
# A = A + 0.1 * np.eye(N)

def mA(x):
    return np.dot(A, x) + 0

def mAT(x):
    return np.dot(A.T, x) + 0

b = np.zeros(N).astype(np.complex128)
b[N/2] = 1 + 1j
# b = np.arange(N)
# print A, A.T, b
# print mA(b)
# print mAT(b)
x, err = bicg.solve2(mA, mAT, b, b, np.zeros(N), np.zeros(N), max_iters=120)
r = mA(x) - b
print np.dot(r, r)
print err  
plt.plot(x)
plt.show()

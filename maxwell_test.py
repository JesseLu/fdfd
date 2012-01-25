import pycuda.autoinit
import numpy as np
from my_math import bicg
from my_phys import maxwell 
from matplotlib import pyplot as plt

# shape = (3,3,3)
shape = (100,100,100)
# b_rand = [np.random.randn(*shape).astype(np.complex128) for k in range(3)]
omega = 0.4
b = [np.zeros(shape).astype(np.complex128) for k in range(3)]
b[1][50,50,50] = 1.
# b[0][30,30,30] = 1.

ops, b = maxwell.get_ops(omega, b)
# a0 = b.dup()
# ops['multA'](b, a0)
# a1 = b.dup()
# ops['multAT'](b, a1)
# for k in range(3):
#     diff = a0.f[k].g.get() - a1.f[k].g.get()
#     print np.linalg.norm(diff.flatten(), ord=2)
# a = a1.f[0].g.get().flatten()
# for t in a:
#     print t
x, err = bicg.solve_asymm(b, max_iters=1000, **ops)
# for k in range(err.size):
#     print k, err[k]
# print err.size, 'iterations ending with', err[-3:]

v = 0.01
plt.imshow(np.real(np.squeeze(x.f[1].g.get()[50,:,:])), \
        cmap=plt.cm.jet, vmin=-v, vmax=v, interpolation='nearest')
plt.show()

import numpy as np
from my_math import bicg
from my_phys import maxwell 
from matplotlib import pyplot as plt

shape = (30, 4, 30)
omega = 0.6
b = [np.zeros(shape).astype(np.complex128) for k in range(3)]
b[1][15,2,15] = 1.

import pycuda.autoinit
ops, b = maxwell.get_ops(omega, b)
x, err = bicg.solve_asymm(b, max_iters=200, **ops)
print err.size, 'iterations ending with', err[-3:]

# v = 0.1
# plt.imshow(np.real(np.squeeze(x.f[1].g.get()[:,2,:])), \
#         cmap=plt.cm.jet, vmin=-v, vmax=v, interpolation='nearest')
# plt.show()

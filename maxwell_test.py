import numpy as np
from my_math import bicg
from my_phys import maxwell 
from matplotlib import pyplot as plt

shape = (50, 30, 30)
omega = 0.3
b = [np.zeros(shape).astype(np.complex128) for k in range(3)]
b[1][15, 15, 15] = 1.

import pycuda.autoinit
ops, b = maxwell.get_ops(omega, b)
x, err = bicg.solve_asymm(b, max_iters=20, **ops)
print err.size, 'iterations ending with', err[-3:]

v = 0.01
plt.imshow(np.abs(np.squeeze(x.f[1].g.get()[20,:,:])), \
        cmap=plt.cm.jet, vmin=-v, vmax=v, interpolation='nearest')
plt.show()

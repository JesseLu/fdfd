import numpy as np
from my_math import bicg
from my_phys import maxwell 
from matplotlib import pyplot as plt

shape = (40, 40, 40)
omega = 0.6
b = [np.zeros(shape).astype(np.complex128) for k in range(3)]
b[1][20,20,20] = 1.

import pycuda.autoinit
ops, b = maxwell.get_ops(omega, b)
x, err = bicg.solve_asymm(b, **ops)
print err.size, 'iterations ending with', err[-3:]

plt.imshow(np.real(np.squeeze(x.f[1].g.get()[:,20,:])))
plt.show()

import numpy as np
from my_math import bicg
from my_phys import maxwell 

shape = (1, 2, 14)
omega = 0.5
b = [np.zeros(shape).astype(np.complex128) for k in range(3)]
b[0][0,1,7] = 1.

import pycuda.autoinit
ops, b = maxwell.get_ops(omega, b)
x, err = bicg.solve_asymm(b, **ops)
print err.size, 'iterations ending with', err[-3:]

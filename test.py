import pycuda.autoinit
import numpy as np
from my_phys import maxwell as mx

x, y, z = np.ones(10), np.ones(10), np.ones(10)
a = mx.VecField()
a = mx.VecField(x, y, z)
b = a.dup()
print a.dot(b)
b.aby(2, 4, a)
print a.dot(b)

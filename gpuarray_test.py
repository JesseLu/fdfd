import numpy as np
from my_math import bicg
from my_phys import simple_wave
import pycuda.autoinit

 
shape = (1, 1, 400)
omega = 0.3;
b = np.zeros(shape).astype(np.complex128)
b[0,0,shape[2]/2] = 1 + 0j;
# b = ga.to_gpu(b)
# b.set(np.arange(shape[2]).astype(np.complex128))
# y = ga.zeros_like(b) 
b, ops = simple_wave.get_ops(shape, omega, b)
# multAT(b, y)
# print y.get()
# multA(b, y)
# print y.get()
x, err = bicg.solve_asymm(b, **ops)
# x, err = bicg.solve_asymm(multA, multAT, b, \
#                 dot=my_dot, axby=my_axby, copy=my_copy)
print err.size, 'iterations ending with', err[-3:]

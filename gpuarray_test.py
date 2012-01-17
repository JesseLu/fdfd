from jinja2 import Template
import numpy as np
from my_math import bicg
from my_phys import stretched_coords, simple_wave
from my_cs import grid_traverse
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import pycuda.gpuarray as ga

 
shape = (1, 1, 400)
omega = 0.3;
b = np.zeros(shape).astype(np.complex128)
b[0,0,shape[2]/2] = 1 + 0j;
# b = ga.to_gpu(b)
# b.set(np.arange(shape[2]).astype(np.complex128))
# y = ga.zeros_like(b) 
b, multA, multAT, ops = simple_wave.get_ops1(shape, omega, b)
# multAT(b, y)
# print y.get()
# multA(b, y)
# print y.get()
x, err = bicg.solve_asymm(multA, multAT, b, **ops)
# x, err = bicg.solve_asymm(multA, multAT, b, \
#                 dot=my_dot, axby=my_axby, copy=my_copy)
print err.size, 'iterations ending with', err[-3:]

import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import pycuda.gpuarray as ga
import numpy as np
import my_traverse

# # x = ga.zeros((2, 3, 4), np.dtype([('x', np.complex64), ('y', np.complex64)]))
# x = ga.zeros((2, 3, 4), np.dtype(np.complex64))
# y = x + (1 + 1j)
# print y.conj().get()
my_traverse.fd_kernel(  'testfunc', \
                        'float', \
                        ('Ex', 'Ey'), \
                        (2, 3, 4), \
                        'Ey(0,0,0) = 1.0;')

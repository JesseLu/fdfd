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
shape = (2, 3, 4)
src = my_traverse.fd_kernel(  'testfunc', \
                        'cuFloatComplex', \
                        ('Ey',), \
                        shape, \
                        """
                        Ey(0,0,0) = make_cuFloatComplex(i, j);
                        """)
print src
mod = SourceModule(src)
E_update = mod.get_function('testfunc')
Ex = ga.zeros(shape, np.complex64)
Ey = ga.zeros(shape, np.complex64)
E_update(Ey.gpudata, block=shape[::-1], grid=(1,1))
print Ey.get()
# print Ey.get()
print ga.dot(Ex, Ey)

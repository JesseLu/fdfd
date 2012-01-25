from pycuda import gpuarray as ga
from pycuda import driver
from pycuda.elementwise import ElementwiseKernel
from pycuda.reduction import ReductionKernel
import numpy as np

_axby = ElementwiseKernel(
            """ pycuda::complex<double> a, pycuda::complex<double> *x,
                pycuda::complex<double> b, pycuda::complex<double> *y""", \
           ' x[i] = a * x[i] + b * y[i]')

_norm = ReductionKernel(np.complex128, neutral="0",
        reduce_expr="a+b", map_expr="pow(abs(x[i]), 2)",
                arguments="pycuda::complex<double> *x")


class Grid:
    def __init__(self, array):
        # Get the array.
        if type(array) is np.ndarray:
            self.g = ga.to_gpu(array) # Copy data to the GPU.
        elif type(array) is ga.GPUArray:
            self.g = array # GPUArray already initialized.
        else:
            print 'Invalid type' # Raise proper exception here.

#         # Create the aby function.
#         if self.g.dtype is np.dtype('complex128'):
#             cuda_type = 'pycuda::complex<double>'
#         elif self.g.dtype is np.dtype('complex64'):
#             cuda_type = 'pycuda::complex<float>'


    def dup(self):
        dup_grid = Grid(ga.empty_like(self.g))
        driver.memcpy_dtod(dup_grid.g.gpudata, self.g.gpudata, self.g.nbytes)
        return dup_grid
        
    def dot(self, y):
        # return ga.dot(self.g, y.g).get()
        return np.dot(self.g.get().flatten(), y.g.get().flatten())

    def aby(self, a, b, y):
        _axby(a, self.g, b, y.g)

    def norm(self):
        # return np.sqrt(ga.sum(pow(abs(self.g),2)))
        # return np.sqrt(np.sum(np.abs(self.g.get())**2))
        return _norm(self.g).get()

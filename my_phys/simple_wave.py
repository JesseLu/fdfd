from jinja2 import Environment, PackageLoader
from my_cs import grid_traverse
import stretched_coords
from pycuda import gpuarray as ga
import numpy as np
# Implements multA, multAT, dot, axby, and copy for a simple 1D wave equation.

# Execute when module is loaded.
# Load the jinja environment.
jinja_env = Environment(loader=PackageLoader(__name__, 'templates'))

def get_ops(shape, omega):
    ds0 = ga.to_gpu(stretched_coords.get_coeffs(shape[2], 0.0, 10, omega))
    ds1 = ga.to_gpu(stretched_coords.get_coeffs(shape[2], 0.5, 10, omega))
    cuda_type = 'pycuda::complex<double>'
    const = 'test'

    mA_func = grid_traverse.get_function(shape, \
        jinja_env.get_template('simplewave_multA.cu').render(w2=omega**2, zz=shape[2]), \
        (cuda_type, 's0'), (cuda_type, 's1'), \
        (cuda_type, 'u'), (cuda_type, 'v'))
    def multA(x, y):
        mA_func(ds0, ds1, x, y)
        return

    mAT_func = grid_traverse.get_function(shape, \
        jinja_env.get_template('simplewave_multAT.cu').render(w2=omega**2, zz=shape[2]), \
        (cuda_type, 's0'), (cuda_type, 's1'), \
        (cuda_type, 'u'), (cuda_type, 'v'))
    def multAT(x, y):
        mAT_func(ds0, ds1, x, y)
        return

    def dot(x, y):
        return ga.dot(x, y).get()
     
    def axby(a, x, b, y):
        y.set(y.mul_add(b, x, a).get())
        return

    def copy(x):
        y = ga.empty_like(x)
        y.set(x.get())
        return y

    return multA, multAT, \
            {   'dot': dot, \
                'axby': axby, \
                'copy': copy}

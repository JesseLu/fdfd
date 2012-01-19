from jinja2 import Environment, PackageLoader
from my_cs import grid_traverse
from my_cs import dist_grid as dg
import stretched_coords
import numpy as np
# Implements multA, multAT, dot, axby, and copy for a simple 1D wave equation.

# Execute when module is loaded.
# Load the jinja environment.
jinja_env = Environment(loader=PackageLoader(__name__, 'templates'))

def get_ops(shape, omega, b, t_pml=10):
    sc0 = dg.Grid(stretched_coords.get_coeffs(shape[2], 0.0, t_pml, omega).astype(np.complex128))
    sc1 = dg.Grid(stretched_coords.get_coeffs(shape[2], 0.5, t_pml, omega).astype(np.complex128))

    if b.dtype.type is np.complex128:
        cuda_type = 'pycuda::complex<double>'
    elif b.dtype.type is np.complex64:
        cuda_type = 'pycuda::complex<float>'
    else:
        print 'error on data type of b'


    mA_func = grid_traverse.TraverseKernel(shape, \
        jinja_env.get_template('simplewave_multA.cu').render(w2=omega**2, zz=shape[2]), \
        (cuda_type, 's0__f'), (cuda_type, 's1__f'), \
        (cuda_type, 'u'), (cuda_type, 'v'))
    def multA(x, y):
        mA_func(sc0, sc1, x, y)
        return

    mAT_func = grid_traverse.TraverseKernel(shape, \
        jinja_env.get_template('simplewave_multAT.cu').render(w2=omega**2, zz=shape[2]), \
        (cuda_type, 's0__f'), (cuda_type, 's1__f'), \
        (cuda_type, 'u'), (cuda_type, 'v'))
    def multAT(x, y):
        mAT_func(sc0, sc1, x, y)
        return

    def dot(x, y):
        return x.dot(y)
     
    def axby(a, x, b, y):
        y.aby(b, a, x)

    def copy(x):
        return x.dup()
    
    return dg.Grid(b), \
            {   'multA': multA, \
                'multAT': multAT, \
                'dot': dot, \
                'axby': axby, \
                'copy': copy}

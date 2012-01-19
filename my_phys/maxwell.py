from jinja2 import Environment, PackageLoader
from my_cs import grid_traverse
from my_cs import dist_grid as dg
import numpy as np
# Implements multA, multAT, dot, axby, and copy for Maxwell's EM equations (3D).

# Execute when module is loaded.
# Load the jinja environment.
jinja_env = Environment(loader=PackageLoader(__name__, 'templates'))


class VecField:
    def __init__(self, *f0):
        self.f = [dg.Grid(field) for field in f0]

    def dup(self):
        v = VecField()
        v.f = [field.dup() for field in self.f]
        return v

    def dot(self, v):
        return sum([self.f[k].dot(v.f[k]) for k in range(len(self.f))])

    def aby(self, a, b, v):
        for k in range(len(self.f)):
            self.f[k].aby(a, b, v.f[k])

def get_ops(omega, b):
    """ define the operations """

    def copy(x):
        return x.dup()

    def dot(x, y):
        return x.dot(y)

    def axby(a, x, b, y):
        y.aby(b, a, x)

    shape = b[0].shape
    cuda_type = 'pycuda::complex<double>'
    field_names = ('Ex', 'Ey', 'Ez', 'Ax', 'Ay', 'Az')
    mA_func = grid_traverse.get_function(shape, \
        jinja_env.get_template('maxwell_multA.cu').\
            render(w2=omega**2, dims=shape, type=cuda_type), \
        *[(cuda_type, name) for name in field_names])
    def multA(x, y):
        mA_func(x.f[0], x.f[1], x.f[2], y.f[0], y.f[1], y.f[2])
        return

    def multAT(x, y):
        mA_func(x.f[0], x.f[1], x.f[2], y.f[0], y.f[1], y.f[2])
        return

    return  {'multA': multA, 'multAT': multAT, 'copy': copy, 'dot': dot, 'axby': axby}, VecField(*b)

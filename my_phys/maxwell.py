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

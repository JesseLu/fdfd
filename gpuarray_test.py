import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import pycuda.gpuarray as ga
import numpy as np
import my_traverse
from jinja2 import Environment, PackageLoader
from solvers import bicg

shape = (1, 2, 10)
env = Environment(loader=PackageLoader(__name__, 'templates'))
code = env.get_template('d2.cu')
src = my_traverse.fd_kernel(  'testfunc', \
                        'pycuda::complex<float>', \
                        ('u',), \
                        shape, \
                        code.render(zzm1=shape[2]-1, w2=0))
# print src
mod = SourceModule(src)
E_update = mod.get_function('testfunc')
u = ga.zeros(shape, np.complex64)
u.set(np.arange(np.prod(shape)).astype(np.complex64))
print ga.dot(u, u)
b0 = np.zeros(shape).astype(np.complex64)
b0[0,0,0] = 1.
b = ga.zeros(shape, np.complex64)
b.set(b0) 

E_update(u.gpudata, block=shape[::-1], grid=(1,1))
print u.get()
# def multA(u):
#     E_update(u.gpudata, block=shape[::-1], grid=(1,1))
#     return u
# 
# test = ga.dot(u, u)
# rho = bicg.solve(multA, multA, b, ga.zeros(shape, np.float32))
# print rho

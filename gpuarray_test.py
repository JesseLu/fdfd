import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import pycuda.gpuarray as ga
import numpy as np
import my_traverse
from jinja2 import Environment, PackageLoader, Template
from solvers import bicg
import stretched_coords

shape = (1, 1, 100)
omega = 0.3;
s0 = stretched_coords.get_coeffs(shape[2], 0.0, 2, omega)
ds0 = ga.zeros(shape, np.complex128) + 1
s1 = stretched_coords.get_coeffs(shape[2], 0.5, 2, omega)
ds1 = ga.zeros(shape, np.complex128) + 1
# ds0.set(s0.astype(np.complex128))
# ds1.set(s1.astype(np.complex128))
env = Environment(loader=PackageLoader(__name__, 'templates'))
code = env.get_template('d2.cu')
code1 = Template("""
    if (k == 0) 
        v(0,0,0) = u(0,0,0) - u(0,0,{{ zz-1 }});
    else
        v(0,0,0) = u(0,0,0) - u(0,0,-1);
    """)
code2 = Template("""
    if (k == {{ zz-1 }}) 
        v(0,0,0) = u(0,0,0) - u(0,0,-{{ zz-1 }});
    else
        v(0,0,0) = u(0,0,0) - u(0,0,1);
    """)
src = my_traverse.fd_kernel(  'testfunc', \
                        'pycuda::complex<double>', \
                        ('v', 'u'), \
                        shape, \
                        code1.render(zz=shape[2]))
mod = SourceModule(src)
d1 = mod.get_function('testfunc')
src = my_traverse.fd_kernel(  'testfunc', \
                        'pycuda::complex<double>', \
                        ('v', 'u'), \
                        shape, \
                        code2.render(zz=shape[2]))
mod = SourceModule(src)
d2 = mod.get_function('testfunc')
u = ga.zeros(shape, np.complex128)
u0 = np.zeros(shape).astype(np.complex128)
u0[0,0,shape[2]/2] = 0 + 1j;
u.set(u0)
v = ga.zeros_like(u)

# d1(v.gpudata, ds0.gpudata, u.gpudata, block=shape[::-1], grid=(1,1))
# print v.get()
# d2(v.gpudata, ds1.gpudata, u.gpudata, block=shape[::-1], grid=(1,1))
# print v.get()

def multA(u):
    v0 = ga.empty_like(u)
    v1 = ga.empty_like(u)
    d1(v0.gpudata, u.gpudata, block=shape[::-1], grid=(1,1))
    v0 = v0 * ds0
    d2(v1.gpudata, v0.gpudata, block=shape[::-1], grid=(1,1))
    v1 = v1 * ds1
    return v1 - omega**2 * u

def multAT(u):
    v0 = ga.empty_like(u)
    v1 = ga.empty_like(u)
    d2(v0.gpudata, (u * ds1).gpudata, block=shape[::-1], grid=(1,1))
    d1(v1.gpudata, (v0 * ds0).gpudata, block=shape[::-1], grid=(1,1))
    return v1 - omega**2 * u


x, err = bicg.solve1(multA, multAT, u, v, v*1, max_iters=1000)
print err.size, 'iterations ending with', err[-3:]

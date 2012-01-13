from jinja2 import Environment, PackageLoader, Template
import numpy as np
from my_math import bicg
from my_phys import stretched_coords
from my_cs import grid_traverse
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import pycuda.gpuarray as ga

shape = (1, 1, 100)
omega = 0.3;
s0 = stretched_coords.get_coeffs(shape[2], 0.0, 10, omega)
ds0 = ga.zeros(shape, np.complex128) + 1
s1 = stretched_coords.get_coeffs(shape[2], 0.5, 10, omega)
ds1 = ga.zeros(shape, np.complex128) + 1
ds0.set(s0.astype(np.complex128))
ds1.set(s1.astype(np.complex128))
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
cuda_type = 'pycuda::complex<double>'
d1 = grid_traverse.get_function(shape, code1.render(zz=shape[2]), \
            (cuda_type, 'v'), (cuda_type, 'u'))
d2 = grid_traverse.get_function(shape, code2.render(zz=shape[2]), \
            (cuda_type, 'v'), (cuda_type, 'u'))
u = ga.zeros(shape, np.complex128)
u0 = np.zeros(shape).astype(np.complex128)
u0[0,0,shape[2]/2] = 1 + 0j;
u.set(u0)
v = ga.zeros_like(u)

# d1(v.gpudata, ds0.gpudata, u.gpudata, block=shape[::-1], grid=(1,1))
# print v.get()
# d2(v.gpudata, ds1.gpudata, u.gpudata, block=shape[::-1], grid=(1,1))
# print v.get()

def multA(u):
    v0 = ga.empty_like(u)
    v1 = ga.empty_like(u)
    # d1(v0.gpudata, u.gpudata, block=shape[::-1], grid=(1,1))
    d1(v0, u)
    v0 = v0 * ds0
    d2(v1, v0)
    # d2(v1.gpudata, v0.gpudata, block=shape[::-1], grid=(1,1))
    v1 = v1 * ds1
    return v1 - omega**2 * u

def multAT(u):
    v0 = ga.empty_like(u)
    v1 = ga.empty_like(u)
    # d1(v0.gpudata, (u * ds1).gpudata, block=shape[::-1], grid=(1,1))
    d1(v0, u * ds1)
    # d2(v1.gpudata, (v0 * ds0).gpudata, block=shape[::-1], grid=(1,1))
    d2(v1, v0 * ds0)
    return v1 - omega**2 * u

x, err = bicg.solve1(multA, multAT, u, v, v*1, max_iters=1000)
print err.size, 'iterations ending with', err[-3:]
y = x.get()

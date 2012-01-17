from jinja2 import Template
import numpy as np
from my_math import bicg
from my_phys import stretched_coords, simple_wave
from my_cs import grid_traverse
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import pycuda.gpuarray as ga

# s0 = stretched_coords.get_coeffs(shape[2], 0.0, 10, omega)
# ds0 = ga.zeros(shape, np.complex128) + 1
# s1 = stretched_coords.get_coeffs(shape[2], 0.5, 10, omega)
# ds1 = ga.zeros(shape, np.complex128) + 1
# ds0.set(s0.astype(np.complex128))
# ds1.set(s1.astype(np.complex128))
# code1 = Template("""
#     if (k == 0) 
#         v(0,0,0) = u(0,0,0) - u(0,0,{{ zz-1 }});
#     else
#         v(0,0,0) = u(0,0,0) - u(0,0,-1);
#     """)
# code2 = Template("""
#     if (k == {{ zz-1 }}) 
#         v(0,0,0) = u(0,0,0) - u(0,0,-{{ zz-1 }});
#     else
#         v(0,0,0) = u(0,0,0) - u(0,0,1);
#     """)
# cuda_type = 'pycuda::complex<double>'
# d1 = grid_traverse.get_function(shape, simple_wave.back_diff(shape[2]), \
#             (cuda_type, 'v'), (cuda_type, 'u'))
# d2 = grid_traverse.get_function(shape, simple_wave.forw_diff(shape[2]), \
#             (cuda_type, 'v'), (cuda_type, 'u'))
# b = np.zeros(shape).astype(np.complex128)
# b[0,0,shape[2]/2] = 1 + 0j;
# b.to_gpu(b)
# y = ga.zeros_like(b)
# 
# d1(v.gpudata, ds0.gpudata, u.gpudata, block=shape[::-1], grid=(1,1))
# print v.get()
# d2(v.gpudata, ds1.gpudata, u.gpudata, block=shape[::-1], grid=(1,1))
# print v.get()
# 
# def multA(u, y):
#     v0 = ga.empty_like(u)
#     v1 = ga.empty_like(u)
#     # d1(v0.gpudata, u.gpudata, block=shape[::-1], grid=(1,1))
#     d1(v0, u)
#     v0 = v0 * ds0
#     d2(v1, v0)
#     # d2(v1.gpudata, v0.gpudata, block=shape[::-1], grid=(1,1))
#     v1 = -v1 * ds1
#     y.set((v1 - omega**2 * u).get())
#     return
# 
# def multAT(u, y):
#     v0 = ga.empty_like(u)
#     v1 = ga.empty_like(u)
#     # d1(v0.gpudata, (u * ds1).gpudata, block=shape[::-1], grid=(1,1))
#     d1(v0, u * ds1)
#     # d2(v1.gpudata, (v0 * ds0).gpudata, block=shape[::-1], grid=(1,1))
#     d2(v1, v0 * ds0)
#     y.set((-v1 - omega**2 * u).get())
#     return
# 
# def my_dot(x, y):
#     return ga.dot(x, y).get()
#  
# def my_axby(a, x, b, y):
#     y.set(y.mul_add(b, x, a).get())
#     return
# 
# def my_copy(x):
#     y = ga.empty_like(x)
#     y.set(x.get())
#     return y
# 
shape = (1, 1, 40)
omega = 0.3;
b = np.zeros(shape).astype(np.complex128)
b[0,0,shape[2]/2] = 1 + 0j;
b = ga.to_gpu(b)
y = ga.zeros_like(b) 
multA, multAT, ops = simple_wave.get_ops(shape, omega)
multAT(b, y)
print y.get()
multA(b, y)
print y.get()
x, err = bicg.solve_asymm(multA, multAT, b, **ops)
# x, err = bicg.solve_asymm(multA, multAT, b, \
#                 dot=my_dot, axby=my_axby, copy=my_copy)
print err.size, 'iterations ending with', err[-3:]

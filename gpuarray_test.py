import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import pycuda.gpuarray as ga
import numpy as np
import my_traverse
from jinja2 import Environment, PackageLoader

shape = (1, 1, 10)
env = Environment(loader=PackageLoader(__name__, 'templates'))
code = env.get_template('d2.cu')
src = my_traverse.fd_kernel(  'testfunc', \
                        'float', \
                        ('u',), \
                        shape, \
                        code.render(zzm1=shape[2]-1))
print src
mod = SourceModule(src)
E_update = mod.get_function('testfunc')
u = ga.zeros(shape, np.float32)
u.set(np.arange(shape[2]).astype(np.float32))

E_update(u.gpudata, block=shape[::-1], grid=(1,1))
print u.get()

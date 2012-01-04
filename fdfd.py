import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import numpy as np
from jinja2 import Environment, PackageLoader
import my_traverse

env = Environment(loader=PackageLoader(__name__, 'templates'))
src_macros = env.get_template('my_cuda_macros.cu')
src_update = env.get_template('simple_update.cu')
# device = pycuda.autoinit.device


# Choose the type
python_type = np.float32
cuda_type = 'float'

# Shape of the field
field_shape = (3,4,5)

# Source
code = """
        Ex(0,0,1) = k;
        Ey(0,0,0) = 7.0;
    """


# print device.get_attributes()
src = my_traverse.fd_kernel('E_update', \
                            cuda_type, \
                            ('Ex', 'Ey', 'Ez'), \
                            field_shape, \
                            code)
print src
# src = src_macros.render() + \
#     src_update.render(  function_name='E_update', \
#                         dims=field_shape, \
#                         cuda_type=cuda_type, \
#                         fields=('Ex', 'Ey', 'Ez'), \
#                         code=source)
# print src
mod = SourceModule(src)

E_update = mod.get_function('E_update')
Ex = np.zeros(field_shape).astype(python_type)
Ey = np.zeros(field_shape).astype(python_type)
Ez = np.zeros(field_shape).astype(python_type)
E_update(drv.InOut(Ex), drv.InOut(Ey), drv.InOut(Ez), block=(1,2,1), grid=(5,2))
print Ex

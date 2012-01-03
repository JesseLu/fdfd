import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import numpy as np
import h5py
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader(__name__, 'templates'))
src_macros = env.get_template('my_cuda_macros.cu')
src_update = env.get_template('simple_update.cu')
# device = pycuda.autoinit.device


# Choose the type
python_type = np.float64
cuda_type = 'double'

# Shape of the field
field_shape = (3,4,5)

# Source
source = """
        Ey(i,j,k) = 7.0;
        """


# print device.get_attributes()
src = src_macros.render() + \
    src_update.render(  function_name='E_update', \
                        field_shape=field_shape, \
                        cuda_type=cuda_type, \
                        fields=('Ex', 'Ey', 'Ez'), \
                        code=source)
print src
mod = SourceModule(src)

E_update = mod.get_function('E_update')
Ex = np.zeros(field_shape).astype(python_type)
Ey = np.zeros(field_shape).astype(python_type)
Ez = np.zeros(field_shape).astype(python_type)
E_update(drv.InOut(Ex), drv.InOut(Ey), drv.InOut(Ez), block=(5,4,3), grid=(1,1))
print Ey
#     
# 
# mult = mod.get_function("mult");
# x = np.zeros((4, 4, 3)).astype(python_type)
# y = np.zeros((4, 4, 3)).astype(python_type)
# z = np.zeros((4, 4, 3)).astype(python_type)
# 
# mult(drv.InOut(x), drv.InOut(y), drv.InOut(z), block=(1,1,4), grid=(3,4))
# print x
# print y
# print z

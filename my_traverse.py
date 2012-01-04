# import pycuda.driver as drv
# from pycuda.compiler import SourceModule
# import pycuda.gpuarray as ga
from jinja2 import Environment, PackageLoader

def fd_kernel(function_name, cuda_type, fields, shape, source):
    env = Environment(loader=PackageLoader(__name__, 'templates'))
    src_macros = env.get_template('my_cuda_macros.cu')
    src_update = env.get_template('update.cu')

    src = src_macros.render() + \
        src_update.render(  function_name='E_update', \
                            dims=shape, \
                            cuda_type=cuda_type, \
                            fields=('Ex', 'Ey', 'Ez'), \
                            code=source)
    return src

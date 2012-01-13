from pycuda import compiler
from jinja2 import Environment, PackageLoader

# Execute when module is loaded.
# Load the jinja environment.
jinja_env = Environment(loader=PackageLoader(__name__, 'templates'))

def get_function(shape, code, *params):
    """Return a cuda function that will execute on a grid.

    Input arguments:
    shape -- the size of the grid.
    code -- the CUDA source code to be executed at every cell.
    *params -- (type, name) tuples of the input parameters.

    Output arguments:
    wrapped_fun -- a function that accepts a list of pycuda.gpuarray.GPUArray
        objects as well as pycuda.driver.Function.__call__ keyword arguments.

    Examples:
    # Form a simple cuda function that doubles elements of an array.
    import numpy as np
    from pycuda import gpuarray as ga
    from my_cs import grid_traverse
    x = ga.zeros((2,3,4), np.float32) + 1
    double_it = grid_traverse.get_function( (2,3,4), 
                                            'x(0,0,0) *= 2', 
                                            ('float', 'x'))
    double_it(x)
        print x.get()
    """
    # Get the template and render it using jinja2.
    template = jinja_env.get_template('traverse.cu') 
    cuda_source = template.render(  params=params, \
                                    dims=shape, \
                                    loop_code=code)

    # Compile the code.
    mod = compiler.SourceModule(cuda_source)
    fun = mod.get_function('traverse')

    # Wrapper for the function, so we don't need to deal with inverting
    # the block and grid shapes.
    # TODO: allow keyword arguments to be passed to the pycuda function call.
    # TODO: allow for default optimized block and grid shape function call.
    def wrapped_fun(*gpu_arrays):
        fun(*[ga.gpudata for ga in gpu_arrays], block=shape[::-1], grid=(1,1))

    return wrapped_fun

    

def fd_kernel(function_name, cuda_type, fields, shape, source):
    env = Environment(loader=PackageLoader(__name__, 'templates'))
    src_macros = env.get_template('my_cuda_macros.cu')
    src_complex = env.get_template('my_complex_macros.cu')
    src_update = env.get_template('update.cu')

    src = src_macros.render() + src_complex.render() + \
        src_update.render(  function_name=function_name, \
                            dims=shape, \
                            cuda_type=cuda_type, \
                            fields=fields, \
                            code=source)
    return src

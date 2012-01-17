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
    from my_cs import grid_traverse, dist_grid
    x = dist_grid.Grid(np.ones(2,3,4).astype(np.float32))
    double_it = grid_traverse.get_function( (2,3,4), 
                                            'x(0,0,0) *= 2', 
                                            ('float', 'x'))
    double_it(x)
    print x.ary.get()
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
    def wrapped_fun(*grids):
        fun(*[grid.g.gpudata for grid in grids], block=shape[::-1], grid=(1,1))

    return wrapped_fun

    

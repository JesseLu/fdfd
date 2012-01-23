from pycuda import compiler
from jinja2 import Environment, PackageLoader
import numpy as np

# Execute when module is loaded.
# Load the jinja environment.
jinja_env = Environment(loader=PackageLoader(__name__, 'templates'))

class TraverseKernel():
    def __init__(self, shape, code, *params):
        """Return a cuda function that will execute on a grid.

        Input arguments:
        shape -- the size of the grid.
        code -- the CUDA source code to be executed at every cell.
        *params -- (type, name) tuples of the input parameters.

        Output arguments:
        wrapped_fun -- a function that accepts a list of pycuda.gpuarray.GPUArray
            objects as well as pycuda.driver.Function.__call__ keyword arguments.
        """

        # Initialize parameters.
        self.shape = shape # Size of the simulation.
        self.block_shapes, self.grid_shapes = _get_shapes(shape)

        # Get the template and render it using jinja2.
        template = jinja_env.get_template('traverse.cu') 
        cuda_source = template.render(  params=params, \
                                        dims=self.shape, \
                                        loop_code=code, \
                                        flat_tag='_f')
        # print cuda_source
        # Compile the code into a callable cuda function.
        mod = compiler.SourceModule(cuda_source)
        self.fun = mod.get_function('traverse')


    def __call__(self, *grids):
#         # TODO: allow keyword arguments to be passed to the pycuda function call.
#         # TODO: allow for default optimized block and grid shape function call.
        self.fun(*[grid.g.gpudata for grid in grids], \
                block=self.block_shapes[::-1], grid=self.grid_shapes[2:0:-1])

def _get_shapes(shape):
    block_shapes = (1, 16, 16)
    grid_shapes = (1, int(np.ceil(shape[1]/block_shapes[1]) + 1), \
                    int(np.ceil(shape[2]/block_shapes[2]) + 1))
    return block_shapes, grid_shapes

    

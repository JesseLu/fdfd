from pycuda import gpuarray as ga
import numpy as np

class Grid:
    def __init__(self, np_array):
        self.g = ga.to_gpu(np_array) # Copy data to the GPU.

    def dup(self):
        return Grid(self.g.get()) # This should be changed to a d-d copy.
        
    def dot(self, y):
        return ga.dot(self.g, y.g).get()

    def aby(self, a, b, y):
        # See if this is faster without the creation of a new GPUArray.
        # self.g.set(self.g.mul_add(a, y.g, b).get())
        x = self.g.mul_add(a, y.g, b).get()
        self.g.set(x)
    

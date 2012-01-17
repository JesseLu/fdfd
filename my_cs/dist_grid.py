from pycuda import gpuarray as ga
import numpy as np
class Grid:
    def __init__(self, np_array):
        self.ary = ga.to_gpu(np_array) # Copy data to the GPU.

    def dup(self):
        return Grid(self.ary.get())
        
    def dot(self, y):
        return ga.dot(self.ary, y.ary).get()

    def aby(self, a, b, y):
        self.ary.set(self.ary.mul_add(a, y.ary, b).get())
    

from jinja2 import Template
from my_cs import grid_traverse
import stretched_coords
from pycuda import gpuarray as ga
import numpy as np
# Implements multA, multAT, dot, axby, and copy for a simple 1D wave equation.

def get_ops(shape, omega):
    n = shape[2]
    ds0 = ga.to_gpu(stretched_coords.get_coeffs(shape[2], 0.0, 10, omega))
    ds1 = ga.to_gpu(stretched_coords.get_coeffs(shape[2], 0.5, 10, omega))
    cuda_type = 'pycuda::complex<double>'
    d1 = grid_traverse.get_function(shape, back_diff(shape[2]), \
                (cuda_type, 'v'), (cuda_type, 'u'))
    d2 = grid_traverse.get_function(shape, forw_diff(shape[2]), \
                (cuda_type, 'v'), (cuda_type, 'u'))

    code = Template("""
        int prev, next;
        if (k == 0) 
            prev = {{ zz-1 }};
        else
            prev = -1;

        if (k == {{ zz-1 }})
            next = {{ -(zz-1) }};
        else
            next = 1;

        v(0,0,0) = -s1(0,0,0) * 
                (s0(0,0,next) * (u(0,0,next) - u(0,0,0)) - 
                s0(0,0,0) * (u(0,0,0) - u(0,0,prev))) - 
                {{ w2 }} * u(0,0,0); 
            """).render(w2=omega**2, zz=shape[2])
    mA_func = grid_traverse.get_function(shape, code, \
        (cuda_type, 's0'), (cuda_type, 's1'), \
        (cuda_type, 'u'), (cuda_type, 'v'))
    def mA(x, y):
        mA_func(ds0, ds1, x, y)
        return

    def multA(x, y):
        t0 = ga.empty_like(x)
        t1 = ga.empty_like(x)
        d1(t0, x)
        d2(t1, t0 * ds0)
        t1 = -t1 * ds1
        y.set((t1 - omega**2 * x).get())
        return

    def multAT(x, y):
        t0 = ga.empty_like(x)
        t1 = ga.empty_like(x)
        d1(t0, x * ds1)
        d2(t1, t0 * ds0)
        y.set((-t1 - omega**2 * x).get())
        return

    def my_dot(x, y):
        return ga.dot(x, y).get()
     
    def my_axby(a, x, b, y):
        y.set(y.mul_add(b, x, a).get())
        return

    def my_copy(x):
        y = ga.empty_like(x)
        y.set(x.get())
        return y

    return mA, multAT, \
            {   'dot': my_dot, \
                'axby': my_axby, \
                'copy': my_copy}

def forw_diff(n):
    code = Template("""
        if (k == {{ zz-1 }}) 
            v(0,0,0) = u(0,0,-{{ zz-1 }}) - u(0,0,0);
        else
            v(0,0,0) = u(0,0,1) - u(0,0,0);
        """)
    return code.render(zz=n)


def back_diff(n):
    code = Template("""
        if (k == 0) 
            v(0,0,0) = u(0,0,0) - u(0,0,{{ zz-1 }});
        else
            v(0,0,0) = u(0,0,0) - u(0,0,-1);
        """)
    return code.render(zz=n)

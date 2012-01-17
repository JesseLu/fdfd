// These macros redefine the CUDA blocks and grids to be row-major,
// instead of column major.

#define tx threadIdx.z
#define ty threadIdx.y
#define tz threadIdx.x

#define bx blockIdx.z
#define by blockIdx.y
#define bz blockIdx.x

#define txx blockDim.z
#define tyy blockDim.y
#define tzz blockDim.x

#define bxx gridDim.z
#define byy gridDim.y
#define bzz gridDim.x


// Use the complex-value definition and operators included with pycuda.
// This allows us to work with pycuda's GPUArray class.
#include <pycuda-complex.hpp>


// Defines row major access to a 3D array.
// sx, sy, sz are shifts from the present location of the field.
#define MY_OFFSET(sx,sy,sz) sx * {{ dims[1] }} * {{ dims[2] }} + sy * {{ dims[2] }} + sz 


// Macros to access fields using the field(i,j,k) format,
// where sx, sy, and sz are RELATIVE offsets in the x, y, and z directions
// respectively.
{%- for param in params%} 
#define {{ param[1] }}(sx,sy,sz) {{ param[1] }}[MY_OFFSET(sx,sy,sz)]
{%- endfor %} 

{%- for param in params%} 
#define {{ param[1] }}_abs(sx,sy,sz) {{ param[1] }}[MY_OFFSET(sx-i,sy-j,sz-k)]
{%- endfor %} 

__global__ void traverse(
    {#- Add the fields as input parameters to the function. -#}
    {%- for param in params -%} 
        {% if not loop.first -%}, {% endif -%} 
        {{ param[0] }} *{{ param[1] }}
    {%- endfor -%}) 
{
    // Set the index variables. Only i will change, since we only traverse
    // the grid in the x-direction.
    int i = tx + txx * bx;
    const int j = ty + tyy * by;
    const int k = tz + tzz * bz;

    // Set the field pointers to the appropriate location 
    // for the current thread.
    {%- for param in params %} 
    {{ param[1] }} += MY_OFFSET(i,j,k);
    {%- endfor %} 

    // User-defined "pre-loop" code.
    {{ preloop_code }}

    for (; i < {{ dims[0] }} ; i += txx) {
        // User-defined "loop" code.
        {{ loop_code }}

        // Increment the pointers, in order to scan through the entire grid
        // in the x-direction.
        {%- for param in params %} 
        {{ param[1] }} += MY_OFFSET(txx,0,0);
        {%- endfor %} 
    }

    // User-defined "post-loop" code.
    {{ postloop_code }}
}




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



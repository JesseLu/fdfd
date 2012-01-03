
__global__ void mult({{ type }} *x, {{ type }} *y, {{ type }} *z) {
    int i = tx + txx * bx;
    int j = ty + tyy * by;
    int k = tz + tzz * bz;
    int ind = i * {{ dims[1] }} * {{ dims[2] }} + j * {{ dims[2] }} + k;
    x[ind] = bx;
    y[ind] = by;
    z[ind] = bz;
}

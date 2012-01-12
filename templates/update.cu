// Defines row major access to a 3D array.
// sx, sy, sz are shifts from the present location of the field.
#define MY_OFFSET(sx,sy,sz) sx * {{ dims[1] }} * {{ dims[2] }} + sy * {{ dims[2] }} + sz 

// Macros to access fields using the field(i,j,k) format.
{%- for field in fields %} 
#define {{field}}(i,j,k) {{field}}[MY_OFFSET(i,j,k)]
{%- endfor %} 

__global__ void {{ function_name }}(
    {#- Add the fields as input parameters to the function. -#}
    {%- for field in fields -%} 
        {% if not loop.first -%}, {% endif -%} 
        {{ cuda_type }} *{{field}}
    {%- endfor -%}) 
{
    // Set the index variables. Only i will change, since we only traverse
    // the grid in the x-direction.
    int i = tx + txx * bx;
    const int j = ty + tyy * by;
    const int k = tz + tzz * bz;

    // Set the field pointers to the appropriate location 
    // for the current thread.
    {%- for field in fields %} 
    {{field}} += MY_OFFSET(i,j,k);
    {%- endfor %} 

    for (; i < {{ dims[0] }} ; i += txx) {
        // Begin user-defined loop code.
        {{ code }}
        // End user-defined loop code.

        // Increment the pointers, in order to scan through the entire grid
        // in the x-direction.
        {%- for field in fields %} 
        {{field}} += MY_OFFSET(1,0,0);
        {%- endfor %} 
    }
}

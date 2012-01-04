// Defines row major access to a 3D array.
#define IND(i,j,k) i * {{ dims[1] }} * {{ dims[2] }} + j * {{ dims[2] }} + k

// Macros to access fields using the field(i,j,k) format.
{%- for field in fields %} 
#define {{field}}(i,j,k) {{field}}[IND(i,j,k)]
{%- endfor %} 

__global__ void {{ function_name }}(
    {# Add the fields as input parameters to the function. #}
    {%- for field in fields -%} 
        {% if not loop.first -%}, {% endif -%} 
        {{ cuda_type }} *{{field}}
    {%- endfor -%}) 
{
    const int j = ty + tyy * by;
    const int k = tz + tzz * bz;
    for (int i = tx + txx * bx; i < {{dims[0] }} ; i += txx) {
    {{ code }}
    }
}

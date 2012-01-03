// Make it simpler to access different field elements
#define IND(i,j,k) \
    i * {{ field_shape[1] }} * {{ field_shape[2] }} + \
    j * {{ field_shape[2] }} + \
    k

#define Ey(i,j,k) Ey[IND(i,j,k)]


__global__ void {{ function_name }}(
    {%- for field in fields -%} 
        {% if not loop.first -%}, {% endif -%} 
        {{ cuda_type }} *{{field}}
    {%- endfor -%}) 
{
    const int j = ty + tyy * by;
    const int k = tz + tzz * bz;
    for (int i = tx + txx * bx; i < {{field_shape[0] }} ; i += txx) {
    {{ code }}
    }
}

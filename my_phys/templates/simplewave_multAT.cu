        int prev, next; // relative indices for adjacent points.
        if (k == 0) 
            prev = {{ zz-1 }};
        else
            prev = -1;

        if (k == {{ zz-1 }})
            next = {{ -(zz-1) }};
        else
            next = 1;

        // Update equation.
        v(0,0,0) = -(s0__f[k+next] * (s1__f[k+next] * u(0,0,next) - s1__f[k] * u(0,0,0)) - 
                s0__f[k] * (s1__f[k] * u(0,0,0) - s1__f[k+prev] * u(0,0,prev))) - 
                double({{ w2 }}) * u(0,0,0); 

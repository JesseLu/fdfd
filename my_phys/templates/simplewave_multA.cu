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
        v(0,0,0) = -s1(0,0,0) * 
                (s0(0,0,next) * (u(0,0,next) - u(0,0,0)) - 
                s0(0,0,0) * (u(0,0,0) - u(0,0,prev))) - 
                double({{ w2 }}) * u(0,0,0); 

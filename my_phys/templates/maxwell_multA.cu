
        int in, ip, jn, jp, kn, kp; // relative ipdices for adjacept noipts.

        if (i == 0) 
            in = {{ dims[0]-1 }};
        else
            in = -1;

        if (i == {{ dims[0]-1 }})
            ip = {{ -(dims[0]-1) }};
        else
            ip = 1;

        if (j == 0) 
            jn = {{ dims[1]-1 }};
        else
            jn = -1;

        if (j == {{ dims[1]-1 }})
            jp = {{ -(dims[1]-1) }};
        else
            jp = 1;

        if (k == 0) 
            kn = {{ dims[2]-1 }};
        else
            kn = -1;

        if (k == {{ dims[2]-1 }})
            kp = {{ -(dims[2]-1) }};
        else
            kp = 1;

        // Update equation.
        {{ type }} Hx_0 = (Ey(0,0,0) - Ey(0,0,kp)) - (Ez(0,0,0) - Ez(0,jp,0));
        {{ type }} Hx_jn = (Ey(0,jn,0) - Ey(0,jn,kp)) - (Ez(0,jn,0) - Ez(0,0,0));
        {{ type }} Hx_kn = (Ey(0,0,kn) - Ey(0,0,0)) - (Ez(0,0,kn) - Ez(0,jp,kn));
        {{ type }} Hy_0 = (Ez(0,0,0) - Ez(ip,0,0)) - (Ex(0,0,0) - Ex(0,0,kp));
        {{ type }} Hy_in = (Ez(in,0,0) - Ez(0,0,0)) - (Ex(in,0,0) - Ex(in,0,kp));
        {{ type }} Hy_kn = (Ez(0,0,kn) - Ez(ip,0,kn)) - (Ex(0,0,kn) - Ex(0,0,0));
        {{ type }} Hz_0 = (Ex(0,0,0) - Ex(0,jp,0)) - (Ey(0,0,0) - Ey(ip,0,0));
        {{ type }} Hz_in = (Ex(in,0,0) - Ex(in,jp,0)) - (Ey(in,0,0) - Ey(0,0,0));
        {{ type }} Hz_jn = (Ex(0,jn,0) - Ex(0,0,0)) - (Ey(0,jn,0) - Ey(ip,jn,0));

        Ax(0,0,0) = (Hy_0 - Hy_kn) - (Hz_0 - Hz_jn) - {{ w2 }} * Ex(0,0,0);
        Ay(0,0,0) = (Hz_0 - Hz_in) - (Hx_0 - Hx_kn) - {{ w2 }} * Ey(0,0,0);
        Az(0,0,0) = (Hx_0 - Hx_jn) - (Hy_0 - Hy_in) - {{ w2 }} * Ez(0,0,0);

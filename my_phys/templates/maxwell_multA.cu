        if ((i < {{ dims[0] }}) && (j < {{ dims[1] }}) && (k < {{ dims[2] }})) {
            int in, ip, jn, jp, kn, kp; // relative indices for adjacept points.

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
            {{ type }} Hx_0 =   sz1_f[k] * (Ey(0,0,0) - Ey(0,0,kp)) - 
                                sy1_f[j] * (Ez(0,0,0) - Ez(0,jp,0));
            {{ type }} Hx_jn =  sz1_f[k] * (Ey(0,jn,0) - Ey(0,jn,kp)) - 
                                sy1_f[j+jn] * (Ez(0,jn,0) - Ez(0,0,0));
            {{ type }} Hx_kn =  sz1_f[k+kn] * (Ey(0,0,kn) - Ey(0,0,0)) - 
                                sy1_f[j] * (Ez(0,0,kn) - Ez(0,jp,kn));

            {{ type }} Hy_0 =   sx1_f[i] * (Ez(0,0,0) - Ez(ip,0,0)) - 
                                sz1_f[k] * (Ex(0,0,0) - Ex(0,0,kp));
            {{ type }} Hy_in =  sx1_f[i+in] * (Ez(in,0,0) - Ez(0,0,0)) - 
                                sz1_f[k] * (Ex(in,0,0) - Ex(in,0,kp));
            {{ type }} Hy_kn =  sx1_f[i] * (Ez(0,0,kn) - Ez(ip,0,kn)) - 
                                sz1_f[k+kn] * (Ex(0,0,kn) - Ex(0,0,0));

            {{ type }} Hz_0 =   sy1_f[j] * (Ex(0,0,0) - Ex(0,jp,0)) - 
                                sx1_f[i] * (Ey(0,0,0) - Ey(ip,0,0));
            {{ type }} Hz_in =  sy1_f[j] * (Ex(in,0,0) - Ex(in,jp,0)) - 
                                sx1_f[i+in] * (Ey(in,0,0) - Ey(0,0,0));
            {{ type }} Hz_jn =  sy1_f[j+jn] * (Ex(0,jn,0) - Ex(0,0,0)) - 
                                sx1_f[i] * (Ey(0,jn,0) - Ey(ip,jn,0));

            Ax(0,0,0) = sy0_f[j] * (Hz_0 - Hz_jn) - sz0_f[k] * (Hy_0 - Hy_kn) 
                        - {{ w2 }} * Ex(0,0,0);
            Ay(0,0,0) = sz0_f[k] * (Hx_0 - Hx_kn) - sx0_f[i] * (Hz_0 - Hz_in) 
                        - {{ w2 }} * Ey(0,0,0);
            Az(0,0,0) = sx0_f[i] * (Hy_0 - Hy_in) - sy0_f[j] * (Hx_0 - Hx_jn) 
                        - {{ w2 }} * Ez(0,0,0);
        }

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

            {{ type }} Ex_000 = Ex(0,0,0);
            {{ type }} Ex_00p = Ex(0,0,kp);
            {{ type }} Ex_n0p = Ex(in,0,kp);
            {{ type }} Ex_n00 = Ex(in,0,0);
            {{ type }} Ex_00n = Ex(0,0,kn);
            {{ type }} Ex_0p0 = Ex(0,jp,0);
            {{ type }} Ex_np0 = Ex(in,jp,0);
            {{ type }} Ex_0n0 = Ex(0,jn,0);

            {{ type }} Ey_000 = Ey(0,0,0);
            {{ type }} Ey_00p = Ey(0,0,kp);
            {{ type }} Ey_0n0 = Ey(0,jn,0);
            {{ type }} Ey_0np = Ey(0,jn,kp);
            {{ type }} Ey_00n = Ey(0,0,kn);
            {{ type }} Ey_p00 = Ey(ip,0,0);
            {{ type }} Ey_n00 = Ey(in,0,0);
            {{ type }} Ey_pn0 = Ey(ip,jn,0);

            {{ type }} Ez_000 = Ez(0,0,0);
            {{ type }} Ez_0p0 = Ez(0,jp,0);
            {{ type }} Ez_0n0 = Ez(0,jn,0);
            {{ type }} Ez_00n = Ez(0,0,kn);
            {{ type }} Ez_0pn = Ez(0,jp,kn);
            {{ type }} Ez_p00 = Ez(ip,0,0);
            {{ type }} Ez_n00 = Ez(in,0,0);
            {{ type }} Ez_p0n = Ez(ip,0,kn);

            // Update equation.
            {{ type }} Hx_0 =   (sz0_f[k] * Ey_000 - sz0_f[k+kp] * Ey_00p) - 
                                (sy0_f[j] * Ez_000 - sy0_f[j+jp] * Ez_0p0);
            {{ type }} Hx_jn =  (sz0_f[k] * Ey_0n0 - sz0_f[k+kp] * Ey_0np) - 
                                (sy0_f[j+jn] * Ez_0n0 - sy0_f[j] * Ez_000);
            {{ type }} Hx_kn =  (sz0_f[k+kn] * Ey_00n - sz0_f[k] * Ey_000) - 
                                (sy0_f[j] * Ez_00n - sy0_f[j+jp] * Ez_0pn);

            {{ type }} Hy_0 =   (sx0_f[i] * Ez_000 - sx0_f[i+ip] * Ez_p00) - 
                                (sz0_f[k] * Ex_000 - sz0_f[k+kp] * Ex_00p);
            {{ type }} Hy_in =  (sx0_f[i+in] * Ez_n00 - sx0_f[i] * Ez_000) - 
                                (sz0_f[k] * Ex_n00 - sz0_f[k+kp] * Ex_n0p);
            {{ type }} Hy_kn =  (sx0_f[i] * Ez_00n - sx0_f[i+ip] * Ez_p0n) - 
                                (sz0_f[k+kn] * Ex_00n - sz0_f[k] * Ex_000);

            {{ type }} Hz_0 =   (sy0_f[j] * Ex_000 - sy0_f[j+jp] * Ex_0p0) - 
                                (sx0_f[i] * Ey_000 - sz0_f[i+ip] * Ey_p00);
            {{ type }} Hz_in =  (sy0_f[j] * Ex_n00 - sy0_f[j+jp] * Ex_np0) - 
                                (sx0_f[i+in] * Ey_n00 - sx0_f[i] * Ey_000);
            {{ type }} Hz_jn =  (sy0_f[j+jn] * Ex_0n0 - sy0_f[j] * Ex_000) - 
                                (sx0_f[i] * Ey_0n0 - sx0_f[i+ip] * Ey_pn0);

            Ax(0,0,0) = (sy1_f[j] * Hz_0 - sy1_f[j+jn] * Hz_jn) - 
                        (sz1_f[k] * Hy_0 - sz1_f[k+kp] * Hy_kn) - 
                        {{ w2 }} * Ex(0,0,0);
            Ay(0,0,0) = (sz1_f[k] * Hx_0 - sz1_f[k+kn] * Hx_kn) - 
                        (sx1_f[i] * Hz_0 - sx1_f[i+in] * Hz_in) - 
                        {{ w2 }} * Ey(0,0,0);
            Az(0,0,0) = (sx1_f[i] * Hy_0 - sx1_f[i+in] * Hy_in) - 
                        (sy1_f[j] * Hx_0 - sy1_f[j+jn] * Hx_jn) - 
                        {{ w2 }} * Ez(0,0,0);
        }

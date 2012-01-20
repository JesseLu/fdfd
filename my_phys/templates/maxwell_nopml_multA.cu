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
            {{ type }} Hx_0 =   (Ey_000 - Ey_00p) - (Ez_000 - Ez_0p0);
            {{ type }} Hx_jn =  (Ey_0n0 - Ey_0np) - (Ez_0n0 - Ez_000);
            {{ type }} Hx_kn =  (Ey_00n - Ey_000) - (Ez_00n - Ez_0pn);

            {{ type }} Hy_0 =   (Ez_000 - Ez_p00) - (Ex_000 - Ex_00p);
            {{ type }} Hy_in =  (Ez_n00 - Ez_000) - (Ex_n00 - Ex_n0p);
            {{ type }} Hy_kn =  (Ez_00n - Ez_p0n) - (Ex_00n - Ex_000);

            {{ type }} Hz_0 =   (Ex_000 - Ex_0p0) - (Ey_000 - Ey_p00);
            {{ type }} Hz_in =  (Ex_n00 - Ex_np0) - (Ey_n00 - Ey_000);
            {{ type }} Hz_jn =  (Ex_0n0 - Ex_000) - (Ey_0n0 - Ey_pn0);

            Ax(0,0,0) = (Hz_0 - Hz_jn) - (Hy_0 - Hy_kn) - {{ w2 }} * Ex(0,0,0);
            Ay(0,0,0) = (Hx_0 - Hx_kn) - (Hz_0 - Hz_in) - {{ w2 }} * Ey(0,0,0);
            Az(0,0,0) = (Hy_0 - Hy_in) - (Hx_0 - Hx_jn) - {{ w2 }} * Ez(0,0,0);
        }

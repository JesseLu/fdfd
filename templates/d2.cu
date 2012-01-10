        float u_next, u_prev;
        // Implement the second derivative function.
        if (k == 0) { // First cell must wrap-around.
            u_prev = u(0,0,{{ zzm1 }});
            u_next = u(0,0,1);
        }
        else if (k == {{ zzm1 }}) { // Last cell must all wrap-around.
            u_prev = u(0,0,-1);
            u_next = u(0,0,-{{ zzm1 }});
        }
        else { // Normal update for all other cells.
            u_prev = u(0,0,-1);
            u_next = u(0,0,1);
        }
        u(0,0,0) = u_next - (2 + {{ w2 }}) * u(0,0,0) + u_prev;


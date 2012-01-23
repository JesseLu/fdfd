What is this?
=============

Software package to solve the finite-difference frequency-domain (FDFD)
  electromagnetic problem, using multiple GPUs.


Purpose
=======

To solve the time-harmonic electromagnetic wave equation
  quickly, and on large grids.


To-do
=====

Now
---

1.  Clean everything up and get ready to optimize!
1.  Write unit_tests for subpackages
1.  Start basic documentation with pocoo (?).

Later
-----
*   In bicg.py: check for breakdown condition.
*   In bicg.py: notify user if we were not able to beat term_err.
*   In dist_grid.py: eliminate unnecessary h-d transfers,
        test with (xx, yy, 1) sized grids.

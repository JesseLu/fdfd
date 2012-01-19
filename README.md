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

1.  Verify 3D solve (maxwell_test)
1.  Organize my_physics subpackage.
1.  Write unit_tests for subpackages
1.  Start basic documentation with pocoo (?).

Later
-----
*   In bicg.py: check for breakdown condition.
*   In bicg.py: notify user if we were not able to beat term_err.

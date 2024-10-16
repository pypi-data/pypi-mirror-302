
.. _how-to-time-lapse:

DRS4 Time Lapse Correction
==========================

.. warning::
    The production of this correction coefficients is not yet available in the present release.

Input Data
..........

Events of a run of dark pedestals (acquired with closed camera and random triggers).
These runs are tagged with ``run_type`` DRS4 in the run summary file. By default
minimum number of 20,000 events is required in order to collect enough statistics per
capacitor for the baseline estimation.

How To
......

The baseline file is produced by the tool ..,
which can be run with the simple command:

..    onsite_create_... -r [run_number]

It is possible to write data in a not official data-tree with the option  ``-b [data-tree-root]``.


Output data
...........

Coefficients are written in a *fit*, *fits.gz* or *hdf5* format depending on the option ``--output-format``.

The data model and format are described below :

...

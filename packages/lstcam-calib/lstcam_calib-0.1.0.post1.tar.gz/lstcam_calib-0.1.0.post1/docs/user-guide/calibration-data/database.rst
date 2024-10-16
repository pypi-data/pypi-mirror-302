.. _data_base:

Database
========

The calibration database is hosted by the **TCU Mongo server**. All input/output actions must be
performed by specific onsite tools, through the functions of the :ref:`database <database-input-output>`
module (for more details see :ref:`Change Database Documents <act-on-database>`).

Meta-data are stored in **several collections**, one for each  ``CalibrationType`` :

    .. autoclass:: lstcam_calib.io.database.CalibrationType
        :members:
        :no-index:


Each document contains a set of fields that are common to all ``CalibrationType`` :

    * :class:`~lstcam_calib.io.database.CommonFields`


Then, each ``CalibrationType`` has its own specific fields, collected in the following classes :

    * :class:`~lstcam_calib.io.database.DRS4BaselineFile`
    * :class:`~lstcam_calib.io.database.DRS4TimeSamplingFile`
    * :class:`~lstcam_calib.io.database.CalibrationFile`
    * :class:`~lstcam_calib.io.database.FFactorSystematicsFile`

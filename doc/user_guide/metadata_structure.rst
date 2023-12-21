.. _metadata_structure:

LumiSpy metadata structure
**************************

LumiSpy extends the :external+hyperspy:ref:`HyperSpy metadata structure
<metadata_structure>`
with conventions for metadata specific to its signal types. Refer to the
:external+hyperspy:ref:`HyperSpy metadata documentation <metadata_structure>`
for general metadata fields.

The metadata of any **signal objects** is stored in the `metadata` attribute,
which has a tree structure. By convention, the node labels are capitalized and
the ones for leaves are not capitalized. When a leaf contains a quantity that
is not dimensionless, the units can be given in an extra leaf with the same
label followed by the ``_units`` suffix.

Besides directly accessing the metadata tree structure, e.g.
``s.metadata.Signal.signal_type``, the HyperSpy methods
:external:meth:`set_item() <hyperspy.misc.utils.DictionaryTreeBrowser.set_item>`,
:external:meth:`has_item() <hyperspy.misc.utils.DictionaryTreeBrowser.has_item>` and
:external:meth:`get_item() <hyperspy.misc.utils.DictionaryTreeBrowser.get_item>`
can be used to add to, search for and read from items in the metadata tree,
respectively.

The luminescence specific metadata structure is represented in the following
tree diagram. The default units are given in parentheses. Details about the
leaves can be found in the following sections of this chapter. Note that not
all types of leaves will apply to every type of measurement. For example,
while parallel acquisition with a CCD is characterized by the
``central_wavelength``, a serial acquisition with a PMT will require a
``start_wavelength`` and a ``step_size``.

::

    metadata
    ├── General
    │   └── # see HyperSpy
    ├── Sample
    │   └── # see HyperSpy
    ├── Signal
    │   ├── signal_type
    │   ├── quantity
    │   └── # otherwise see HyperSpy
    └── Acquisition_instrument
        ├── Laser / SEM / TEM
        │   ├── laser_type
        │   ├── model
        │   ├── wavelength (nm)
        │   ├── power (mW)
        │   ├── objective_magnification
        │   ├── Filter
        │   │   ├── filter_type
        │   │   ├── position
        │   │   ├── optical_density
        │   │   ├── cut_on_wavelength (nm)
        │   │   └── cut_off_wavelength (nm)
        │   └── # for SEM/TEM see HyperSpy
        ├── Spectrometer
        │   ├── model
        │   ├── acquisition_mode
        │   ├── entrance_slit_width (mm)
        │   ├── exit_slit_width (mm)
        │   ├── central_wavelength (nm)
        │   ├── start_wavelength (nm)
        │   ├── step_size (nm)
        │   ├── Grating
        │   │   ├── groove_density (grooves/mm)
        │   │   ├── blazing_angle (º)
        │   │   └── blazing_wavelength (nm)
        │   └── Filter
        │       ├── filter_type
        │       ├── position
        │       ├── optical_density
        │       ├── cut_on_wavelength (nm)
        │       └── cut_off_wavelength (nm)
        ├── Detector
        │   ├── detector_type
        │   ├── model
        │   ├── frames
        │   ├── integration_time (s)
        │   ├── saturation_fraction
        │   ├── binning
        │   ├── processing
        │   ├── sensor_roi
        │   └── pixel_size (µm)
        └── Spectral_image
            ├── mode
            ├── drift_correction_periodicity
            └── drift_correction_units (s)


General
=======

See :external+hyperspy:ref:`HyperSpy-Metadata-General <general-metadata>`

Sample
======

See :external+hyperspy:ref:`HyperSpy-Metadata-Sample <sample-metadata>`.

Signal
======

signal_type
    type: string

    String that describes the type of signal. The LumiSpy specific signal classes are
    summarized under :ref:`signal_types`.

quantity
    type: string

    The name of the quantity of the “intensity axis” with the units in round brackets if
    required, for example 'Intensity (counts/s)'.

See :external+hyperspy:ref:`HyperSpy-Metadata-Signal <signal-metadata>`
for additional fields.

Acquisition Instrument
======================

Laser / SEM / TEM
=================

For **SEM** or **TEM** see :external+exspy:ref:`ExSpy-Metadata-SEM/TEM
<source-metadata>`.


Laser
-----

laser_type
    type: string

    The type of laser used, e.g. 'HeCd'.

model
    type: string

    Model of the laser (branding by manufacturer).

wavelength
    type: float

    Emission wavelength of the exciting laser in nm.

power
    type: float

    Measured power of the excitation laser in mW.

magnification
    type: int

    Magnification of the microscope objective used to focus the beam to the
    sample.

.. _filter:

Filter
-------

Information about additional filters entered into the lightpath before the
sample. In case multiple filters are used, they should be numbered
`Filter_1`, etc.

filter_type
    type: string

    Type of filter (e.g. 'optical density', 'short pass', 'long pass',
    'bandpass', 'color').

position
    type: string

    Position in the beam (e.g. 'excitation' vs. 'detection' in case of optical
    excitation).

optical_density
    type: float

    Optical density in case of an intensity filter.

cut_on_wavelength
    type: float

    Cut on wavelength in nm in case of a long-pass or bandpass filter.

cut_off_wavelength
    type: float

    Cut off wavelength in nm in case of a short-pass or bandpass filter.

Spectrometer
============

Contains information about the spectrometer, configuration and grating used
for the measurement. In case multiple spectrometers are connected in series,
they should be numbered `Spectrometer_1`, etc.

model
    type: string

    Model of the spectrometer (branding by manufacturer).

acquisition_mode
    type: string

    Acquisition mode (e.g. 'Parallel dispersive', versus 'Serial dispersive').

entrance_slit_width
    type: float

    Width of the entrance slit in mm.

exit_slit_width
    type: float

    Width of the exit slit (serial acquisition) in mm.

central_wavelength
    type: float

    Central wavelength during acquisition (parallel acquisition).
    
start_wavelength
    type: float

    Start wavelength in nm (serial acquisition).

step_size
    type: float

    Step size in nm (serial acquisition).

Grating
-------

Information of the dispersion grating employed in the measurement.

groove_density
    type: int

    Density of lines on the grating in grooves/mm.

blazing_angle
    type: int

    Angle in degree (º) that the grating is blazed at.

blazing_wavelength
    type: int

    Wavelength that the grating blaze is optimized for in nm.

Filter
-------

Information about additional filters entered into the lightpath after the
sample. In case multiple filters are used, they should be numbered
`Filter_1`, etc. See :ref:`filter` above for details on items that
may potentially be included.

Detector
========

Contains information about the detector used to acquire the signal. Contained
leaves will differ depending on the type of detector.

detector_type
    type: string

    The type of detector used to acquire the signal (CCD, PMT, StreakCamera, 
    TCSPD).

model
    type: string

    The model of the used detector.

frames
    type: int

    Number of frames that are summed to yield the total integration time.

integration_time (s)
    type: float

    Time over which the signal is integrated. In case multiple frames are
    summed, it is the total exposure time. In case of serial acquisition, it is
    the dwell time per data point.

saturation_fraction
    type: float

    Fraction of the signal intensity compared with the saturation threshold of
    the CCD.

binning
    type: tuple of int

    A tuple that describes the binning of a parallel detector such a CCD on
    readout in x and y directions.

processing
    type: string

    Information about automatic processing performed on the data, e.g. 'dark
    subtracted'.

sensor_roi
    type: tuple of int

    Tuple of length 2 or 4 that specifies range of pixels on a detector that
    are read out: (offset x, offset y, size x, size y) for a 2D array detector
    and (offset, size) for a 1D line detector.

pixel_size
    type: float or tuple of float

    Size of a pixel in µm. Tuple of length 2 (width, height), when the pixel is
    not square.


Spectral_image
==============

Contains information about mapping parameters, such as step size, drift
correction, etc.

mode
    type: string

    Mode of the spectrum image acquisition such as 'Map' or 'Linescan'.

drift_correction_periodicity
    type: int/float

    Periodicity of the drift correction in specified units (standard s).

drift_correction_units
    type: string

    Units of the drift correction such as 's', 'px', 'rows'.

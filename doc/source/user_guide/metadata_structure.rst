.. _metadata_structure:

LumiSpy metadata structure
**************************

LumiSpy extends the `HyperSpy metadata structure
<https://hyperspy.org/hyperspy-doc/current/user_guide/metadata_structure.html>`_
with conventions for metadata specific to its signal types. Refer to `HyperSpy
<https://hyperspy.org/hyperspy-doc/current/user_guide/metadata_structure.html>`_
for general metadata fields.

The metadata of any **signal objects** is stored in the `metadata` attribute,
which has a tree structure. By convention, the node labels are capitalized and
the ones for leaves are not capitalized. When a leaf contains a quantity that
is not dimensionless, the units can be given in an extra leaf with the same
label followed by the ``_units`` suffix.

The luminescence specific metadata structure is represented in the following
tree diagram. The default units are given in parentheses. Details about the
leaves can be found in the following sections of this chapter. Note that not
all types of leaves will apply to every type of measurements. For example,
while parallel acquisition with a CCD is characterized by the
``central_wavelength``, a serial acquisition with a PMT will require a
``start_wavelength`` and a ``step_size``.

::

    └── Acquisition_instrument
        ├── Spectrometer
        │   ├── model_name
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
        │   ├── model_name
        │   ├── frames
        │   ├── integration_time (s)
        │   ├── saturation_fraction
        │   ├── binning
        │   ├── processing
        │   ├── sensor_roi
        │   └── pixel_width (µm)
        └── Spectral_image
            ├── mode
            ├── step_size
            ├── step_size_units (nm)
            ├── drift_correction_periodicity
            └── drift_correction_units (s)

    
::


Spectrometer
============

Contains information about the spectrometer, configuration and grating used
for the measurement. In case multiple spectrometers are connected in series,
they should be numbered `Spectrometer_1`, etc.

model_name
    type: string

    Model of the spectrometer.

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

Information about additional filters entered into the lightpath. In case
multiple filters are used, they should be numbered `Filter_1`, etc.

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

Detector
========

Contains information about the detector used to acquire the signal. Contained
leaves will differ depending on the type of detector.

detector_type
    type: string

    The type of detector used to acquire the signal (CCD, PMT, StreakCamera, 
    TCSPD)

model_name
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

    Tuple that specifies range of pixels on a detector that are read out.

pixel_width
    type: float

    Diameter of a pixel in µm.


Spectral_image
==============

Contains information about mapping parameters, such as step size, drift
correction, etc.

mode
    type: string

    Mode of the spectrum image acquisition such as 'Map' or 'Linescan'.

step_size
    type: float

    Distance between subsequent pixels in the spectral image.

step_size_units
    type: string

    Units of the step size (standard 'nm').

drift_correction_periodicity
    type: int/float

    Periodicity of the drift correction in specified units (standard s).

drift_correction_units
    type: string

    Units of the drift correction such as 's', 'px', 'rows'.

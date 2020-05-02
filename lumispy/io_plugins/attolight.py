# -*- coding: utf-8 -*-
# Copyright 2019 The LumiSpy developers
#
# This file is part of LumiSpy.
#
# LumiSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LumiSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LumiSpy.  If not, see <http://www.gnu.org/licenses/>.
import glob
import os
import numpy as np
from hyperspy._signals.signal2d import Signal2D
from lumispy.signals.cl_sem_spectrum import CLSEMSpectrum

# Plugin characteristics
# ----------------------
format_name = 'AttolightSEM_HYPCard'
description = 'Reads CL data from the Attolight SEM system'
version = '0.1'
full_support = False
# Recognised file extension
file_extensions = ['bin', 'BIN']
default_extension = 0
# Writing capabilities
writes = False

# Attolight system specific parameters
# ------------------------------------
attolight_systems = {
    'cambridge_uk_attolight': {
        'channels': 1024,
        'cal_factor_x_axis': 131072,
        'metadata_file_name': 'MicroscopeStatus.txt',
        'grating_corrfactors': {
            150: 2.73E-04,
            600: 6.693659836087227e-05,
        }
    }
}


def file_reader(filename, *args, **kwds):
    """Load data into CLSEMSpectrum lumispy object.
    Parameters
    ----------
    filename : str, None
        The HYPCard.bin filepath for the file to be loaded, created by AttoLight software.
        Please, state the directory.
        If None, a pop-up window will be loaded.
    lazy : bool
        If True the file will be opened lazily, i.e. without actually reading
        the data from the disk until required. Allows datasets much larger than
        available memory to be loaded.
    metadata_file_name: str
        By default, AttoLight software names it 'MicroscopeStatus.txt'.
        Otherwise, specify.
    attolight_acquisition_system : str
        Specify which acquisition system the HYPCard was taken with, from the
        attolight_systems dictionary file. By default, it assumes it is
        the Cambridge Attolight SEM system.
    Returns
    -------
    s : Signal
        A CLSEMSpectrum lumispy object containing loaded data.
    """
    # Read the kwds, else return their default
    lazy = kwds.pop('lazy', False)
    attolight_acquisition_system = kwds.pop('attolight_acquisition_system', 'cambridge_uk_attolight')
    metadata_file_name = kwds.pop('metadata_file_name',
                                  attolight_systems[attolight_acquisition_system]['metadata_file_name'])

    def _get_metadata(filename, md_file_name, attolight_acquisition_system):
        """Import the metadata from the MicroscopeStatus.txt file.
        Returns binning, nx, ny, FOV, grating and central_wavelength.
        Parameters
        ----------
        filename : str
            The absolute folder path where the md_file_name exists.
        """
        path = os.path.join(filename, md_file_name)
        with open(path, encoding='windows-1252') as status:
            for line in status:
                if 'Horizontal Binning:' in line:
                    binning = int(line[line.find(':') + 1:-1])  # binning = binning status
                if 'Resolution_X' in line:
                    nx = int(line[line.find(':') + 1:-7])
                    # nx = pixel in x-direction
                if 'Resolution_Y' in line:
                    ny = int(line[line.find(':') + 1:-7])
                    # ny = pixel in y-direction
                if 'Real Magnification' in line:
                    FOV = float(line[line.find(':') + 1:-1])
                if 'Grating - Groove Density:' in line:
                    grating = float(line[line.find(':') + 1:-6])
                if 'Central wavelength:' in line:
                    central_wavelength_nm = float(line[line.find(':') + 1:-4])
                if 'Channels:' in line:
                    total_channels = int(line[line.find(':') + 1:-1])
                if 'Signal Amplification:' in line:
                    amplification = int(line[line.find(':x') + 2:-1])
                if 'Readout Rate (horizontal pixel shift):' in line:
                    readout_rate_khz = int(line[line.find(':') + 1:-4])

                if 'Exposure Time:' in line:
                    exposure_time_ccd_s = float(line[line.find(':') + 1:-3])
                if 'HYP Dwelltime:' in line:
                    dwell_time_scan_s = float(line[line.find(':') + 1:-4]) / 1000
                if 'Beam Energy:' in line:
                    beam_acc_voltage_kv = float(line[line.find(':') + 1:-3]) / 1000
                if 'Gun Lens:' in line:
                    gun_lens_amps = float(line[line.find(':') + 1:-3])
                if 'Objective Lens:' in line:
                    obj_lens_amps = float(line[line.find(':') + 1:-3])
                if 'Aperture:' in line:
                    aperture_um = float(line[line.find(':') + 1:-4])
                if 'Aperture Chamber Pressure:' in line:
                    chamber_pressure_torr = float(line[line.find(':') + 1:-6])
                if 'Real Magnification:' in line:
                    real_magnification = float(line[line.find(':') + 1:-3])

        # Correct channels to the actual value, accounting for binning. Get
        # channels on the detector used (if channels not defined, then assume
        # its 1024)
        try:
            total_channels
        except:
            total_channels = attolight_systems[attolight_acquisition_system]['channels']
        channels = total_channels // binning

        # Return metadata
        return binning, nx, ny, FOV, grating, central_wavelength_nm, channels, amplification, readout_rate_khz, exposure_time_ccd_s, dwell_time_scan_s, beam_acc_voltage_kv, gun_lens_amps, obj_lens_amps, aperture_um, chamber_pressure_torr, real_magnification

    def _store_metadata(cl_object, hypcard_folder, md_file_name,
                       attolight_acquisition_system):
        """
        TO BE ADDED
        Store metadata in the CLSpectrum object metadata property. Stores
        binning, nx, ny, FOV, grating and central_wavelength.
        Parameters
        ----------
        cl_object: CLSpectrum object
            The CLSpectrum object where to save the metadata.
        hypcard_folder : str
            The absolute folder path where the metadata_file_name exists.
        """
        # Get metadata
        binning, nx, ny, FOV, grating, central_wavelength_nm, channels, amplification, readout_rate_khz, exposure_time_ccd_s, dwell_time_scan_s, beam_acc_voltage_kv, gun_lens_amps, obj_lens_amps, aperture_um, chamber_pressure_torr, real_magnification = _get_metadata(
            hypcard_folder, md_file_name, attolight_acquisition_system)

        # Store metadata
        cl_object.metadata.set_item("Acquisition_instrument.Spectrometer.grating",
                                    grating)
        cl_object.metadata.set_item("Acquisition_instrument.Spectrometer.central_wavelength_nm",
                                    central_wavelength_nm)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.resolution_x",
                                    nx)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.resolution_y",
                                    ny)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.FOV", FOV)
        cl_object.metadata.set_item("Acquisition_instrument.CCD.binning",
                                    binning)
        cl_object.metadata.set_item("Acquisition_instrument.CCD.channels",
                                    channels)
        cl_object.metadata.set_item("Acquisition_instrument.acquisition_system",
                                    attolight_acquisition_system)
        cl_object.metadata.set_item("Acquisition_instrument.CCD.amplification", amplification)
        cl_object.metadata.set_item("Acquisition_instrument.CCD.readout_rate_khz", readout_rate_khz)
        cl_object.metadata.set_item("Acquisition_instrument.CCD.exposure_time_s", exposure_time_ccd_s)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.dwell_time_scan_s", dwell_time_scan_s)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.beam_acc_voltage_kv", beam_acc_voltage_kv)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.gun_lens_amps", gun_lens_amps)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.obj_lens_amps", obj_lens_amps)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.aperture_um", aperture_um)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.chamber_pressure_torr", chamber_pressure_torr)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.real_magnification", real_magnification)
        cl_object.metadata.set_item("General.folder_path", hypcard_folder)

        return cl_object

    def _calibrate_signal_axis_wavelength(cl_object):
        """
        Based on the Attolight software export function. Need to be automatised.
        Two calibrated sets show the trend:
        #Centre at 650 nm:
            spec_start= 377.436, spec_end = 925.122
        #Centre at 750:
            spec_start= 478.2, spec_end = 1024.2472
        Returns
        ----------
        spectra_offset_array: []
            Array containing the spectrum energy axis start and end points in
            nm (from the MeanSpectrum file), such as [spec_start, spec_end]
        """
        # Get relevant parameters from metadata
        central_wavelength = cl_object.metadata.Acquisition_instrument.Spectrometer.central_wavelength_nm

        # Estimate start and end wavelengths
        spectra_offset_array = [central_wavelength - 273, central_wavelength + 273]

        # Apply calibration
        dx = cl_object.axes_manager.signal_axes[0]
        dx.name = 'Wavelength'
        dx.scale = (spectra_offset_array[1] - spectra_offset_array[0]) \
                   / cl_object.axes_manager.signal_size
        dx.offset = spectra_offset_array[0]
        dx.units = '$nm$'

        return cl_object

    def _calibrate_navigation_axis(cl_object):
        # Edit the navigation axes
        x = cl_object.axes_manager.navigation_axes[0]
        y = cl_object.axes_manager.navigation_axes[1]

        # Get relevant parameters from metadata and acquisition_systems
        # parameters
        attolight_acquisition_system \
            = cl_object.metadata.Acquisition_instrument.acquisition_system
        cal_factor_x_axis \
            = attolight_systems[attolight_acquisition_system]['cal_factor_x_axis']
        FOV = cl_object.metadata.Acquisition_instrument.SEM.FOV
        nx = cl_object.metadata.Acquisition_instrument.SEM.resolution_x

        # Get the calibrated scanning axis scale from the acquisition_systems
        # dictionary
        calax = cal_factor_x_axis / (FOV * nx)
        x.name = 'x'
        x.scale = calax * 1000
        # changes micrometer to nm, value for the size of 1 pixel
        x.units = 'nm'
        y.name = 'y'
        y.scale = calax * 1000
        # changes micrometer to nm, value for the size of 1 pixel
        y.units = 'nm'

        return cl_object

    def _save_background_metadata(cl_object, hypcard_folder, background_file_name='Background*.txt'):
        """
        Based on the Attolight background savefunction.
        If background is found in the folder, it saves background as in the metadata.
        """
        # Get the absolute path
        path = os.path.join(hypcard_folder, background_file_name)

        # Try to load the file, if it exists.
        try:
            # Find the exact filename, using the * wildcard
            path = glob.glob(path)[0]
            # Load the file as a numpy array
            bkg = np.loadtxt(path)
            # The bkg file contains [wavelength, background]
            cl_object.metadata.set_item("Signal.background", bkg)
            return cl_object
        except:
            cl_object.metadata.set_item("Signal.background", None)
            return cl_object


    #################################

    # Loading function starts here

    # Check if a path has been given
    if filename is None:
        from hyperspy.signal_tools import Load
        from hyperspy.ui_registry import get_gui
        load_ui = Load()
        get_gui(load_ui, toolkey="hyperspy.load")
        if load_ui.filename:
            filename = load_ui.filename
            lazy = load_ui.lazy
        if filename is None:
            raise ValueError("No file provided to reader")

    # Import folder name
    hypcard_folder = os.path.split(os.path.abspath(filename))[0]

    # Import metadata
    metadata_file_name \
        = attolight_systems[attolight_acquisition_system]['metadata_file_name']

    binning, nx, ny, FOV, grating, central_wavelength_nm, channels, amplification, readout_rate_khz, \
    exposure_time_ccd_s, dwell_time_scan_s, beam_acc_voltage_kv, gun_lens_amps, obj_lens_amps, aperture_um,\
    chamber_pressure_torr, real_magnification = \
        _get_metadata(hypcard_folder, metadata_file_name, attolight_acquisition_system)

    # Load file
    with open(filename, 'rb') as f:
        data = np.fromfile(f, dtype=[('bar', '<i4')], count=channels * nx * ny)
        array = np.reshape(data, [channels, nx, ny], order='F')

    # Swap x-y axes to get the right xy orientation
    sarray = np.swapaxes(array, 1, 2)

    # Make the CLSEMSpectrum object
    # Load the transposed data
    s = Signal2D(sarray).T
    s.change_dtype('float')
    s = CLSEMSpectrum(s)

    # Add all parameters as metadata
    _store_metadata(s, hypcard_folder, metadata_file_name, attolight_acquisition_system)

    # Add name as metadata
    experiment_name = os.path.basename(hypcard_folder)
    if attolight_acquisition_system == 'cambridge_attolight':
        # CAUTION: Specifically delimeted by Attolight default naming system
        if len(experiment_name) > 37:
            name = experiment_name[:-37]
        else:
            name = experiment_name
    else:
        name = experiment_name
    s.metadata.General.title = name

    # Calibrate navigation axis
    _calibrate_navigation_axis(s)

    # Calibrate signal axis
    _calibrate_signal_axis_wavelength(s)

    # Save background file if exisent (after calibrating signal axis)
    _save_background_metadata(s, hypcard_folder,)

    return s


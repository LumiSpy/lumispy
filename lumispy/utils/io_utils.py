# -*- coding: utf-8 -*-
# Copyright 2017-2019 The LumiSpy developers
#
# This file is part of lumispy.
#
# lumispy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lumispy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lumispy.  If not, see <http://www.gnu.org/licenses/>.

# a lot of stuff depends on this, so we have to create it first

import glob
import logging
import os
import warnings
import numpy as np

#from hyperspy.io import load as hyperspyload
#from hyperspy.io import load_with_reader

from hyperspy.signals import Signal2D
from lumispy.signals.cl_sem import CLSEMSpectrum

from .acquisition_systems import acquisition_systems




def load_hypcard(hypcard_file, lazy = False, acquisition_system = 'cambridge_attolight'):
    """Load data into pyxem objects.
    Parameters
    ----------
    hypcard_file : str
        The HYPCard.bin file for the file to be loaded, created by AttoLight software. Please, state the directory.
    lazy : bool
        If True the file will be opened lazily, i.e. without actually reading
        the data from the disk until required. Allows datasets much larger than
        available memory to be loaded.
    metadata_file_name: str
        By default, AttoLight software names it 'MicroscopeStatus.txt'. Otherwise, specify.
    acquisition_system : str
        Specify which acquisition system the HYPCard was taken with, from the acquisition_systems.py dictionary file. By default, it assumes it is the Cambridge Attolight SEM system.
    Returns
    -------
    s : Signal
        A pyxem Signal object containing loaded data.
    """
    def get_metadata(hypcard_folder, metadata_file_name):
        """Import the metadata from the MicroscopeStatus.txt file.
        Returns binning, nx, ny, FOV, grating and central_wavelength.
        Parameters
        ----------
        hypcard_folder : str
            The absolute folder path where the metadata_file_name exists.
        """
        path = hypcard_folder + '\\'+ metadata_file_name
        with open(path, encoding='windows-1252' ) as status:
            for line in status:
                if 'Horizontal Binning' in line:
                    binning = int(line[-2])        #binning = binning status
                if 'Resolution_X' in line:
                    nx = int(line[line.find(':')+1:-8])         #nx = pixel in x-direction
                if 'Resolution_Y' in line:
                    ny = int(line[line.find(':')+1:-8])         #ny = pixel in y-direction
                if 'Real Magnification' in line:
                     FOV = float(line[line.find(':')+1:-2])
                if 'Grating - Groove Density:' in line:
                    grating = float(line[line.find(':')+1:-7])
                if 'Central wavelength:' in line:
                    central_wavelength = float(line[line.find(':')+1:-5])
                if 'Channels:' in line:
                    total_channels = int(line[line.find(':'), -2])

        #Correct channels to the actual value, accounting for binning. Get channels on the detector used (if channels not defined, then assume its 1024)
        try:
            total_channels
        except:
            total_channels = acquisition_systems[acquisition_system]['channels']
        channels =  total_channels//binning

        #Return metadata
        return binning, nx, ny, FOV, grating, central_wavelength, channels

    def store_metadata(cl_object, hypcard_folder, metadata_file_name, acquisition_system):
        """
        TO BE ADDED
        Store metadata in the CLSpectrum object metadata property. Stores binning, nx, ny, FOV, grating and central_wavelength.
        Parameters
        ----------
        cl_object: CLSpectrum object
            The CLSpectrum object where to save the metadata.
        hypcard_folder : str
            The absolute folder path where the metadata_file_name exists.
        """
        #Get metadata
        binning, nx, ny, FOV, grating, central_wavelength, channels = get_metadata(hypcard_folder, metadata_file_name)

        #Store metadata
        cl_object.metadata.set_item("Acquisition_instrument.SEM.Spectrometer.grating", grating)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.Spectrometer.central_wavelength", central_wavelength)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.resolution_x", nx)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.resolution_y", ny)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.FOV", FOV)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.CCD.binning", binning)
        cl_object.metadata.set_item("Acquisition_instrument.SEM.CCD.channels", channels)
        cl_object.metadata.set_item("Acquisition_instrument.acquisition_system", acquisition_system)

        return cl_object

    def calibrate_signal_axis_wavelength(cl_object):
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
            Array containing the spectrum energy axis start and end points in nm (from the MeanSpectrum file), such as [spec_start, spec_end]
        """
        #Get relevant parameters from metadata
        central_wavelength = cl_object.metadata.Acquisition_instrument.SEM.Spectrometer.central_wavelength

        #Estimate start and end wavelengths
        spectra_offset_array = [central_wavelength-273, central_wavelength+273]

        #Apply calibration
        dx = cl_object.axes_manager.signal_axes[0]
        dx.name = 'Wavelength'
        dx.scale = (spectra_offset_array[1] - spectra_offset_array[0])/cl_object.axes_manager.signal_size
        dx.offset = spectra_offset_array[0]
        dx.units = '$nm$'

        return cl_object

    def calibrate_navigation_axis(cl_object):
        #Edit the navigation axes
        x = cl_object.axes_manager.navigation_axes[0]
        y = cl_object.axes_manager.navigation_axes[1]

        #Get relevant parameters from metadata and acquisition_systems parameters
        acquisition_system = cl_object.metadata.Acquisition_instrument.acquisition_system
        cal_factor_x_axis = acquisition_systems[acquisition_system]['cal_factor_x_axis']
        FOV = cl_object.metadata.Acquisition_instrument.SEM.FOV
        nx = cl_object.metadata.Acquisition_instrument.SEM.resolution_x

        #Get the calibrated scanning axis scale from the acquisition_systems dictionary
        calax = cal_factor_x_axis/(FOV*nx)
        x.name = 'x'
        x.scale = calax * 1000
        #changes micrometer to nm, value for the size of 1 pixel
        x.units = 'nm'
        y.name = 'y'
        y.scale = calax * 1000
        #changes micrometer to nm, value for the size of 1 pixel
        y.units = 'nm'

        return cl_object

    #################################

    #Loading function starts here
    #Import folder name
    hypcard_folder = os.path.split(os.path.abspath(hypcard_file))[0]

    #Import metadata
    metadata_file_name = acquisition_systems[acquisition_system]['metadata_file_name']
    binning, nx, ny, FOV, grating, central_wavelength, channels = get_metadata(hypcard_folder, metadata_file_name)


    #Load file
    with open(hypcard_file, 'rb') as f:
        data = np.fromfile(f, dtype= [('bar', '<i4')], count= channels*nx*ny)
        array = np.reshape(data, [channels, nx, ny], order='F')

    #Swap x-y axes to get the right xy orientation
    sarray = np.swapaxes(array, 1,2)

    ##Make the CLSEMSpectrum object
    #Load the transposed data
    s = Signal2D(sarray).T
    s.change_dtype('float')
    s = CLSEMSpectrum(s)

    #Add all parameters as metadata
    store_metadata(s, hypcard_folder, metadata_file_name, acquisition_system)

    ##Add name as metadata
    if acquisition_system == 'cambridge_attolight':
        #Import file name
        experiment_name = os.path.split(hypcard_folder)[1]
        #CAUTION: Specifically delimeted by Attolight default naming system
        try:
            name = experiment_name[:-37]
        except:
            name = experiment_name
        s.metadata.General.title = name

    #Calibrate navigation axis
    calibrate_navigation_axis(s)

    #Calibrate signal axis
    calibrate_signal_axis_wavelength(s)

    return(s)

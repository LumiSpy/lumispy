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

"""Signal class for Luminescence data (BaseSignal class).
"""


class CommonLumi:
    """General Luminescence signal class (dimensionless).
    ----------
    """

    def crop_edges(self, crop_px):
        """
        Crop the amount of pixels from the four edges of the scanning region, from out the edges inwards.

        Parameters
        ---------------
        crop_px : int
            Amount of pixels to be cropped on each side individually.

        Returns
        ---------------
        signal_cropped : CommonLuminescence
            A smaller cropped CL signal object. If inplace is True, the original object is modified and no LumiSpectrum is returned.
        """

        width = self.axes_manager.shape[0]
        height = self.axes_manager.shape[1]

        if crop_px * 2 > width or crop_px * 2 > height:
            raise ValueError("The pixels to be cropped cannot be larger than half the width or the length!")
        else:
            signal_cropped = self.inav[crop_px + 1: width - crop_px + 1, crop_px + 1: height - crop_px + 1]

        # Store transformation in metadata (or update the value if already previously transformed)

        try:
            px_already_cropped = signal_cropped.metadata.Signal.cropped_edges
            signal_cropped.metadata.Signal.cropped_edges = px_already_cropped + crop_px
        except:
            signal_cropped.metadata.set_item("Signal.cropped_edges", crop_px)

        return signal_cropped

    def background_subtraction(self, background=None, inplace=False):
        """
        Subtract the background to the signal in each pixel.
        If background is manually input of function as argument, it will be subtracted if it matches the x axis wavelenght values.
        Otherwise, if no background is passed, it will check on the metadata.
        If background is in metadata, it subtracts it without need to manually input background (background is automatically saved upon load_hyp() if the bakground file is found in the same folder as the data).
        Otherwise it raises an Error.

        Parameters
        ---------------
        background : numpy.array[wavelength, bkg]
            OPTIONAL: Background array with two columns: [wavelength, bkg]. Length of array must match signal_axes size.

        inplace : boolean
            If False, it returns a new object with the transformation. If True, the original object is transformed, returning no object.

        Returns
        ---------------
        signal_cropped : LumiSpectrum
            A smaller cropped CL signal object. If inplace is True, the original object is modified and no LumiSpectrum is returned.
        """

        def subtract_self(signal, bkg):
            """
            Dummy function to be used in self.map below.
            """
            return signal - bkg

        background_metadata = self.metadata.Signal.background
        if background is not None:
            if (background[0]).all() == (self.axes_manager.signal_axes[0].axis).all():
                bkg = background[1]

            else:
                raise ValueError('The background x axis provided as external argument is does not match the signal '
                                 'wavelength x axis values.')
        else:
            if background_metadata is not None:
                if (background_metadata[0]).all() == (self.axes_manager.signal_axes[0].axis).all():
                    bkg = background_metadata[1]

                else:
                    raise ValueError('The background x axis wavelength values from the signal.background axis do not '
                                     'match the signal wavelength x axis values.')
            else:
                raise ValueError('No background defined on the Signal.background metadata NOR as an input of this function.')

        if not inplace:
            self_subtracted = self.map(subtract_self, bkg=bkg, inplace=False)
            self_subtracted.metadata.set_item("Signal.background_subtracted", True)
            return self_subtracted
        else:
            self.metadata.set_item("Signal.background_subtracted", True)
            return self.map(subtract_self, bkg=bkg, inplace=True)

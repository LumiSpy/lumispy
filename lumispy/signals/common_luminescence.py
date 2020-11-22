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
            signal_cropped.metadata.Signal.cropped_edges += crop_px
        except AttributeError:
            signal_cropped.metadata.set_item("Signal.cropped_edges", crop_px)

        return signal_cropped

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

acquisition_systems = {
    'cambridge_attolight' : {
        'channels' : 1024,
        'cal_factor_x_axis' : 131072,
        'metadata_file_name' :'MicroscopeStatus.txt',
        'grating_corrfactors' : {
            150 : 2.73E-04,
            600 : 6.693659836087227e-05,
        }
    }
}

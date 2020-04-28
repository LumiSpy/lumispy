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


import logging

from hyperspy.io import load as hyperspyload

import numpy as np

from natsort import natsorted

from .signals.luminescence_spectrum import LumiSpectrum
from .signals.cl_spectrum import CLSpectrum
from .signals.cl_sem_spectrum import CLSEMSpectrum
from .signals.cl_stem_spectrum import CLSTEMSpectrum
from .signals.pl_spectrum import PLSpectrum
from .signals.el_spectrum import ELSpectrum
from .signals.luminescence_transient import LumiTransient

from .signals.luminescence_spectrum import LazyLumiSpectrum
from .signals.cl_spectrum import LazyCLSpectrum
from .signals.cl_sem_spectrum import LazyCLSEMSpectrum
from .signals.cl_stem_spectrum import LazyCLSTEMSpectrum
from .signals.pl_spectrum import LazyPLSpectrum
from .signals.el_spectrum import LazyELSpectrum
from .signals.luminescence_transient import LazyLumiTransient

from .io import load

from . import release_info

__version__ = release_info.version
__author__ = release_info.author
__copyright__ = release_info.copyright
__credits__ = release_info.credits
__license__ = release_info.license
__maintainer__ = release_info.maintainer
__email__ = release_info.email
__status__ = release_info.status

_logger = logging.getLogger(__name__)


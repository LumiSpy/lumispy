# -*- coding: utf-8 -*-
# Copyright 2019-2021 The LumiSpy developers
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

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from scipy.interpolate import interp1d


def plot_linescan(s, logscale=True, colorbar=True, invert=False, cmap='jet', \
            filename=None, vmin=1, vmax=None, interpolate=None, contour=False, \
            clevels=15, figsize=None, vline=None, vlinecolor='black', \
            hline=None, hlinecolor='black', linewidth=1, fontsize=18, \
            fontfamily='DejaVu Sans'):
    """Plot spectral linescan as colormap on screen and optionally write to
    file.
    
    Parameters
    ----------
    s : LumiSpectrum object
        Works only for exactly one navigation dimension.
    logscale : boolean, optional
        If `True` (default), plot on a logarithmic intensity scale.
    colorbar: boolean, optional
        If `True` (default), add colorbar to the right.
    invert: boolean, optional
        Invert navigation direction. Default `False`.
    cmap : string, optional
        Color map, e.g. 'jet' (default), 'inferno', ...
    filename : string, optional
        If not `None, write to an image file with this filename. The format is
        determined by the extension, e.g. 'outfile.png'.
    vmin : float, optional
        Minimum `z` (intensity) value. Default 1.
    vmax : float, optional
        If `None` (default), automatically determine the maximum value of the
        `z` (intensity) scale from dataset. Otherwise take given value.
    interpolate : int
        If not `None` (default), interpolate to finer mesh with given number of
        interpolation points both for x and y direction.
    contour : boolean, optional
        Plot additional contour lines (default `False`)
    clevels : int
        Number of contour levels (default 15)
    figsize : tuple of floats
        If `None` (default) use standard figure size, otherwise use size
        defined by the given tuple.
    vline : float or array of floats
        Position(s) along signal axis at which to plot a vertical line.
        Default `None` corresponds to no lines.
    vlinecolor : string
        Color of vertical lines (default 'black')
    hline : float or array of floats
        Position(s) along navigation axis at which to plot a vertical line.
        Default `None` corresponds to no lines.
    hlinecolor : string
        Color of vertical lines (default 'black')
    linewidth : int, optional
        Scaling factor for tick linewidth and horizontal/vertical lines.
    fontsize : int
        Font size of axes labels (default 18)
    fontfamily : 
        Font type of axes labels (default 'DejaVu Sans')
	
    Returns
    -------
    Figure and axes objects.
    
    """
    if s.axes_manager.navigation_dimension != 1 or s.axes_manager.signal_dimension != 1:
        raise AttributeError('Wrong number of signal or navigation dimensions, '
                             'this signal is not a linescan.')
    # Initialize figure
    if figsize is None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figsize)
    plt.matplotlib.rcParams.update({'font.size': fontsize, 'font.weight': 'normal', 'font.family': fontfamily})
    ax = fig.add_subplot(111)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.tick_params(direction='out', pad=5, width=1.5*linewidth, length=5*linewidth)
    ax.tick_params(which='minor', direction='out', width=1.2*linewidth, length=3*linewidth)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1*linewidth)
    # Setup data
    x = s.axes_manager[1].axis
    y = s.axes_manager[0].axis
    z = s.data.clip(1)
    # Interpolate data to finer mesh
    if interpolate is not None:
        x2 = np.linspace(np.min(x), np.max(x), 150)
        y2 = np.linspace(np.min(y), np.max(y), 100)
        f = interpolate.interp2d(x, y, z, kind='cubic')
        z = f(x2, y2)
        x, y = x2, y2
    # Set intensity range
    if vmax is None and vmin is None:
        mi, ma = np.floor(np.nanmin(z)), np.ceil(np.nanmax(z))    
    elif vmin is None:
        mi, ma = np.floor(np.nanmin(z)), vmax
    else:
        mi, ma = vmin, vmax
    # invert navigation axis
    if invert:
        z = z[::-1,:]
    # set axes labels
    if isinstance(s.axes_manager[1].name, str) and isinstance(s.axes_manager[1].units, str):
        plt.xlabel(s.axes_manager[1].name + ' (' + s.axes_manager[1].units + ')')
    elif isinstance(s.axes_manager[1].name, str):
        plt.xlabel(s.axes_manager[1].name + ' (arb. units)')
    elif isinstance(s.axes_manager[1].units, str):
        plt.xlabel('Signal (' + s.axes_manager[1].units + ')')
    else:
        plt.xlabel('Signal (arb. units)')
    if isinstance(s.axes_manager[0].name, str) and isinstance(s.axes_manager[0].units, str):
        plt.ylabel(s.axes_manager[0].name + ' (' + s.axes_manager[0].units + ')')
    elif isinstance(s.axes_manager[0].name, str):
        plt.ylabel(s.axes_manager[0].name + ' (arb. units)')
    elif isinstance(s.axes_manager[0].units, str):
        plt.ylabel('Position (' + s.axes_manager[0].units + ')')
    else:
        plt.ylabel('Position (arb. units)')
    # plot
    if logscale:
        im = plt.pcolormesh(x,y,z, cmap=cmap, norm=plt.matplotlib.colors.LogNorm(vmin=vmin,vmax=ma),
                            linewidth=0, rasterized=True, shading='auto')
    else: 
        im = plt.pcolormesh(x,y,z, cmap=cmap, vmax=ma, linewidth=0,
                            rasterized=True, shading='auto')
    im.set_edgecolor('face')
    plt.ylim(min(y),max(y))
    plt.xlim(min(x),max(x))
    # plot colorbar
    if colorbar:
        plt.colorbar()
    # make sure that labels are not cut off
    fig.tight_layout()
    # add contour lines
    if contour:
        if logscale:
            levels = np.geomspace(mi, ma, clevels)
            plt.contour(x,y,z, levels=levels, linewidths=0.5, colors=[(0,0,0,0.5)])            
        else:
            levels = np.linspace(mi, ma, clevels)
            plt.contour(x,y,z, levels=levels, linewidths=0.5, colors=[(0,0,0,0.5)])
    # add vertical lines (array for multiple)
    if vline is not None:
        if np.isscalar(vline): vline = [vline]
        for i in vline:
            plt.axvline(i, linewidth=1.5*linewidth, color=vlinecolor)
    # add horizontal lines (array for multiple)
    if hline is not None:
        if np.isscalar(hline): hline = [hline]
        for i in hline:
            plt.axhline(i, linewidth=1.5*linewidth, color=hlinecolor)
    # save figure to file
    if filename is not None:
        extension = split('\.',filename)[-1]
        plt.savefig(filename, pad_inches=0.5, format=extension)
    return fig, ax

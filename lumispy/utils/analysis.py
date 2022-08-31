import hyperspy.drawing.widgets
import hyperspy.roi
import numpy as np


class SpanMap:
    """
    A class for interactively seeing how the intensity of a hyperspectral map vary over different ranges.
    
    Different channels correspond to different colours in the map.
    
    Each channel slices the hyperspectral data over its signal range.
    
    Each channel's range is interactively set by scanning over the sum of hyperspectra over all positions.
    
    Either use this class directly or use the convenience function `plot_auto_peakmap`.
    
    Arguments
    ---------
    hs: hyperspy.signals.Signal1D 
        hyperspectra to analyse. Is intended to be of the form <BaseSignal x, y| sig>
    channels: *SpanChannel
        a number of SpanChannels to slice up and view `hs` via.
        
        
    Attributes
    ----------
    nav: hyperspy.signals.Signal1D
        'navigator' used to interactively set the range of each channel. Will be of the form `<BaseSignal | sig>`
    peakmap: hyperspy.signals.Signal1D
        Map showing the intensities of each channel at each pixel position. Intensities are normalised to the maximum within that channel. Will be of the form `<BaseSignal |x, y>`.
    channels: [SpanChannel]
        list of channels displayed in this `SpanMap`.
        
    Examples
    --------
    
    
    
    """
    
    colours = ['red', 'green', 'blue']
    
    def __init__(self, hs, *channels):
        self.hs = hs
        
        self.nav = self.hs.sum()
        self.channels = list(channels)
        
        self.peakmap = hs.deepcopy().sum(axis=-1)
        self.peakmap.data[...] = np.nan
                
        self._aximages = {}
        
        # for blitting, see https://matplotlib.org/stable/tutorials/advanced/blitting.html
        self._sig_bg = None
        
    def plot_nav(self):
        self.nav.plot()
        nav_plot = self.nav._plot.signal_plot
        
        for channel in self.channels:
            if not channel.roi:
                channel.create_roi(self.nav)

            def cb(roi, changed_channel=channel):  # late binding nonsense!
                return self._channel_changed(changed_channel=changed_channel)
            
            channel.roi.events.changed.connect(cb)
                
    def plot_signal(self):
        self.peakmap.plot(navigator_kwds=dict(colorbar=False, scalebar_color='k'))
        sig_plot = self.peakmap._plot.navigator_plot
        
        self._sig_bg = sig_plot.figure.canvas.copy_from_bbox(sig_plot.figure.bbox)
        sig_plot.figure.canvas.mpl_connect("draw_event", self._on_sig_draw)
        
        sigs = [channel(self.hs) for channel in self.channels]
        
        for channel in self.channels:
            self._plot_channel(channel)
        
    def plot(self):
        self.plot_nav()
        self.plot_signal()
        
    def _plot_channel(self, channel):
        aximage = self.peakmap._plot.navigator_plot.ax.imshow(channel(self.hs),
                                                    alpha=channel.alpha, 
                                                    extent=self.peakmap._plot.navigator_plot._extent, 
                                                    cmap=channel.cmap,
                                                    zorder=channel.zorder,
                                                    vmin=0, vmax=1)

        self._aximages[channel] = aximage
        
    def _on_sig_draw(self, event):
        """
        I don't really understand why this is necessary, it's in:
        
        https://matplotlib.org/stable/tutorials/advanced/blitting.html
        """
        cv = self.peakmap._plot.navigator_plot.figure.canvas
        
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self._sig_bg = cv.copy_from_bbox(cv.figure.bbox)
    
    def _channel_changed(self, changed_channel):
        # this can trigger before the peakmap is actually rendered.
        if self.peakmap._plot is None:
            return
        
        fig = self.peakmap._plot.navigator_plot.figure
        ax = self.peakmap._plot.navigator_plot.ax
        
        # draws the background
        fig.canvas.restore_region(self._sig_bg)
        
        changed_aximage = self._aximages[changed_channel]
        
        changed_aximage.set_data(changed_channel(self.hs))

        # remove the maps, stops strange transparent things happening... I think!
        for channel in self.channels:
            try:
                self._aximages[channel].remove()
            except ValueError:
                pass
        
        # I feel like this is possible without redrawing everything...
        for channel in self.channels: 
            aximage = self._aximages[channel]
            
            aximage.set_zorder(channel.zorder)
            ax.draw_artist(aximage)
        
        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()

        
class SpanChannel:
    """
    Span Channel for SpanMap plots.
    
    A channel represents a colour in the auto_peak_map and a range of wavelengths/ energies to slice hyperspectra with.
    
    Arguments
    ---------
    
    colour: {'red', 'green', 'blue'}
        Colour used to represent this channel in `SpanMap.peakmap`. Should be one of {'red', 'green', 'blue'}.
    range_: [lo, hi]
        initial range the `SpanChannel` slices over. These are in the same units as `SpanMap.hs.signal_axes[0].axis`. e.g. wavelengths or energy.
    thresh: float
        threshold value below which no colour is plotted for a given position. Default is `0.3`.
    alpha: float
        level of transparency when colourmap is plotted in `SpanMap.peakmap`.
    zorder: float
        zposition when colourmap is plotted in `SpanMap.peakmap`.
    cmap: str | matplotlib.colors.Colormap
        colourmap used to render this SpanChannel in `SpanMap.peakmap`. Defaults to `f'{colour.capitalize()}s'` e.g. `red -> Reds`.
    
    Attibutes
    ---------
    roi: hyperspy.roi.SpanROI
        `SpanROI` rendered on `SpanMap.nav` to represent this range. Only one instance is allowed, maybe this is too strict, but it's very confusing to me if there's more than one!
    """
    
    def __init__(self, colour, left, right, thresh=0.2, alpha=0.5, zorder=None, cmap=None):
        self.colour = colour
        self._default_span = [left, right]
        self.thresh = thresh
        self.alpha = alpha
        self.zorder = zorder
        
        if cmap is None:
            cmap = f'{colour.capitalize()}s'
        
        self.cmap = cmap
        
        self._roi = None
        
    def __repr__(self):
        return f'<SpanChannel left={self.left} right={self.right} roi={self.roi}'
        
    @property
    def roi(self):
        return self._roi
        
    def create_roi(self, nav):
        """        
        Create a roi for this channel that is associated with the provided axes_manager
        
        Arguments
        ---------
        nav: hyperspy.signals.Signal1D
            'navigator' this span will draw onto.
        
        Returns
        -------
        roi: hyperspy.roi.SpanROI
            SpanROI for this channel.
        """    
        
        if self.roi:
            raise AttributeError("ROI associated with this channel instance has already been created, please use a reference to this instead!")
        
        left, right = self._default_span
        roi = hyperspy.roi.SpanROI(left=left, right=right)
        
        roi.interactive(nav, color=f'tab:{self.colour}')
        
        self._roi = roi
        return roi
        
    @property
    def left(self):
        """
        left side the ROI will slice over. In axes units e.g. wavelength.
        """
        if self.roi is None:
            return self._default_range[0]
        else:
            return self.roi.left

    @property
    def right(self):
        """
        right side the ROI will slice over. In axes units e.g. wavelength.
        """
        if self.roi is None:
            return self._default_range[1]
        else:
            return self.roi.right

    @property
    def bounds(self):
        """
        bounds side the ROI will slice over. In axes units e.g. wavelength.
        """
        return self.left, self.right

    def slice_sig(self, sig):
        """
        Slice a signal accordig to the current range for this channel.
        """
        counts = self.roi(sig, axes=[-1]).sum(axis=-1).data
        
        return self.normalize_slice(counts)
            
    def __call__(self, hs):
        """
        Equivalent to `self.slice_sig`
        """
        return self.slice_sig(hs)
        
    def normalize_slice(self, counts):
        """
        Take slice (typically from `self.slice_sig`) then normalise it for rendering in `SpanMap.peakmap`.
        
        Default behaviour is to divide by the maximum found in `counts`, then set any values below `self.thresh` to `np.nan`.
        """
        norm_counts = counts / counts.max()
        mask = norm_counts < self.thresh
        norm_counts[mask] = np.nan
        return norm_counts


def plot_span_map(hs, nchannels=1, thresh=0.2):
    """
    Convenience function for creating a SpanMap - a map where regions of a the signal in a hyperspectra can be selected using spans, and
    a map where integrating intensity of those spans is plotted as a function of position.

    Arguments
    ---------
    nchannels: int
        number of `SpanChannel`s to plot.
    thresh: float
        Threshold value where normalised integrated intensity for a given channel is plotted as fully transparent.

    Notes
    -----
    For finer control of the plot, use the `SpanMap` and `SpanChannel` classes directly

    """
    lo, hi = hs.axes_manager.signal_axes[0].axis[[0, -1]]
    width = ((hi - lo) / (nchannels * 2))
    
    channels = []
    
    for i, colour in zip(range(nchannels), SpanMap.colours):
        channels.append(SpanChannel(colour, 
                                     left=lo + i * width, 
                                     right=(lo + (i + 1) * width) - 1, 
                                     thresh=thresh,
                                     alpha=1 / nchannels,
                                     zorder=i))
    
    apm = SpanMap(hs, *channels)
    apm.plot()
    return apm

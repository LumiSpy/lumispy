import hyperspy.drawing.widgets
import hyperspy.roi
import numpy as np


class AutoPeakMap:
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
    channels: *RangeChannel
        a number of RangeChannels to slice up and view `hs` via.
        
        
    Attributes
    ----------
    nav: hyperspy.signals.Signal1D
        'navigator' used to interactively set the range of each channel. Will be of the form `<BaseSignal | sig>`
    peakmap: hyperspy.signals.Signal1D
        Map showing the intensities of each channel at each pixel position. Intensities are normalised to the maximum within that channel. Will be of the form `<BaseSignal |x, y>`.
    channels: [RangeChannel]
        list of channels displayed in this `AutoPeakMap`.
        
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
        
        self._sig_bg = None
        
    def plot_nav(self):
        self.nav.plot()
        nav_plot = self.nav._plot.signal_plot
        
        for channel in self.channels:
            if not channel.widget:
                channel.create_widget(self.nav.axes_manager, nav_plot.ax)

            def cb(obj, changed_channel=channel):  # late binding nonsense!
                return self._channel_changed(changed_channel=changed_channel)
            
            channel.widget.events.changed.connect(cb)
                
    def plot_signal(self):
        self.peakmap.plot(navigator_kwds=dict(colorbar=False, scalebar_color='k'))
        sig_plot = self.peakmap._plot.navigator_plot
        
        self._sig_bg = sig_plot.figure.canvas.copy_from_bbox(sig_plot.figure.bbox)
        
        sigs = [channel(self.hs) for channel in self.channels]
        
        for channel in self.channels:
            self._plot_channel(channel)
            
        sig_plot.figure.canvas.mpl_connect("draw_event", self._on_sig_draw)
        
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
        
        fig.canvas.restore_region(self._sig_bg)
        
        changed_aximage = self._aximages[changed_channel]
        
        changed_aximage.set_data(changed_channel(self.hs))
        
        for channel in self.channels: # I feel like this is possible without redrawing everything...
            
            aximage = self._aximages[channel]
            
            aximage.set_zorder(channel.zorder)
            
            ax.draw_artist(aximage)

        
        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()
        
        

        
class RangeChannel:
    """
    Range channel for AutoPeakMap plots.
    
    A channel represents a colour in the auto_peak_map and a range of wavelengths/ energies to slice hyperspectra with.
    
    Arguments
    ---------
    
    colour: {'red', 'green', 'blue'}
        Colour used to represent this channel in `AutoPeakMap.peakmap`. Should be one of {'red', 'green', 'blue'}.
    range_: [lo, hi]
        initial range the `RangeChannel` slices over. These are in the same units as `AutoPeakMap.hs.signal_axes[0].axis`. e.g. wavelengths or energy.
    thresh: float
        threshold value below which no colour is plotted for a given position. Default is `0.3`.
    alpha: float
        level of transparency when colourmap is plotted in `AutoPeakMap.peakmap`.
    zorder: float
        zposition when colourmap is plotted in `AutoPeakMap.peakmap`.
    cmap: str | matplotlib.colors.Colormap
        colourmap used to render this RangeChannel in `AutoPeakMap.peakmap`. Defaults to `f'{colour.capitalize()}s'` e.g. `red -> Reds`.
    
    Attibutes
    ---------
    widget: hyperspy.drawing.widgets.RangeWidget
        `RangeWidget` rendered on `AutoPeakMap.nav` to represent this range. Only one instance is allowed, maybe this is too strict, but it's very confusing to me if there's more than one!
    """
    
    def __init__(self, colour, range_, thresh=0.2, alpha=0.5, zorder=None, cmap=None):
        self.colour = colour
        self._default_range = range_
        self.thresh = thresh
        self.alpha = alpha
        self.zorder = zorder
        
        if cmap is None:
            cmap = f'{colour.capitalize()}s'
        
        self.cmap = cmap
        
        self._widget = None
        
    @property
    def widget(self):
        return self._widget
        
    def create_widget(self, am, ax):
        """        
        Create a widget for this channel that is associated with the provided axes_manager
        
        Arguments
        ---------
        am: hyperspy.axes_manager
        ax: matplotlib ax to plot the widget on
        
        Returns
        -------
        widget: hyperspy.drawing.widgets.RangeWidget
            range widget for this channel.
        """    
        
        if self.widget:
            raise AttributeError("Widget associated with this channel instance has already been created, please use a reference to this instead!")
        
        widget = hyperspy.drawing.widgets.RangeWidget(am, 
                                                      useblit=True, 
                                                      color=f'tab:{self.colour}',
                                                      direction='horizontal')
        
        widget.set_mpl_ax(ax)        
        
        left, right = self._default_range
        widget.set_bounds(left=left, right=right)
        
        self._widget = widget
        return widget
        
    @property
    def range_(self):
        """
        The current range the widget will slice over. In axes units e.g. wavelength.
        """
        if self.widget is None:
            return self._default_range
        else:
            return self.widget._get_range()  
            
    def slice_sig(self, sig):
        """
        Slice a signal accordig to the current range for this channel.
        """
        
        left, right = self.range_
        counts = sig.isig[left:right].sum(axis=-1).data
        
        return self.normalize_slice(counts)
            
    def __call__(self, hs):
        """
        Equivalent to `self.slice_sig`
        """
        return self.slice_sig(hs)
        
    def normalize_slice(self, counts):
        """
        Take slice (typically from `self.slice_sig`) then normalise it for rendering in `AutoPeakMap.peakmap`.
        
        Default behaviour is to divide by the maximum found in `counts`, then set any values below `self.thresh` to `np.nan`.
        """
        norm_counts = counts / counts.max()
        mask = norm_counts < self.thresh
        norm_counts[mask] = np.nan
        return norm_counts

    

def plot_auto_peakmap(hs, nranges=1, thresh=0.2):
    lo, hi = hs.axes_manager.signal_axes[0].axis[[0, -1]]
    width = ((hi - lo) // (nranges * 2))
    
    channels = []
    
    for i, colour in zip(range(nranges), AutoPeakMap.colours):
        channels.append(RangeChannel(colour, 
                                     range_=[lo + i * width, (lo + (i + 1) * width) - 1], 
                                     thresh=thresh,
                                     alpha=1 / nranges,
                                     zorder=i))
        
    
    apm = AutoPeakMap(hs, *channels)
    apm.plot()
    return apm

import hyperspy.api as hs
from warnings import warn


def plot_span_map(sig, nspans=1):
    """
    Plot a span map.
    
    Plots a navigator consisting of the sum over all positions in sig, with `nspans` spans. 

    For each span a `BaseSignal` image is plotted consisting of integrated counts over the the range defined by the span.

    The spans can be moved interactively and the corresponding images will update automatically.

    Arguments
    ---------
    sig: hyperspy.signals.Signal1D
        hyperspectra to inspect. Should have 2 spatial dimensions and 1 signal dimension.
    nspans: int
        number of channels to plot. Maximum is 3, default is 1.

    Returns
    -------
    spans: [hs.roi.SpanROI]
        The span ROIs from the navigator
    span_sigs: [hs.signals.BaseSignal]
        slices of `sig` according to each span roi
    span_sums: [hs.signals.BaseSignal]
        the summed `span_sigs`.
    """
    if nspans > 3:
        raise ValueError("Maximum number of spans allowed is 3")

    
    if sig.axes_manager.signal_dimension != 1 or sig.axes_manager.navigation_dimension != 2:
        sig_dims, nav_dims = sig.axes_manager.signal_dimension, sig.axes_manager.navigation_dimension
        warn(f"This method is designed for data with 1 signal and 2 navigation dimensions, not {sig_dims} and {nav_dims} respectively"
              " - therefore this function may misbehave")

    colors = ['red', 'green', 'blue']
    
    spans = []
    span_sigs = []
    span_sums = []
    
    ax_sig = sig.axes_manager.signal_axes[0].axis
    ax_sig_range = ax_sig[-1] - ax_sig[0]
    
    span_width = ax_sig_range / (2 * nspans)
    
    all_s = sig.nansum()
    all_s.plot()
    
    for i in range(nspans):
        # create a span that has a unique range 
        span = hs.roi.SpanROI(i * span_width + ax_sig[0], 
                              (i + 1) * span_width + ax_sig[0])
        spans.append(span)
        
        color = colors[i]
        
        # add it to the sum over all positions
        span.add_widget(all_s, color=colors[i])
        
        # create a signal that is the spectral slice of sig
        span_sig = hs.interactive(span, signal=sig, event=span.events.changed, axes=sig.axes_manager.signal_axes)
        span_sigs.append(span_sig)
        
        # create a signal that is the spectral integral of span_sig
        span_sum = span_sig.nansum(-1).as_signal2D([0, 1]) # convert to signal, otherwise the navigator doesn't support updating...?
        span_sums.append(span_sum)
        
        span_sum.plot(cmap=f'{color.capitalize()}s')
        
        # connect the span signal changing range to the value of span_sum
        hs.interactive(span_sig.nansum, axis=-1, 
               event=span_sig.axes_manager.events.any_axis_changed,
               out=span_sum)

    # return all ya bits for future messing around.
    return spans, span_sigs, span_sums


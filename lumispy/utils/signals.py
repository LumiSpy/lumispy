import numpy as np
from hyperspy.axes import FunctionalDataAxis
from scipy.ndimage import center_of_mass
from scipy.interpolate import interp1d


def com(spectrum_intensities, signal_axis, **kwargs):
    """Finds the centroid (center of mass) of a peak in the spectrum based
    from the intensity at each pixel value and its respective signal axis.

    Parameters
    ----------
    spectrum_intensities : array
        An array with the intensities of the spectrum.
    signal_axis: hyperspy.axes.BaseDataAxis subclass
        A HyperSpy signal axis class containing an array with the wavelength/
        energy for each intensity/signal value.
    kwargs : dictionary
        For the scipy.interpolate.interp1d function.

    Returns
    -------
    center_of_mass : float
        The centroid of the spectrum.

    Examples
    --------
    # Assume we have a spectrum with wavelengths and intensities
    >>> wavelengths = [200, 300, 400, 500, 600, 700]
    >>> intensities = [1, 2, 3, 2, 1, 0]
    >>> from hyperspy.axes import DataAxis
    >>> signal_axis = DataAxis(axis=wavelengths)

    >>> center_of_mass = com(intensities, signal_axis)
    >>> print(center_of_mass)  # Outputs: [400.0]
    """

    def _interpolate_signal(axis_array, index, **kwargs):
        """
        Wrapper for `hs.axes.index2value` that linearly interpolates between
        values should the index passed not be a integer. Using the kwargs, the
        interpolation method can be changed.
        """
        rem = index % 1
        index = int(index // 1)
        if rem == 0:
            return axis_array[int(index)]
        else:
            y = [axis_array[index], axis_array[index + 1]]
            x = [0, 1]
            fx = interp1d(x, y, **kwargs)
            return float(fx(rem))

    # Find center of mass wrt array index
    index_com = float(center_of_mass(spectrum_intensities)[0])

    # Check for the type of hyperspy.axis
    if type(signal_axis) == FunctionalDataAxis:
        # Calculate value y from x[index_com]
        x = _interpolate_signal(signal_axis.x.axis, index_com)
        kwargs = {}
        for kwarg in signal_axis.parameters_list:
            kwargs[kwarg] = getattr(signal_axis, kwarg)
        com_val = signal_axis._function(x, **kwargs)

    elif hasattr(signal_axis, "axis"):
        # Calculate value interpolating between index_com 0 and 1
        com_val = _interpolate_signal(signal_axis.axis, index_com)
    elif type(signal_axis) in (list, np.ndarray, tuple):
        # Check for dimensionality
        if len(spectrum_intensities) != len(signal_axis):
            raise ValueError(
                f"The length of the spectrum array {len(spectrum_intensities)} must match "
                "the length of the wavelength array {len(signal_axis)}."
            )
        # Calculate value interpolating between index_com 0 and 1
        com_val = _interpolate_signal(np.array(signal_axis), index_com)
    else:
        raise ValueError("The parmeter `signal_axis` must be a HyperSpy Axis object.")

    return com_val






import warnings
import matplotlib.pyplot as plt

from hyperspy.drawing._markers.circles import Circles
from matplotlib import get_backend

def dark_spot_counter(
    image, 
    log_algorithm=True,
    max_sigma=30, 
    min_sigma=12, 
    num_sigma=5, 
    threshold=0.1,    
    overlap=0.5,
    log_scale=False,
    exclude_border=True,
    invert_img=True,
    click_tolerance=0.06, 
    r=0.15, 
    color='g', 
    linewidth=2
):
    """
    Interactive tool for detecting and marking dark spots in an image using 
    the Laplacian of Gaussian (LoG) method, with optional manual adjustments 
    via mouse clicks. Updates image metadata to reflect the number and density 
    of detected dark spots.

    Parameters
    ----------
    image : hyperspy Signal2D object
        The image to be processed and annotated.
    log_algorithm : bool, default True
        Whether to use the Laplacian of Gaussian (LoG) algorithm for dark spot detection.
    max_sigma : float, default 30
        The maximum sigma value for the LoG filter, determining the largest scale of detection.
    min_sigma : float, default 12
        The minimum sigma value for the LoG filter, determining the smallest scale of detection.
    num_sigma : int, default 5
        The number of sigma values to use for the LoG filter.
    threshold : float, default 0.1
        The threshold for detecting dark spots.
    overlap : float, default 0.5
        The overlap parameter for the LoG filter, defining the minimum overlap between detected spots.
    log_scale : bool, default False
        Whether to use logarithmic scale in the LoG filter.
    exclude_border : bool, default True
        Whether to exclude dark spots near the borders of the image.
    invert_img : bool, default True
        Whether to invert the image before applying the LoG filter.
    click_tolerance : float, default 0.06
        The tolerance for detecting clicks when adding or removing markers.
    r : float, default 0.15
        The radius of the markers used to display detected dark spots.
    color : str, default 'g'
        The color of the markers used to display detected dark spots.
    linewidth : float, default 2
        The linewidth of the edges of the markers used to display detected dark spots.

    Returns
    -------
    None
        Updates the image with marked dark spots and modifies the metadata to 
        include the number and density of detected dark spots.
    """

    if get_backend() != 'widget':
        warnings.warn("You are not using the matplotlib widget backend. Interactive features may not work optimally with this setting.")

    if image.axes_manager.as_dictionary()['axis-0']['units'] is None:
        warnings.warn("The provided signal does not possess units in its axes_manager; therefore, dark spot density calculations may be inaccurate. Supported units include: 'µm', 'nm'")

    # Determine conversion factor for physical area calculation
    factor = 1
    if image.axes_manager[0].units == 'µm': 
        factor = 1e-6
    elif image.axes_manager[0].units == 'nm': 
        factor = 1e-9

    # Calculate physical area of image in metres for density calculation
    h = image.axes_manager[0].size * image.axes_manager[0].scale * factor
    w = image.axes_manager[1].size * image.axes_manager[1].scale * factor
    
    def update_density():
        """Update density in image metadata."""
        N = len(image.metadata.Markers.as_dictionary()['Circles']['kwargs']['offsets'])
        density = "{:.3e}".format(N / (h * w * 1e4))  # Calculate density in cm^-2
        image.metadata.set_item('Dark_spots.number', N)
        image.metadata.set_item('Dark_spots.density', density)
        image.metadata.set_item('Dark_spots.density_units', 'cm$^{-2}$') 
        plt.title(r'$\rho_{\text{spots}} = \text{' + density + r'} \text{ cm}^{-2}$')

    # Initialize marker collection from existing or create a new one
    if image.metadata.has_item('Markers'):
        marker = Circles(**image.metadata.Markers.Circles.kwargs)
        del image.metadata.Markers.Circles  # Remove to avoid duplication
    else:
        marker = Circles(
            offsets=np.empty((0, 2)), 
            sizes=np.array([r]), 
            edgecolor=color, 
            linewidth=linewidth
        )
        
    # Perform Laplacian of Gaussian algorithm 
    if log_algorithm:
        from hyperspy.utils.peakfinders2D import find_peaks_log

        image_log = (image.map(np.max, inplace=False) - image) if invert_img else image

        blobs = find_peaks_log(
            image_log.data, 
            min_sigma,
            max_sigma,
            num_sigma,
            threshold,
            overlap,
            log_scale,
            exclude_border
        )
        
        y = blobs[:, 0] * image.axes_manager[1].scale
        x = blobs[:, 1] * image.axes_manager[0].scale

        marker.add_items(offsets=np.stack((x, y), axis=1), sizes=np.array([]))
        image.add_marker(marker, permanent=True)
        update_density()
    else:
        image.plot()

    # Event handlers for mouse clicks
    def click1(event):  
        if event.inaxes is not None: 
            index = (np.array([], dtype=np.int64),)

            if len(marker.get_current_kwargs()['offsets']) > 0:
                index = np.where(np.all(np.isclose(marker.get_current_kwargs()['offsets'], [event.xdata, event.ydata], atol=click_tolerance), axis=1))
                
                if len(index[0]) == 1:
                    marker.remove_items(indices=index[0][0])    

            if len(index[0]) == 0: 
                marker.add_items(offsets=np.array([[event.xdata, event.ydata]]), sizes=np.array([]))
        
            image.add_marker(marker, permanent=True)
            update_density()
            
    def click2(event):  
        if event.inaxes is not None: 
            update_density()
   
    plt.connect('button_press_event', click1)
    plt.connect('button_release_event', click2)


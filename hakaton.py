import rasterio
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy
import glob

images = glob.glob("im/*.tif")


for filename in images:

    with rasterio.open(filename) as src:
        band_blue = src.read(1)
    with rasterio.open(filename) as src:
        band_green = src.read(2)
    with rasterio.open(filename) as src:
        band_red = src.read(3)
    with rasterio.open(filename) as src:
        band_nir = src.read(4)
    
    # Do not display error when divided by zero 
    numpy.seterr(divide='ignore', invalid='ignore')
    
    #ndvi = (band_nir.astype(float) + band_red.astype(float)) / (band_nir + band_red)
    #NDWI = (Green - NIR) / (Green + NIR)
    ndvi = (band_green.astype(float) - band_nir.astype(float)) / (band_green.astype(float) + band_nir.astype(float))
    
    class MidpointNormalize(colors.Normalize):
       
        def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
            self.midpoint = midpoint
            colors.Normalize.__init__(self, vmin, vmax, clip)
    
        def __call__(self, value, clip=None):
           
            x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
            return numpy.ma.masked_array(numpy.interp(value, x, y), numpy.isnan(value))
    
    # Set min/max values from NDVI range for image
    min=numpy.nanmin(ndvi)
    max=numpy.nanmax(ndvi)
    
    # Set our custom midpoint for most effective NDVI analysis
    mid=0.1
    
    # Setting color scheme ref:https://matplotlib.org/users/colormaps.html as a reference
    colormap = plt.cm.RdYlGn 
    norm = MidpointNormalize(vmin=min, vmax=max, midpoint=mid)
    
    fig = plt.figure(figsize=(10,5))
    
    ax = fig.add_subplot(111)
    
    # Use 'imshow' to specify the input data, colormap, min, max, and norm for the colorbar
    cbar_plot = ax.imshow(ndvi, cmap=colormap, vmin=min, vmax=max, norm=norm)
    
    # Turn off the display of axis labels 
    ax.axis('off')
    # Set a title 
    ax.set_title('NDWI: ' + str(filename[3:-4]), fontsize=17, fontweight='bold')
    # Configure the colorbar
    cbar = fig.colorbar(cbar_plot, orientation='horizontal', shrink=0.65)
    
    # Call 'savefig' to save this plot to an image file
    name = str(filename[3:-4])+'.png'
    fig.savefig(name, dpi=200, bbox_inches='tight', pad_inches=0.7)
    
    # let's visualize
    plt.show()

# load the prepared dataset
import sunpy.io
import sunpy.map
from numpy import load
from numpy import savez_compressed

from matplotlib import pyplot

from numpy.random import randint

base = "/Users/lxy/Desktop/Rice/PHYS 491 & 493 Research/data/"

lis = sunpy.io.fits.read(
    base + "094/AIA" + "20190309" + "_0000_0094.fits")
data, header = lis[1]

# load the dataset
data = load('maps_256.npz')
src_images, tar_images = data['arr_0'], data['arr_1']
print('Loaded: ', src_images.shape, tar_images.shape)
# plot source images
n_samples = 3
for i in range(n_samples):
    # pyplot.subplot(2, n_samples, 1 + i)
    # pyplot.axis('off')
    res = src_images[i].reshape(src_images[i].shape[0], src_images[i].shape[1])
    mymap = sunpy.map.Map(res, header)
    mymap.peek(draw_limb=True)
# pyplot.imshow(src_images[i], cmap= "gray", vmax= 1.0, vmin= -1.0)
# plot target image
for i in range(n_samples):
    # pyplot.subplot(2, n_samples, 1 + n_samples + i)
    # pyplot.axis('off')
    res = tar_images[i].reshape(tar_images[i].shape[0], tar_images[i].shape[1])
    mymap = sunpy.map.Map(res, header)
    mymap.peek(draw_limb=True)
# pyplot.imshow(tar_images[i], cmap= "gray", vmax= 1.0, vmin= -1.0)
pyplot.show()

import sunpy.io
import sunpy.map

from keras.models import load_model
from numpy import load
from numpy import vstack
import numpy as np
from matplotlib import pyplot

from numpy.random import randint
base = "/Users/lxy/Desktop/Rice/PHYS 491 & 493 Research/data/"

lis = sunpy.io.fits.read(
    base + "094/AIA" + "20190309" + "_0000_0094.fits")
data, header = lis[1]


# load and prepare training images
def load_real_samples(filename):
    # load compressed arrays
    data = load(filename)
    # unpack arrays
    X1, X2 = data['arr_0'], data['arr_1']
    # scale from [0,255] to [-1,1]
    # X1 = (X1 - 127.5) / 127.5
    # X2 = (X2 - 127.5) / 127.5
    # Reshape
    X1 = np.reshape(X1, (X1.shape[0], X1.shape[1], X1.shape[2], 1))
    X2 = np.reshape(X2, (X2.shape[0], X2.shape[1], X2.shape[2], 1))
    return [X1, X2]


# plot source, generated and target images
def plot_images(src_img, gen_img, tar_img):
    images = vstack((src_img, gen_img, tar_img))
    # scale from [-1,1] to [0,1]
    # images = (images + 1) / 2.0
    titles = ['Source', 'Generated', 'Expected']
    # plot images row by row
    for i in range(len(images)):
        res = images[i].reshape(images[i].shape[0], images[i].shape[1])
        # define subplot
        # pyplot.subplot(1, 3, 1 + i)
        # turn off axis
        # pyplot.axis('off')
        mymap = sunpy.map.Map(res, header)
        mymap.peek(draw_limb=True)
        # im = mymap.plot()
        # pyplot.show()
        # plot raw pixel data
        # pyplot.imshow(res)
        # show title
        # pyplot.title(titles[i])
        # pyplot.savefig(base + str(i) + "_Fe_XVIII.jpg")
        pyplot.clf()
    # pyplot.show()


if __name__ == "__main__":
    # load dataset
    [X1, X2] = load_real_samples('maps_256_data.npz')
    print('Loaded', X1.shape, X2.shape)
    # load model
    model = load_model('model_001700.h5')
    # select random example
    ix = randint(0, len(X1), 1)
    print(ix)
    src_image, tar_image = X1[ix], X2[ix]
    # generate image from source
    gen_image = model.predict(src_image)
    # plot all three images
    plot_images(src_image, gen_image, tar_image)
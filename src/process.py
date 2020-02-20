import sunpy.io
import sunpy.map
import sunpy.data.sample
import matplotlib.pyplot as plt
from numpy import asarray
from numpy import vstack
# from keras.preprocessing.image import img_to_array
# from keras.preprocessing.image import load_img
from numpy import savez_compressed

base = "/Users/lxy/Desktop/Rice/PHYS 491 & 493 Research/data/"
years = ["2019"]
months = [str(i + 1) for i in range(12)]
months = list(map(lambda i: '0' + i if len(i) == 1 else i, months))
days = [str(i + 1) for i in range(31)]
days = list(map(lambda i: '0' + i if len(i) == 1 else i, days))

a1 = -7.31 * 10 ** (-2)
a2 = -9.75 * 10 ** (-1)
a3 = -9.90 * 10 ** (-2)
a4 = -2.84 * 10 ** (-3)
f = 0.31


def process(*argv):
    """

    """
    filename = 'maps_1024.npz'

    src_list = []
    tar_list = []
    for yr in years:
        for mo in months[:3]:
            for da in days:
                try:
                    lis = sunpy.io.fits.read(
                        base + "094/AIA" + yr + mo + da + "_0000_0094.fits")
                    smap171 = sunpy.map.Map(
                        base + "171/AIA" + yr + mo + da + "_0000_0171.fits")
                    smap193 = sunpy.map.Map(
                        base + "193/AIA" + yr + mo + da + "_0000_0193.fits")

                    # formula comes from appendix of doi:10.1088/0004-637X/759/2/141
                    inside = (f * smap171.data) + ((1 - f) * smap193.data) / 116.54
                    smap = 0.39 * (a1 * inside ** 1 + a2 * inside ** 2 + a3 * inside ** 3 + a4 * inside ** 4)
                    data, header = lis[1]

                    # Mius the warm portion of the picture
                    mymap = sunpy.map.Map(data - smap, header)
                    # mymap.peek(draw_limb=True)
                    tar = mymap.data
                    print(yr + mo + da)

                    if "256" in argv:
                        filename = 'maps_256.npz'
                        data = downsample_256(data)
                        tar = downsample_256(tar)

                    # Add data
                    if "addData" in argv:
                        src_list.append(data)
                        tar_list.append(tar)

                    im = mymap.plot()
                    if "show" in argv:
                        plt.show()
                    if "saveFig" in argv:
                        plt.savefig(base + yr + mo + da + "_Fe_XVIII.jpg")
                except FileNotFoundError:
                    pass

    if "saveFile" in argv:
        src_images = asarray(src_list)
        tar_images = asarray(tar_list)
        print('Loaded: ', src_images.shape, tar_images.shape)
        savez_compressed(filename, src_images, tar_images)
        print('Saved dataset: ', filename)


def downsample_256(src, *argv):
    """

    """
    res = []
    for i in range(256):
        line = []
        for j in range(256):
            num = - float("inf")
            for x in range(4):
                for y in range(4):
                    if src[4 * i + x][4 * j + y] > num:
                        num = src[4 * i + x][4 * j + y]
            line.append(num)
        res.append(line)
    return res


def plot_day(yr: str, mo: str, da: str):
    """

    :param yr:
    :param mo:
    :param da:
    """
    lis = sunpy.map.Map(
        base + "094/AIA" + yr + mo + da + "_0000_0094.fits")
    im = lis.plot()
    plt.savefig(base + yr + mo + da + "_0000_0094.jpg")
    smap171 = sunpy.map.Map(
        base + "171/AIA" + yr + mo + da + "_0000_0171.fits")
    im = smap171.plot()
    plt.savefig(base + yr + mo + da + "_0000_0171.jpg")
    smap193 = sunpy.map.Map(
        base + "193/AIA" + yr + mo + da + "_0000_0193.fits")
    im = smap193.plot()
    plt.savefig(base + yr + mo + da + "_0000_0193.jpg")


if __name__ == "__main__":
    # process("addData", "256", "saveFile")
    plot_day("2019", "03", "20")

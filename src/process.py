# -*- coding: utf-8 -*-
"""
=================================
Process the EUV Data
=================================

The general workflow is generate ->
downsample -> normalize -> mask_out
-> Save
"""

import sunpy.io
import sunpy.map
import sunpy.data.sample
import matplotlib.pyplot as plt
from numpy import asarray
import numpy as np
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

ignore_list = ["20190101", "20190110", "20190112", "20190113", "20190114", "20190115", "20190116", "20190118",
               "20190119", "20190120", "20190228", "20190307", "20190327", "20190328", "20190330", "20190331",
               "20190422", "20190423", "20190424", "20190426", "20190427", "20190428", "20190429", "20190430",
               "20190501", "20190502", "20190520", "20190521", "20190522", "20190523", "20190524", "20190529",
               "20190615", "20190617", "20190618", "20190619", "20190620", "20190621", "20190622", "20190623",
               "20190714", "20190716", "20190717", "20190718", "20190719", "20190721", "20190728", "20190729",
               "20190730", "20190801", "20190802", "20190810", "20190811", "20190812", "20190813", "20191111"]

def process(*argv):
    """

    """
    filename = 'maps_1024.npz'

    src_list = []
    tar_list = []
    for yr in years:
        for mo in months:
            for da in days:
                try:
                    lis = sunpy.io.fits.read(
                        base + "094/AIA" + yr + mo + da + "_0000_0094.fits")
                    # smap094 = sunpy.map.Map(
                    #     base + "094/AIA" + yr + mo + da + "_0000_0094.fits")
                    smap171 = sunpy.map.Map(
                        base + "171/AIA" + yr + mo + da + "_0000_0171.fits")
                    smap193 = sunpy.map.Map(
                        base + "193/AIA" + yr + mo + da + "_0000_0193.fits")

                    # formula comes from appendix of doi:10.1088/0004-637X/759/2/141
                    inside = (f * smap171.data) + ((1 - f) * smap193.data) / 116.54
                    smap = 0.39 * (a1 * inside ** 1 + a2 * inside ** 2 + a3 * inside ** 3 + a4 * inside ** 4)
                    data, header = lis[1]

                    # smap094_ = sunpy.map.Map(mask_out(smap094.data), header)
                    # smap094_.peek(draw_limb=True)
                    # smap171.peek(draw_limb=True)
                    # smap193.peek(draw_limb=True)
                    # mymap.peek(draw_limb=True)

                    tar = data - smap
                    print(yr + mo + da)

                    if "removeFlare" in argv:
                        if np.amax(tar) > 1e8:
                            print("ignore : " + yr + mo + da)
                            continue

                    if "256" in argv:
                        filename = 'maps_256_flare.npz'
                        data = downsample_256(data)
                        tar = downsample_256(tar)

                    if "mask" in argv:
                        mask_out(data)
                        mask_out(tar)

                    if "normalize" in argv:
                        data = normalize(data)
                        tar = normalize(tar)

                    if "addData" in argv:
                        src_list.append(data)
                        tar_list.append(tar)

                    if "show" in argv:
                        mymap = sunpy.map.Map(tar, header)
                        mymap.peek(draw_limb=True)
                        # im = mymap.plot()
                        # plt.show()
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


def normalize(src):
    """
    Normalize the data set to [-1, 1]
    :param src:
    :return:
    """
    # min_ = np.amin(src)
    # src = np.log2(src - min_ + 2**(-1))

    _max = np.amax(src)
    _min = np.amin(src)

    # Normalize the maximum and minimum to one
    src = (src - ((_max + _min)/2)) / ((_max - _min)/2)
    _max1 = np.amax(src)
    _min1 = np.amin(src)

    # Make sure that normalize is success
    print(_max1, _min1)
    assert(_max1 == 1.0 and abs(_min1 + 1) < 10**(-10))
    return src


def mask_out(src):
    """
    Mask the data  outside of the disk. 0.3846 is a number calculated based on the structure
    of the pic. Due to -inf, this is normally done after normalize
    :param src: full disk data
    :return:    the masked src
    """

    mini = np.amin(src)

    num = len(src)  # can do this since the data is square
    for i in range(num):
        for j in range(num):
            if (i - num/2) ** 2 + (j - num/2) ** 2 > (0.3846 * num) **2:
                src[i][j] = mini

    assert(len(src) == 256 and len(src[0]) == 256)




def plot_day(yr: str, mo: str, da: str):
    """

    :param yr:
    :param mo:
    :param da:
    """

    # lis = sunpy.io.fits.read(
    #     base + "094/AIA" + yr + mo + da + "_0000_0094.fits")
    # data, header = lis[1]
    # mymap = sunpy.map.Map(mask_out(data), header)
    smap094 = sunpy.map.Map(
        base + "094/AIA" + yr + mo + da + "_0000_0094.fits")
    im = smap094.plot()
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
    process("removeFlare", "256", "mask", "normalize", "addData",  "saveFile") # "addData", "256", "saveFile"
# "256", "mask", "normalize", "addData",
import sunpy.io
import sunpy.map
import sunpy.data.sample
from sunpy.map.maputils import all_coordinates_from_map
import matplotlib.pyplot as plt

import numpy as np
lis =  sunpy.io.fits.read("/Users/lxy/Desktop/Rice/PHYS 491 & 493 Research/data/094/AIA20190308_0000_0094.fits")
smap094 = sunpy.map.Map("/Users/lxy/Desktop/Rice/PHYS 491 & 493 Research/data/094/AIA20190308_0000_0094.fits")
smap171 = sunpy.map.Map("/Users/lxy/Desktop/Rice/PHYS 491 & 493 Research/data/171/AIA20190308_0000_0171.fits")
smap193 = sunpy.map.Map("/Users/lxy/Desktop/Rice/PHYS 491 & 493 Research/data/193/AIA20190308_0000_0193.fits")

print(lis)
# smap094.peek(draw_limb=True)
# smap171.peek(draw_limb=True)
# smap193.peek(draw_limb=True)
# # print(sunpy.data.sample.AIA_171_IMAGE)


a1 = -7.31*10**(-2)
a2 = -9.75*10**(-1)
a3 = -9.90*10**(-2)
a4 = -2.84*10**(-3)
f = 0.31
hpc_coords = all_coordinates_from_map(smap094)
# print(np.array(smap094))
# print(smap094)
# print(type(smap094))
# print(hpc_coords)
inside = (f * smap171.data) + ((1-f) * smap193.data)/116.54
smap = 0.39 * (a1 * inside ** 1 + a2 * inside ** 2 + a3 * inside ** 3 + a4 * inside ** 4)

data,header = lis[1]
print(data)
mymap = sunpy.map.Map(data - smap, header)
mymap.peek(draw_limb=True)
im = mymap.plot()


# -*- coding: utf-8 -*-
"""
==========================
Masking out the solar disk
==========================

How to mask out all emission from the solar disk.
"""
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

import sunpy.map
from sunpy.data.sample import AIA_171_IMAGE
from sunpy.map.maputils import all_coordinates_from_map

###############################################################################
# We start with the sample data
aia = sunpy.map.Map(AIA_171_IMAGE)

###############################################################################
# A utility function gives us access to the helioprojective coordinate of each
# pixels. We can use that to create a new array which
# contains the normalized radial position for each pixel.
hpc_coords = all_coordinates_from_map(aia)
r = np.sqrt(hpc_coords.Tx ** 2 + hpc_coords.Ty ** 2) / aia.rsun_obs
# print(aia.rsun_obs)

"""
We know that sun's radius is 945.436711 arcsec in this pic (AIA_171_IMAGE), we 
can assume this is true for other cases. And center_to_corner/radius is 1.845.
We can compute that center_to_side/r = 1.305.
"""

###############################################################################
# With this information, we create a mask where all values which are less then
# the solar radius are masked. We also make a slight change to the colormap
# so that masked values are shown as black instead of the default white.
mask = ma.masked_greater_equal(r, 1)
palette = aia.cmap
palette.set_bad('black')

###############################################################################
# Finally we create a new map with our new mask.
scaled_map = sunpy.map.Map(aia.data, aia.meta, mask=mask.mask)
print(np.amin(scaled_map.data))
print(np.amax(scaled_map.data))

###############################################################################
# Let's plot the results using our modified colormap
fig = plt.figure()
plt.subplot(projection=scaled_map)
scaled_map.plot(cmap=palette)
scaled_map.draw_limb()
plt.show()

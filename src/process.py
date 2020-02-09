import sunpy.io
import sunpy.map
import sunpy.data.sample

aia =  sunpy.io.fits.read("/Users/lxy/Desktop/Rice/PHYS 491 & 493 Research/High Temperature Extraction/data/SDOAIA/AIA20190308_0000_0094.fits")
smap = sunpy.map.Map("/Users/lxy/Desktop/Rice/PHYS 491 & 493 Research/High Temperature Extraction/data/SDOAIA/AIA20190308_0000_0094.fits")
smap.peek(draw_limb=True)
# print(sunpy.data.sample.AIA_171_IMAGE)

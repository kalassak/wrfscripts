import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch

def plotPavalaCoastline():
	m.readshapefile('/home/kalassak/Desktop/pavala/shp/mainland', 'mainland')
	m.readshapefile('/home/kalassak/Desktop/pavala/shp/lakes', 'lakes')

	patches = []
	for shape in m.mainland:
		patches.append(Polygon(np.array(shape), True))

	ax.add_collection(PatchCollection(patches, facecolor='w', edgecolor='k', linewidths=2))

	patches_lake = []
	for shape in m.lakes:
		patches.append(Polygon(np.array(shape), True))

	ax.add_collection(PatchCollection(patches, facecolor='w', edgecolor='k', linewidths=2))

nc = netCDF4.Dataset("/home/kalassak/Desktop/Build_WRF/WRF/run/wrfout_d01_2020-06-05_18:00:00")

lats = nc.variables['XLAT'][:]
lons = nc.variables['XLONG'][:]
olrs = nc.variables['OLR'][:]
pres = nc.variables['PSFC'][:]
precips = (nc.variables['RAINC'][:] + nc.variables['RAINNC'][:])*.0393700787 #precip in inches
ssts = nc.variables['SST'][:]
times = nc.variables['Times'][:]

nc.close()

print np.amax(olrs)

#m = Basemap(projection='cyl', llcrnrlat=-90,urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,resolution='l')

print lats[0][83][40]
print lons[0][83][40]
f = open('out', 'w')
for i in xrange(1, len(olrs)):
	f.write(str(''.join(times[i])) + '\t' + str(olrs[i][83][40]) + '\n')

#simulated infrared/outgoing longwave radiation
for i in xrange(1, len(olrs)):
	#m = Basemap(projection='cyl', llcrnrlat=np.amin(lats[i]),urcrnrlat=np.amax(lats[i]),llcrnrlon=np.amin(lons[i]),urcrnrlon=np.amax(lons[i]),resolution='h')
	m = Basemap(width=2500000*3,height=1750000*3,
		rsphere=(6378137.00,6356752.3142),\
		resolution='l',area_thresh=1000.,projection='lcc',\
		lat_1=30,lat_2=60,lat_0=20,lon_0=-90)

	fig = plt.figure(figsize=(18.6, 10.5))
	ax = fig.add_axes((0,0,1,1))
	#ax.set_axis_off()

	m.drawcoastlines()

	#convert for basemap
	xx, yy = m(lons[i], lats[i])
	
	m.pcolormesh(xx, yy, olrs[i], cmap='Greys', vmin=100, vmax=340)

	plt.colorbar(fraction=0.025, pad=0.01)
	
	plt.title('Outgoing Longwave Radiation (W/m^2)\n%s' % ''.join(times[i]))

	plt.savefig("/home/kalassak/Desktop/olr/out_" + str(i) + ".png", bbox_inches='tight', pad_inches=0, dpi=100)
	plt.close()

	print "plot for " + str(''.join(times[i])) + " generated"
	i += 1
'''

#accumulated precipitation map
fig = plt.figure(figsize=(18.6, 10.5))
ax = fig.add_axes((0,0,1,1))
#ax.set_axis_off()

plotPavalaCoastline()

colors = [(0, 0.62, 0), (0, 0.82, 0), (0, 1, 0), (0.31, 1, 0), (0.62, 1, 0), (0.82, 1, 0), (1, 1, 0), (1, 0.82, 0), (1, 0.62, 0), (1, 0.31, 0), (1, 0, 0), (1, 0, 0.62), (1, 0.5, 0.62), (1, 0.82, 0.94), (1, 0.94, 0.97), (1, 1, 1)]
levels = [0.25, 0.5, 1, 2, 3, 4, 6, 8, 12, 16, 20, 24, 36, 48, 64, 80, 96] 

plt.contourf(lons[0], lats[0], precips[len(precips)-1], levels, colors=colors)
plt.colorbar(fraction=0.025, pad=0.01)
#m.drawcoastlines()
plt.savefig("/home/kalassak/Desktop/totalprecip.png", bbox_inches='tight', pad_inches=0, dpi=100)
plt.close()

##sst

levels = np.arange(273.15, 273.15+50, 2.5)
for i in xrange(1, len(ssts)):
	fig = plt.figure(figsize=(18.6, 10.5))
	ax = fig.add_axes((0,0,1,1))
	ax.set_axis_off()
	
	m.pcolormesh(lons[i], lats[i], ssts[i], cmap='RdBu_r')
	contours = plt.contour(lons[i], lats[i], ssts[i], levels, colors='k', linewidths=0.5)
	plt.clabel(contours, inline=1, fontsize=10, inline_spaceing=1)
	m.drawcoastlines()
	plt.savefig("/home/kalassak/Desktop/sst/out_" + str(i) + ".png", bbox_inches='tight', pad_inches=0, dpi=100)
	plt.close()

	print "plot for " + str(''.join(times[i])) + " generated"
	i += 1
'''

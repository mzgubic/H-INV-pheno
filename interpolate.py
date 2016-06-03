import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

npts = 40j

# get the data
infile = open(sys.argv[1])
lines = infile.readlines()

inxs = []
inys = []
invals = []

for line in lines:
  inxs.append(float(line.split()[0]))
  inys.append(float(line.split()[1]))
  invals.append(float(line.split()[2]))

inxs = np.array(inxs)
inys = np.array(inys)
invals = np.array(invals)

print inxs
print inys
print invals

# define the new grid
grid_x, grid_y = np.mgrid[min(inxs):max(inxs):npts, min(inys):max(inys):npts]
grid = griddata( (inxs, inys), invals, (grid_x, grid_y), method='linear')

outxs = grid_x.flatten()
outys = grid_y.flatten()
outvals = grid.flatten()

# write to file
size = str(int(abs(npts)))
outfile = open(size+'x'+size+'_'+sys.argv[1], 'w')
for i in range(len(outxs)):
  outfile.write('%4.4f %4.4f %4.4f\n' % (outxs[i], outys[i], outvals[i]))



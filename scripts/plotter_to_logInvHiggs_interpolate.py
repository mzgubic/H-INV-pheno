import numpy as np
import sys
import os
import argparse as a
from scipy.interpolate import interp1d

# parse the args
parser = a.ArgumentParser(description='Change the masses of plotter input to log')
parser.add_argument('-i', '--infile', required=True)
args = parser.parse_args()

# get the lines
infilename = args.infile
infile = open(infilename)
modelname = infilename.split("_")[0]

# do the transformation
xs = []
yields = []
for l in infile:
  line = l.split()
  m1 = float(line[0])
  val = float(line[1])
  # transform the mass to log mass
  m1 = np.log10(m1)
  xs.append(m1)
  yields.append(val)

xy = zip(xs, yields)
xy.sort()
xs = [x for (x,y) in xy]
yields = [y for (x,y) in xy]

# interpolate
#fn = interp1d(xs, yields)
#newxs = np.linspace(1.0,3.0,20)
#newyields = fn(newxs)

# don't interpolate
newxs = xs
newyields = yields

# multiply the yield above mchi = 10000 to make the limit setting converge
print "WARNING: multiplying the small yields by 10000 to make the limit setting converge later on"
print "make sure the right ones are multiplied and rescaled back after the limit setting"
print newyields
for i, y in enumerate(newyields):
  if i == 4:
    newyields[i] = newyields[i]*1000
  if i > 4:
    newyields[i] = newyields[i]*10000

print newyields

output = []
for point in range(len(newxs)):
  output.append(str(newxs[point])+' '+str(newyields[point])+'\n')

# write
f = open('output.txt', 'w')
for line in output:
  f.write(line)

os.system('mv output.txt '+infilename)


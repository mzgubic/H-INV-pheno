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
  # change lambda=100 to lambda=800
  if modelname in ["D5b"]:
    val = val*(100./1500.)**2
  if modelname in ["D5a", "D5c", "D5d"]:
    val = val*(100./800.)**2
  if modelname in ["D6a", "D6b"]:
    val = val*(100./800.)**4
  if modelname in ["D7a", "D7b", "D7c", "D7d"]:
    val = val*(100./800.)**6
  # transform the mass to log mass
  m1 = np.log10(m1)
  xs.append(m1)
  yields.append(val)

xy = zip(xs, yields)
xy.sort()
xs = [x for (x,y) in xy]
yields = [y for (x,y) in xy]

# interpolate
fn = interp1d(xs, yields)
newxs = np.linspace(1.0,3.0,40)
newyields = fn(newxs)

output = []
for point in range(len(newxs)):
  output.append(str(newxs[point])+' '+str(newyields[point])+'\n')

# write
f = open('output.txt', 'w')
for line in output:
  f.write(line)

os.system('mv output.txt '+infilename)


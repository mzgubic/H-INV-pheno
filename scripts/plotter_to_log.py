import numpy as np
import sys
import os
import argparse as a

# parse the args
parser = a.ArgumentParser(description='Change the masses of plotter input to log')
parser.add_argument('-i', '--infile', required=True)
args = parser.parse_args()

# get the lines
infilename = args.infile
infile = open(infilename)

# do the transformation
output = []
for l in infile:
  line = l.split()
  m1 = float(line[0])
  m2 = float(line[1])
  val = line[2]
  m1 = str(np.log10(m1))
  m2 = str(np.log10(m2))
  output.append(m1+' '+m2+' '+val+'\n')

# write
f = open('output.txt', 'w')
for line in output:
  f.write(line)

os.system('mv output.txt '+infilename)


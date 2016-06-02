# H-INV-pheno
Reproducing the plots of limits on the SM Higgs. I've used Delphes-3.2.0 that was slightly modified to include the variables needed for the analysis. This document will take you from the theory output files (model_parameters.hep format) to the plot. I'll outline the general procedure first and then describe it in detail with references to the scripts you can use to make the process automatic.

## General procedure
First you need to run delphes simulation on the theory files to produce the detector signature. Then you run the scorpion analysis on the delphes files to get the yield passing the selection of your analysis. From here you use the analysis yield to create the cards for the CMSSW limit setting program, which is done by a script that Patrick wrote. These limits are then written to a .root file in the not most obvious way as the procedure was recycled from a code other people wrote before us. Finally a plotting script takes these .root files and produces a plot.

## Detailed procedure

We'll start with a file that contains the locations of your .hep files, file_lists/masterlocal.txt. 


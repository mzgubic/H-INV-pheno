# H-INV-pheno
Reproducing the plots of limits on the SM Higgs. I've used Delphes-3.2.0 that was slightly modified to include the variables needed for the analysis. This document will take you from the delphes output to the plot. I'll outline the general procedure first and then describe it in detail with references to the scripts you can use to make the process automatic.

## general procedure
First you need to run the scorpion analysis on the delphes files to get the yield passing the selection of your analysis. (Make sure scorpion is compiled after you've made changes to analysis, I forgot this a couple of times.) The first number in the file is the normalised output that passed the selection. From here you need to create the cards for the CMSSW limit setting program, which is done by a script that Patrick wrote. These limits are then written to a root file in the not most obvious way as the procedure was recycled from a code other people wrote before us. Finally a plotting script takes these root files and produces a plot.

## detailed procedure including the commands

We'll start with 


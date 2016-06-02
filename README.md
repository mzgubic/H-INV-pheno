# H-INV-pheno
Reproducing the plots of limits on the SM Higgs. I've used Delphes-3.2.0 that was slightly modified to include the variables needed for the analysis. This document will take you from the theory output files (model_parameters.hep format) to the plot. I'll outline the general procedure first and then describe it in detail with references to the scripts you can use to make the process automatic.

## General procedure
First you need to run delphes simulation on the theory files to produce the detector signature. Then you run the scorpion analysis on the delphes files to get the yield passing the selection of your analysis. From here you use the analysis yield to create the cards for the CMSSW limit setting program, which is done by a script that Patrick wrote. These limits are then written to a .root file in the not most obvious way as the procedure was recycled from a code other people wrote before us. Finally a plotting script takes these .root files and produces a plot.

## Detailed procedure

We'll start with a file that contains the locations of your .hep files, file_lists/masterlocal.txt (see example uploaded).

##### Run Delphes detector simulation

First, run Delphes detector simulation by using the batch system with the following command:
```
./batchsubmit.sh file_lists/masterlocal.txt
```
This creates a script for each model, submits it to the batch system, and then deletes it. The delphes output file is moved to the directory of the .hep file. Be careful to comment out either of the lines 23 or 24 depending on whether your files contain seed numbers, i.e. whether there are multiple .hep files of the same model and parameters.

If there were multiple delphes outputs per parameter space point you need to hadd the files together so that a single delphes-output.root file is left in the directory.

##### Run scorpion analysis

You need the cross section file pythia-output.log (see example) with the correct cross section for the process in the same directory as the delphes file.

Then to the scorpion directory and get environment variables:
```
cd scorpion/
source setup.sh
```
then uncomment lines 28 and 29 of the loopdirs.sh script and run:
```
./loopdirs.sh file_lists/masterlocal.txt 
```
which results in the scorpion output files moved to the .hep files directories.


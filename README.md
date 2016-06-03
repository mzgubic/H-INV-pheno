# H-INV-pheno
Reproducing the plots of limits on the SM Higgs. I've used Delphes-3.2.0 that was slightly modified to include the variables needed for the analysis. This document will take you from the theory output files (model_parameters.hep format) to the plot. I'll outline the general procedure first and then describe it in detail with references to the scripts you can use to make the process automatic.

Apologies for the poorly structured and written code. Contact me on miha.zgubic@cern.ch if there is something wrong with the procedure or needs additional clarification.

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
Make sure that you've compiled scorpion if you've made any changes to the analysis, then uncomment lines 28 and 29 of the loopdirs.sh script and run:
```
./loopdirs.sh file_lists/masterlocal.txt 
```
which results in the scorpion output files (see jaf_CMS8_hinv20b_analysis20.txt for an example) moved to the .hep files directories.

##### Collect the analysis data in a more useful format

Collect the scorpion outputs from all the different directories by running:
```
./plotter_input.sh file_lists/masterlocal.txt 
```
which needs the folder "scripts" and the python scripts inside to execute properly. This doesn't only collect the outputs, it also performs some transformations on it. For example, the yields from effective operators are scaled in order to make the limit setting converge.

There are too few points to make pretty plots with the data available so we resort to interpolation between them to make it smoother. For EFTs this is done automatically as there is one parameter and the required Python package is available on the lx04 machine. However, for the two parameter simplified models (scalar and pseudoscalar) this needs to be done on a separate machine where the scipy.interpolate.griddata is available. To interpolate the scalar and pseudoscalar models, run:
```
python interpolate.py invisibleH2_mchi_mh2.txt
```
and the same script on the pseudoscalar output.

##### CMSSW limit setting and plotting

Now you need to move to the directory CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/plotting/ and execute
```
cms
cmsenv
```
where the cms command should be defined as:
```
alias cms='source /vols/cms/grid/setup.sh;
export SCRAM_ARCH=slc6_amd64_gcc491'
```
in your .bashrc file in the home directory. 

The calculation of the limits and the plotting are separated to save time. Each model has its own subfolder containing the limits at different luminosities. 







Reproducing the plots of limits on the SM Higgs. This document will take you from the theory output files (model_parameters.hep format) to the plot. I'll outline the general procedure first and then describe it in detail with references to the scripts you can use to make the process automatic.

Apologies for the poorly structured and written code. This code was written to work in my subdirectory on /vols/cms02/mz2512/ so if you're working in a different directory you may need to adjust the code slightly. Contact me on miha.zgubic@cern.ch if there is something wrong with the procedure or needs additional clarification.

# General procedure
First you need to run delphes simulation on the theory files to produce the detector signature. Then you run the scorpion analysis on the delphes files to get the yield passing the selection of your analysis. From here you use the analysis yield to create the cards for the CMSSW limit setting program, which is done by a script that Patrick wrote. These limits are then written to a .root file in the not most obvious way as the procedure was recycled from a code other people wrote before us. Finally a plotting script takes these .root files and produces a plot.

# Detailed procedure

We'll start with a file that contains the locations of your .hep files, file_lists/masterlocal.txt (see example uploaded).

## 1 Run Delphes detector simulation

The Delphes version that I have used was 3.2.0 which was slightly modified to include the variable needed for the analysis. First, run Delphes detector simulation using the batch system with the following command:
```
./batchsubmit.sh file_lists/masterlocal.txt
```
This creates a script for each model, submits it to the batch system, and then deletes it. The delphes output file is moved to the directory of the .hep file. Be careful to comment out either of the lines 23 or 24 depending on whether your files contain seed numbers, i.e. whether there are multiple .hep files of the same model and parameters.

If there were multiple delphes outputs per parameter space point you need to hadd the files together so that a single delphes-output.root file is left in the directory.

## 2 Run scorpion analysis

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

## 3 Collect the analysis data in a more useful format

Collect the scorpion outputs from all the different directories by running:
```
./plotter_input.sh file_lists/masterlocal.txt 
```
which needs the folder "scripts" and the python scripts inside to execute properly. This doesn't only collect the outputs, it also performs some transformations on it. For example, the yields from effective operators are scaled in order to make the limit setting converge. Don't worry about the lambda800 at the end of the output filenames, they have no meaning, I just didn't correct it when expanding the code.

There are too few points to make pretty plots with the data available so we resort to interpolation between them to make it smoother. For EFTs this is done automatically as there is one parameter and the required Python package is available on the lx04 machine. However, for the two parameter simplified models (scalar and pseudoscalar) this needs to be done on a separate machine where the scipy.interpolate.griddata is available. To interpolate the scalar and pseudoscalar models, run:
```
python interpolate.py invisibleH2_mchi_mh2.txt
```
and the same script on the pseudoscalar output.

## 4 CMSSW limit setting and plotting

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

The calculation of the limits and the plotting are separated to save time. One and two parameter models are treated separately.

#### 4.1 One parameter models: EFTs and invisible Higgs

For this you need cardmaker.py script in the home directory and the two scripts EFTlimit.py and EFTplots.sh in the CMSSW/.../plotting directory. Create subdirectories in the plotting folder for each model and put in the outputs from section 3, i.e. put D5a_mchi_lambda800.txt in the folder CMSSW/.../plotting/D5a/. Model name for invisible Higgs should be invisibleHiggs. 

Uncomment lines 3-9 in the EFTplots.sh and set the models and luminosities you want to calculate the limits for. Then run
```
./EFTplots.sh
```
This creates .root files with the limits of the models at different luminosities, and puts them into the model directories. Now you need the script plot2EFTs.py in the plotting/ directory, and uncomment the lines 14, 16, and 18 and once again run
```
./EFTplots.sh
```
which should produce the EFT limits as a function of dark matter mass at different luminosities and models, with each plot representing one class of models, grouped by their dimensionality. I suggest uncommenting each line separately as the code someone produces a broken plot and running EFTplots.sh a couple of times so that it gets it right (I don't know what causes this).

In order to produce the invisible Higgs plot two scripts are needed: plotSMHiggslumis.py and higgsplots.sh. Uncomment line 17 of higgsplots.sh and run
```
./higgsplots.sh
```

#### 4.2 Two parameter models: scalar and pseudoscalar mediators

For two parameter models the situation is slightly more complicated as there is a grid rather than a line of points in parameter space. Every .root file thus contains one line of the grid, and they are created using the makegrid.py script (written by Patrick).

I've used separate directories for models, luminosities, and number of points in the grid combinations, i.e. a directory called 40x40_20fb_mha/ and separate for 300fb, 3000fb, as well as 3 other directories for the scalar mediator. This was necessary because of how makegrid.py works. Lower grid sizes were used for testing only.

Move the interpolated 40x40_invisibleHa_mchi_mha.txt file with yields to the 40x40_20fb_mha/ directory, as well as the makegrid.py script. Go to that directory and execute
```
python makegrid.py -i 40x40_invisibleHa_mchi_mha.txt -l 20
```
where the -l option refers to the luminosity and should be set accordingly.

Finally use the higgsplots.sh script by uncommenting the appropriate lines to create the on and off shell parts of the plots, which then have to be merged by hand. For this to work, plotMultiOnShell.py and plotMultiOffShell.py are needed.




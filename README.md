# H-INV-pheno
Reproducing the plots of limits on the SM Higgs. I've used Delphes-3.2.0 that was slightly modified to include the variables needed for the analysis. This document will take you from the delphes output to the plot.

First run the scorpion analysis on the directory of the delphes files which should contain a file called delphes-output.root:
./scorpion/run_jaf.py --experiments CMS8 --jaf-output-dir scorpion/output --analyses hinv-8tev --pythia-delphes-dirs $FILEDIR

"""
how to run:
python EFTlimits.py D5a 3000

takes in a model and produces a hadded tree ready for input to the plotting script
"""
import sys
import os
import numpy as np

# get the model and lumi
model = sys.argv[1]
lumi=sys.argv[2]

# import the yields script
infile = open(model+"/"+model+"_mchi_lambda800.txt")
lines = infile.readlines()

treestring = ""
for line in lines:
    mchi = line.split()[0]
    val = line.split()[1]
    os.system("../../../../../cardmaker.py -s "+val+" -l "+lumi+" -n mchi"+mchi+" --systlumiscale True")
    os.system("combine -M Asymptotic -m "+mchi+" ext_vbfhinv_mchi"+mchi+"_13TeV_"+lumi+"fb.txt")
    os.system("mv ext_vbfhinv_mchi"+mchi+"_13TeV_"+lumi+"fb.txt "+model+"/")
    os.system("mv higgsCombineTest.Asymptotic* "+model+"/combine_mchi"+mchi+"_lumi"+lumi+"fb.root")
    treestring = treestring+model+"/combine_mchi"+mchi+"_lumi"+lumi+"fb.root "

os.system("hadd -f "+model+"/combined_"+model+"_"+lumi+"fb.root "+treestring)
os.system("rm roostats-*")
os.system("rm "+model+"/combine_*")
os.system("rm "+model+"/ext**")



#!/bin/bash
# run on master list

INPUTS=""

#change what the script does to all the files in master list 
while IFS='' read -r line || [[ -n "$line" ]]; do
   # get the file directory and print it
   FILEPATH=$line
   FILEDIR=${line%/*}"/"
   NAME=${line##*/}
   echo
   echo $FILEPATH
   echo $FILEDIR

   # unzip
   #gunzip $FILEPATH
   #sleep 20s


   # for hadding the files together
   #NAME=${line%_*}
   #NAME=${NAME%_*}"_delphes-output.root"
   #echo $NAME
   #INPUTS=$INPUTS" "$NAME

   # run scorpion
   #./scorpion/run_jaf.py --experiments CMS8 --jaf-output-dir scorpion/output --analyses hinv-8tev --pythia-delphes-dirs $FILEDIR >> looplog.txt
   #cp scorpion/output/jaf_CMS8_hinv20b_analysis20.txt $FILEDIR

   # plot the distros
   #./scorpion/run_jaf.py --experiments CMS8 --jaf-output-dir scorpion/output --analyses hinv-8tev --pythia-delphes-dirs $FILEDIR
   ##cp scorpion/output/outputfile.root ${FILEDIR}scorpion_output_B4sel.root
   #echo $line
   #NAME2=$( echo $line | sed "s/.*Results\///" | sed "s/\/.*//")
   #echo $NAME2
   #cp scorpion/output/outputfile.root scripts/test_distros/${NAME2}_B4sel.root
   

   # access the number in the jaf file
   #NAME=$FILEDIR"jaf_CMS8_hinv20b_analysis20.txt"
   #TEXT=$(cat $NAME) # get the text as a variable
   #YIELD=${TEXT%%[[:space:]]*} # remove everything after space
   #echo $YIELD >> yields.txt

   # run the cardmaker and move the cards to directories
   #./cardmaker.py -s $YIELD -l 20 --systlumiscale True
   #mv ext_vbfhinv_125_13Tev_20fb_scaleL.txt $FILEDIR

   # copy to DCACHE
   #lcg-cp -D srmv2 -b $FILEPATH $DCACHE_SRM_ROOT/store/user/pdunne/miha_dir/Background3/$NAME

#######################################################################
# renaming examples
# FULLDIR=${GZDIR%.*} # remove the .gz to get dir+filename
# NAME=${FULLDIR##*/} # remove the directories to get filename
# DIR=${FULLDIR%/*} # remove filename to get directory only
# NEWDIRNAME=${NAME:9} # remove the first 9 characters

done < "$1"
#echo $INPUTS

#hadd w13delphes-output.root $INPUTS



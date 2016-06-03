#!/bin/bash
# run on master list

INPUTS=""

# remove old files
rm invisibleHa_mchi_mha.txt
rm invisibleH2_mchi_mh2.txt
rm invisibleHiggs_mchi_mh125.txt
rm D5a_mchi_lambda800.txt
rm D5b_mchi_lambda800.txt
rm D5c_mchi_lambda800.txt
rm D5d_mchi_lambda800.txt
rm D6a_mchi_lambda800.txt
rm D6b_mchi_lambda800.txt
rm D7a_mchi_lambda800.txt
rm D7b_mchi_lambda800.txt
rm D7c_mchi_lambda800.txt
rm D7d_mchi_lambda800.txt

#change what the script does to all the files in master list 
while IFS='' read -r line || [[ -n "$line" ]]; do
   # get the file directory and print it
   FILEPATH=$line
   FILEDIR=${line%/*}"/"
   NAME=${line##*/}
   #echo
   #echo $FILEPATH
   #echo $FILEDIR

   # access the number in the jaf file
   NAME=$FILEDIR"jaf_CMS8_hinv20b_analysis20.txt"
   TEXT=$(cat $NAME) # get the text as a variable
   YIELD=${TEXT%%[[:space:]]*} # remove everything after space
   #echo $YIELD

   # invisibleHa parameter values
   if [[ $FILEPATH == *"invisibleHa"* ]]
       then
       mchi=$(echo $FILEPATH | sed -e "s|.*Ha/\(.*\)mchi.*|\1|")
       mha=$(echo $FILEPATH | sed -e "s|.*_\(.*\)mha.*|\1|")
       echo $mchi" "$mha" "$YIELD >> invisibleHa_mchi_mha.txt
   fi

   # invisibleH2 parameter values
   if [[ $FILEPATH == *"invisibleH2"* ]]
       then
       mchi=$(echo $FILEPATH | sed -e "s|.*H2/\(.*\)mchi.*|\1|")
       mha=$(echo $FILEPATH | sed -e "s|.*_\(.*\)mh2.*|\1|")
       echo $mchi" "$mha" "$YIELD >> invisibleH2_mchi_mh2.txt
   fi

   # invisible higgs
     if [[ $FILEPATH == *"invisibleHiggs"* ]]
         then
         mchi=$(echo $FILEPATH | sed -e "s|.*invisibleHiggs/\(.*\)mchi.*|\1|")
         echo $FILEPATH
         echo $mchi
         echo $mchi" "$YIELD >> invisibleHiggs_mchi_mh125.txt
     fi

   # EFT parameter values
   for model in D5a D5b D5c D5d D6a D6b D7a D7b D7c D7d
   do
       if [[ $FILEPATH == *$model* ]]
           then
           mchi=$(echo $FILEPATH | sed -e "s|.*"$model"/\([^\_]*\)chi.*|\1|")
           echo $mchi" "$YIELD >> ${model}_mchi_lambda800.txt
       fi
   done

#######################################################################
# renaming examples
# FULLDIR=${GZDIR%.*} # remove the .gz to get dir+filename
# NAME=${FULLDIR##*/} # remove the directories to get filename
# DIR=${FULLDIR%/*} # remove filename to get directory only
# NEWDIRNAME=${NAME:9} # remove the first 9 characters

done < "$1"

python scripts/plotter_to_log.py -i invisibleHa_mchi_mha.txt
python scripts/plotter_to_log.py -i invisibleH2_mchi_mh2.txt
python scripts/plotter_to_logInvHiggs_interpolate.py -i invisibleHiggs_mchi_mh125.txt
python scripts/plotter_to_logEFT_interpolate.py -i D5a_mchi_lambda800.txt
python scripts/plotter_to_logEFT_interpolate.py -i D5b_mchi_lambda800.txt
python scripts/plotter_to_logEFT_interpolate.py -i D5c_mchi_lambda800.txt
python scripts/plotter_to_logEFT_interpolate.py -i D5d_mchi_lambda800.txt
python scripts/plotter_to_logEFT_interpolate.py -i D6a_mchi_lambda800.txt
python scripts/plotter_to_logEFT_interpolate.py -i D6b_mchi_lambda800.txt
python scripts/plotter_to_logEFT_interpolate.py -i D7a_mchi_lambda800.txt
python scripts/plotter_to_logEFT_interpolate.py -i D7b_mchi_lambda800.txt
python scripts/plotter_to_logEFT_interpolate.py -i D7c_mchi_lambda800.txt
python scripts/plotter_to_logEFT_interpolate.py -i D7d_mchi_lambda800.txt






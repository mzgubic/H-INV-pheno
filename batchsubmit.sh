#!/bin/bash
# run on master list

INPUTS=""

#change what the script does to all the files in master list 
while IFS='' read -r line || [[ -n "$line" ]]; do
   # get the file directory and print it
   #FILEPATH="/vols/cms02/mz2512/matched_files/"${line}
   FILEPATH=$line
   FILEDIR=${line%/*}
   NAME=${FILEPATH##*/}
   NAME=${NAME%_*} ; NAME=${NAME%_*}
   SEED=$( echo $NAME | sed "s/.*seed//")
   echo
   echo $FILEPATH
   echo $FILEDIR
   echo $NAME
   echo $SEED

   # write a script that is meant to be submitted
   echo cd modifiedDelphes-3.2.0 >> $NAME".sh"
   #echo "./DelphesSTDHEP cards/delphes_card_CMS_PileUp40_withsumet.tcl" $FILEDIR"/delphes-output.root" $FILEPATH >> $NAME".sh" # old files without the seed
   echo "./DelphesSTDHEP cards/delphes_card_CMS_PileUp40_withsumet.tcl" $FILEDIR"/delphes-output${SEED}.root" $FILEPATH >> $NAME".sh" # additional higgses 
   echo cd .. >> $NAME".sh"
   chmod +x $NAME".sh"

   # submit a batch job
   qsub -q hepshort.q $NAME".sh" 

   # wait and clean up
   sleep 3s
   rm $NAME".sh"

#######################################################################

done < "$1"



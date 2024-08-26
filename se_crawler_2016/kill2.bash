#! /bin/bash
# ---------------------------------------------------------
# kills jobs using PIDs which are names of files in ./pid subdirectory
# ---------------------------------------------------------

cd $HOME/se_crawler/pid
pwd

# ---------------------------------------------------------
# remove old outputs and logs
# ---------------------------------------------------------

for PID in `ls -1`; 
do
    nn=`ps -p $PID -o args | grep -P 'se_st\d_.*py' | wc -l`
    if (( $nn >= 1 )); then
        mycmd="kill -9 $PID"
        echo $mycmd
        eval $mycmd
    fi
    rm -f $PID
done


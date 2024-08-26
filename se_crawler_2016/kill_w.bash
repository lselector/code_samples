#! /bin/bash
# ---------------------------------------------------------
# kills workers which PIDs are part of file names in ./pid subdirectory
# Example:   pid/w_879
# ---------------------------------------------------------

cd $HOME/se_crawler/pid
# pwd

# ---------------------------------------------------------
# remove old outputs and logs
# ---------------------------------------------------------
for fname in `ls -1`; 
do
  if [[ $fname == *w_* ]]; then
    PID=$(echo $fname | tr -dc '0-9')
    nn=`ps -p $PID -o args | grep -P 'se_st\d_.*py' | wc -l`
    if (( $nn >= 1 )); then
        mycmd="kill -9 $PID"
        echo $mycmd
        eval $mycmd
    fi
    rm -f $fname
  fi
done


#! /bin/bash
# ---------------------------------------------------------
# kills script myrun2.bash which PID is part of file name in ./pid subdirectory
# Example:   pid/m_879
# ---------------------------------------------------------

cd $HOME/se_crawler/pid
# pwd

# ---------------------------------------------------------
# remove old outputs and logs
# ---------------------------------------------------------

for fname in `ls -1`; 
do
  if [[ $fname == *m_* ]]; then
    PID=$(echo $fname | tr -dc '0-9')
    nn=`ps -p $PID -o args | grep myrun2.bash | wc -l`
    if (( $nn >= 1 )); then
        mycmd="kill -9 $PID"
        echo $mycmd
        eval $mycmd
    fi
    rm -f $fname
  fi
done


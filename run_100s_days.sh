#!/bin/bash -x

# --------------------------------------------------------------
# run_100s_days.sh
# a wrapper script to run daily calculations for last 100+ days
# --------------------------------------------------------------
export PYTHONDONTWRITEBYTECODE=1

export MYDIR=/data/apps/some_dir
export MYDATE=`date +%Y%m%d`
export MYDT=`date +"%Y%m%d_%H%M%S"`
echo "MYDATE = $MYDATE"
echo "MYDT   = $MYDT"

myscript=some_script
myscript_py="${myscript}.py"
echo "running $myscript_py for business days going 14*10=140 dates back"

time_out_sec=900

for (( i = 0; i <= 13; i++ )) 
do
    for (( j = 0 ; j <= 9; j++ )) 
    do
        num=$(( 10*i + j ))
        # # check if it is not a weekend
        # mynum=`date -d "-$num days" | grep "Sat\|Sun" | wc -l` # not zero if Sat or Sun
        # if [ $mynum -eq 0 ]   # bus. day
        # then
            mydate=`date -d "-$num days" +"%Y%m%d"`    # shifts date by num days
            mycmd="python3 -uB $myscript_py -d=${mydate} >> /data/log/${myscript}_${mydate}.txt 2>&1 &"
            echo $num ": " $mycmd
            eval $mycmd
        # fi
    done
    echo " "
    echo " waiting batch $i"
    echo " "
    t1=`date +'%s'`           # epoch seconds, int
    t2=$(($t1 + $time_out_sec)) 
    nn=`ps auxww | grep $myscript_py | grep -v grep | wc -l`
    while [ $nn -gt 0 ] && [ $t1 -lt $t2 ]
    do
      sleep 1
      t1=`date +'%s'`
      nn=`ps auxww | grep $myscript_py | grep -v grep | wc -l`
    done

    if [ $nn -gt 0 ]
    then
      echo "ERROR - script $myscript_py is running too long"
      ps auxww | grep $myscript_py | grep -v grep
      echo "Exiting ..."
      exit 1    
    fi

done
echo "all done"
